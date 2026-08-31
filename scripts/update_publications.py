"""
Refresh the publication data that the website reads.

Writes two files:
    _data/publications.json   every paper, plus citation statistics
    _data/wordcloud.json      the most common terms across those papers

Needs an ADS API token in the ADS_TOKEN environment variable. Get one at
https://ui.adsabs.harvard.edu/user/settings/token

    python scripts/update_publications.py

If you have no token there is a rough arXiv fallback, but arXiv cannot search
by ORCID, so it looks you up by name and will pick up other people called
Davis. Only use it as a stopgap:

    python scripts/update_publications.py --arxiv-fallback
"""

import json
import os
import re
import sys
import urllib.parse
from datetime import date

import requests
import yaml

# --- things you might want to change ---------------------------------------

ORCID = "0000-0001-8047-8351"
SURNAME = "Davis"
FIRST_INITIAL = "K"

# Document types that should not appear on the site. Remove an entry here if
# you want it listed. "abstract" means conference abstracts, which ADS holds
# separately from the talks themselves.
SKIP_DOCTYPES = [
    "abstract",
    "catalog",
    "proposal",
    "software",
    "erratum",
    "bookreview",
    "editorial",
    "pressrelease",
]

# How many terms to show in the word cloud.
CLOUD_SIZE = 45

# --- ADS endpoints ---------------------------------------------------------

SEARCH_URL = "https://api.adsabs.harvard.edu/v1/search/query"
METRICS_URL = "https://api.adsabs.harvard.edu/v1/metrics"
WORDCLOUD_URL = "https://api.adsabs.harvard.edu/v1/vis/word-cloud"

QUERY = 'orcid_pub:"{0}" OR orcid_user:"{0}" OR orcid_other:"{0}"'.format(ORCID)

FIELDS = ",".join([
    "bibcode", "title", "author", "first_author", "year", "pubdate",
    "pub", "bibstem", "volume", "page", "doi", "identifier",
    "citation_count", "abstract", "doctype", "property", "keyword",
])


def fetch_papers(token):
    """Get every ADS record attached to the ORCID, one page at a time."""
    headers = {"Authorization": "Bearer " + token}
    docs = []
    start = 0

    while True:
        params = {
            "q": QUERY,
            "fl": FIELDS,
            "rows": 200,
            "start": start,
            "sort": "date desc, bibcode desc",
        }
        response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        body = response.json()["response"]

        docs = docs + body["docs"]
        start = start + 200

        if start >= body["numFound"]:
            break

    print("ADS returned {} records".format(len(docs)))
    return docs


def fetch_metrics(token, bibcodes):
    """Ask ADS for h-index and citation totals. Returns {} if it fails."""
    headers = {"Authorization": "Bearer " + token}

    try:
        response = requests.post(METRICS_URL, headers=headers,
                                 json={"bibcodes": bibcodes}, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as problem:
        print("Could not fetch metrics from ADS: {}".format(problem))
        return {}


def fetch_wordcloud(token):
    """Ask ADS for term frequencies across the publication list."""
    headers = {"Authorization": "Bearer " + token}

    try:
        response = requests.post(WORDCLOUD_URL, headers=headers,
                                 json={"q": QUERY, "rows": 200}, timeout=90)
        response.raise_for_status()
        body = response.json()
    except Exception as problem:
        print("Could not fetch the word cloud from ADS: {}".format(problem))
        return {}

    # The service has returned the terms both at the top level and under a
    # "wordCloud" key at different times, so accept either shape.
    if isinstance(body, dict) and "wordCloud" in body:
        return body["wordCloud"]
    return body


def wordcloud_from_text(papers):
    """Fallback: count words in the titles and abstracts we already have."""
    stopwords = set("""
        a an and are as at be been but by can for from has have how in into is it
        its of on or that the their there these this to was we were what when
        which with within we our using used use show shows shown new results
        results find found also between during more most than then they them
        such over under both each other same very much many two three one
        """.split())

    counts = {}
    for paper in papers:
        text = paper["title"] + " " + paper.get("abstract_text", "")
        for word in re.findall(r"[A-Za-z][A-Za-z\-]{2,}", text.lower()):
            if word in stopwords:
                continue
            counts[word] = counts.get(word, 0) + 1

    terms = {}
    for word in counts:
        terms[word] = {"total_occurrences": counts[word]}
    return terms


def build_wordcloud(terms):
    """Turn raw term frequencies into the list the site renders."""
    ranked = []
    for word in terms:
        if len(word) < 3 or word.isdigit():
            continue

        entry = terms[word]
        if isinstance(entry, dict):
            count = entry.get("total_occurrences", entry.get("record_count", 0))
        else:
            count = entry

        ranked.append((count, word))

    ranked.sort(reverse=True)
    ranked = ranked[:CLOUD_SIZE]

    # Size by rank rather than by raw count, so one runaway term does not
    # flatten everything else.
    words = []
    for position in range(len(ranked)):
        count, word = ranked[position]

        if position < 3:
            weight = 5
        elif position < 9:
            weight = 4
        elif position < 19:
            weight = 3
        elif position < 31:
            weight = 2
        else:
            weight = 1

        search = 'orcid:"{}" abs:"{}"'.format(ORCID, word)
        url = "https://ui.adsabs.harvard.edu/search/q=" + urllib.parse.quote(search)

        words.append({
            "text": word,
            "count": count,
            "weight": weight,
            "url": url,
        })

    # Alphabetical order reads better than descending frequency in a cloud.
    words.sort(key=lambda item: item["text"])
    return words


def shorten_name(name):
    """Turn "Davis, Kelcey" into "Davis, K."."""
    if "," not in name:
        return name

    surname, given = name.split(",", 1)
    given = given.strip()
    if given == "":
        return surname.strip()

    initials = ""
    for part in given.replace(".", " ").split():
        initials = initials + part[0].upper() + ". "

    return surname.strip() + ", " + initials.strip()


def format_authors(authors, is_first_author):
    """A short author string for the paper lists."""
    if len(authors) == 0:
        return ""

    shown = []
    for name in authors[:3]:
        shown.append(shorten_name(name))

    if len(authors) <= 3:
        return ", ".join(shown)

    line = ", ".join(shown) + ", et al."

    me = SURNAME + ", " + FIRST_INITIAL + "."
    if not is_first_author and me not in shown:
        line = line + " (incl. {})".format(me)

    return line


def format_reference(doc, is_refereed):
    """A short journal reference like "ApJ, 968, 19"."""
    stems = doc.get("bibstem", [])
    if len(stems) > 0:
        journal = stems[0]
    else:
        journal = doc.get("pub", "")

    if journal.startswith("arXiv") or not is_refereed:
        return "Preprint, {}".format(doc.get("year", ""))

    pieces = [journal]
    if doc.get("volume"):
        pieces.append(doc["volume"])

    pages = doc.get("page", [])
    if len(pages) > 0:
        pieces.append(pages[0])

    return ", ".join(pieces) + " ({})".format(doc.get("year", ""))


def find_arxiv_url(doc):
    """Pull an arXiv link out of the ADS identifier list, if there is one."""
    for identifier in doc.get("identifier", []):
        match = re.match(r"^arXiv:(\d{4}\.\d{4,5})", identifier)
        if match:
            return "https://arxiv.org/abs/" + match.group(1)
    return ""


def assign_topics(paper, topics):
    """Decide which research pages this paper belongs on."""
    haystack = (paper["title"] + " " + paper.get("abstract_text", "")
                + " " + paper.get("keyword_text", "")).lower()

    found = []
    for key in topics:
        rules = topics[key]

        if paper["bibcode"] in (rules.get("never") or []):
            continue

        if paper["bibcode"] in (rules.get("always") or []):
            found.append(key)
            continue

        for keyword in rules.get("keywords", []):
            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
            if re.search(pattern, haystack):
                found.append(key)
                break

    return found


def tidy(doc, topics):
    """Turn one raw ADS record into the shape the site templates expect."""
    titles = doc.get("title", [""])
    title = titles[0]

    properties = doc.get("property", [])
    is_refereed = "REFEREED" in properties

    first_author = doc.get("first_author", "")
    is_first_author = first_author.lower().startswith(SURNAME.lower() + ",")
    if is_first_author:
        given = first_author.split(",", 1)[1].strip()
        is_first_author = given[:1].upper() == FIRST_INITIAL.upper()

    paper = {
        "bibcode": doc["bibcode"],
        "title": title,
        "authors_short": format_authors(doc.get("author", []), is_first_author),
        "author_count": len(doc.get("author", [])),
        "year": int(doc.get("year", 0)),
        "pubdate": doc.get("pubdate", ""),
        "reference": format_reference(doc, is_refereed),
        "citations": doc.get("citation_count", 0),
        "refereed": is_refereed,
        "role": "first" if is_first_author else "co",
        "url_ads": "https://ui.adsabs.harvard.edu/abs/{}/abstract".format(
            urllib.parse.quote(doc["bibcode"])),
        "url_arxiv": find_arxiv_url(doc),
        "url_doi": "",
    }

    dois = doc.get("doi", [])
    if len(dois) > 0:
        paper["url_doi"] = "https://doi.org/" + dois[0]

    # Kept only long enough to sort the paper onto topic pages, then dropped.
    abstracts = doc.get("abstract", "")
    if isinstance(abstracts, list):
        abstracts = " ".join(abstracts)
    paper["abstract_text"] = abstracts
    paper["keyword_text"] = " ".join(doc.get("keyword", []))

    paper["topics"] = assign_topics(paper, topics)
    return paper


def drop_duplicates(papers):
    """Keep one record per paper when ADS holds both a preprint and a journal
    version. The refereed one wins."""
    best = {}
    order = []

    for paper in papers:
        key = re.sub(r"[^a-z0-9]", "", paper["title"].lower())[:80]

        if key not in best:
            best[key] = paper
            order.append(key)
            continue

        if paper["refereed"] and not best[key]["refereed"]:
            best[key] = paper

    kept = []
    for key in order:
        kept.append(best[key])

    if len(kept) < len(papers):
        print("Merged {} preprint and journal pairs".format(len(papers) - len(kept)))

    return kept


def compute_stats(papers, metrics):
    """Citation statistics, taken from ADS where possible."""
    n_refereed = 0
    n_first = 0
    citations_total = 0
    counts = []

    for paper in papers:
        if paper["refereed"]:
            n_refereed = n_refereed + 1
        if paper["role"] == "first":
            n_first = n_first + 1
        citations_total = citations_total + paper["citations"]
        counts.append(paper["citations"])

    counts.sort(reverse=True)

    h_index = 0
    for position in range(len(counts)):
        if counts[position] >= position + 1:
            h_index = position + 1

    i10_index = 0
    for count in counts:
        if count >= 10:
            i10_index = i10_index + 1

    # ADS computes these more carefully than we can, so prefer its numbers.
    indicators = metrics.get("indicators", {})
    citation_stats = metrics.get("citation stats", {})

    if "h" in indicators:
        h_index = indicators["h"]
    if "i10" in indicators:
        i10_index = indicators["i10"]
    if "total number of citations" in citation_stats:
        citations_total = citation_stats["total number of citations"]

    return {
        "n_papers": len(papers),
        "n_refereed": n_refereed,
        "n_first_author": n_first,
        "citations_total": int(citations_total),
        "h_index": int(h_index),
        "i10_index": int(i10_index),
        "updated": date.today().isoformat(),
    }


def fetch_from_arxiv():
    """Stopgap for when there is no ADS token. arXiv has no ORCID search, so
    this matches on name and will include papers by other people."""
    print("Using the arXiv fallback. Check the results by hand.")

    search = 'au:"{}, {}" AND cat:astro-ph*'.format(SURNAME, FIRST_INITIAL)
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": search,
        "start": 0,
        "max_results": 200,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    docs = []
    for entry in re.findall(r"<entry>(.*?)</entry>", response.text, re.S):
        title = re.search(r"<title>(.*?)</title>", entry, re.S)
        link = re.search(r"<id>(.*?)</id>", entry)
        published = re.search(r"<published>(\d{4})", entry)
        summary = re.search(r"<summary>(.*?)</summary>", entry, re.S)
        authors = re.findall(r"<name>(.*?)</name>", entry)

        if title is None or link is None:
            continue

        arxiv_id = link.group(1).rsplit("/", 1)[-1]
        docs.append({
            "bibcode": "arXiv:" + arxiv_id,
            "title": [" ".join(title.group(1).split())],
            "author": authors,
            "first_author": authors[0] if authors else "",
            "year": published.group(1) if published else "0",
            "pubdate": "",
            "bibstem": ["arXiv"],
            "property": [],
            "citation_count": 0,
            "abstract": " ".join(summary.group(1).split()) if summary else "",
            "identifier": ["arXiv:" + arxiv_id],
            "doctype": "eprint",
        })

    print("arXiv returned {} records".format(len(docs)))
    return docs


def main():
    use_arxiv = "--arxiv-fallback" in sys.argv
    token = os.environ.get("ADS_TOKEN", "").strip()

    if token == "" and not use_arxiv:
        print("No ADS_TOKEN set. Leaving the existing data files alone.")
        print("Add the token as a repository secret named ADS_TOKEN, or run")
        print("this script with --arxiv-fallback.")
        sys.exit(1)

    with open("_data/topics.yml") as handle:
        topics = yaml.safe_load(handle)

    if use_arxiv:
        docs = fetch_from_arxiv()
    else:
        docs = fetch_papers(token)

    papers = []
    for doc in docs:
        if doc.get("doctype", "") in SKIP_DOCTYPES:
            continue
        papers.append(tidy(doc, topics))

    papers = drop_duplicates(papers)
    papers.sort(key=lambda paper: (paper["pubdate"], paper["bibcode"]), reverse=True)

    if use_arxiv:
        metrics = {}
        terms = wordcloud_from_text(papers)
    else:
        bibcodes = []
        for paper in papers:
            bibcodes.append(paper["bibcode"])

        metrics = fetch_metrics(token, bibcodes)

        terms = fetch_wordcloud(token)
        if len(terms) == 0:
            print("Falling back to counting words in the titles and abstracts.")
            terms = wordcloud_from_text(papers)

    stats = compute_stats(papers, metrics)

    # The abstract text was only needed for topic matching; drop it so the
    # committed data file stays small.
    for paper in papers:
        paper.pop("abstract_text", None)
        paper.pop("keyword_text", None)

    with open("_data/publications.json", "w") as handle:
        json.dump({"stats": stats, "papers": papers}, handle, indent=2)
        handle.write("\n")

    cloud = {"updated": stats["updated"], "words": build_wordcloud(terms)}
    with open("_data/wordcloud.json", "w") as handle:
        json.dump(cloud, handle, indent=2)
        handle.write("\n")

    for key in topics:
        tagged = 0
        for paper in papers:
            if key in paper["topics"]:
                tagged = tagged + 1
        print("{:8s} {} papers".format(key, tagged))

    print("Wrote {} papers, h={}, {} citations".format(
        stats["n_papers"], stats["h_index"], stats["citations_total"]))


if __name__ == "__main__":
    main()
