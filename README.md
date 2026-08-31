# kelceydavis33.github.io

Personal academic site. Static, built by Jekyll, hosted free on GitHub Pages.
The publication list, citation statistics and word cloud refresh themselves
from NASA ADS on the first of every month.

## Setting it up (about 20 minutes, once)

### 1. Create the repository

Make a **public** repository named exactly `kelceydavis33.github.io` and push
these files to a branch called `main`. The name matters: a repository named
after your username is served from the root of the domain, which ranks better
in search than a project subpath.

If you use a different name, set `baseurl: "/thatname"` in `_config.yml`.

### 2. Get an ADS API token

Log in at <https://ui.adsabs.harvard.edu/user/settings/token> and generate a
token. It is free and takes a moment.

In the repository, go to **Settings -> Secrets and variables -> Actions ->
New repository secret**. Name it `ADS_TOKEN` and paste the token as the value.
Do not commit the token to a file.

### 3. Turn on Pages

**Settings -> Pages -> Build and deployment -> Source: GitHub Actions.**
Not "Deploy from a branch" — the workflow here builds and deploys by itself.

### 4. Load your publications

**Actions -> Build site and refresh publications -> Run workflow.** This pulls
everything from ADS, commits the data, and publishes the site. After this it
runs on its own each month.

## Adding your own content

| What | Where |
|---|---|
| Your bio | `index.md` |
| Research summary | `research/index.md` |
| Topic descriptions | `research/little-red-dots.md` and the other two |
| Your CV | replace `assets/cv.pdf`, keeping that filename |
| Topic images | replace `assets/img/lrd.png`, `eelg.png`, `survey.png` |
| Email, links, affiliations | `_config.yml` |

Anything marked with a grey left bar on the live site is placeholder text
waiting to be replaced.

## Sorting papers onto research pages

`_data/topics.yml` decides which papers appear on which topic page. A paper is
tagged if any of that topic's keywords appears in its title, abstract or ADS
keywords.

Expect to tune this once real data loads. When the keywords get something
wrong, override it by hand:

```yaml
lrd:
  always: ["2025ApJ...968...19D"]   # force this paper onto the page
  never:  ["2024ApJ...950..100S"]   # keep this one off it
```

A bibcode looks like `2025ApJ...968...19D` and sits at the top of every ADS
abstract page.

## Running the refresh yourself

```bash
pip install -r scripts/requirements.txt
export ADS_TOKEN="your token"
python scripts/update_publications.py
```

Writes `_data/publications.json` and `_data/wordcloud.json`. Commit both.

## Previewing locally (optional)

```bash
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>. Requires Ruby. You do not need this to
publish — pushing to `main` is enough.

## Being findable by name

The homepage carries a schema.org Person record linking your name to your
ORCID, ADS and GitHub, and `jekyll-sitemap` generates a sitemap. That handles
the technical side. The rest is links: search engines rank you on who points at
you, so add this URL to your ORCID record, your ADS profile, your department
page, Google Scholar and your email signature. That does more for ranking than
anything on the site itself.

Once live, submit the URL to Google Search Console to speed up first indexing.

## Notes

- The monthly job is a GitHub Actions `schedule`. GitHub disables scheduled
  workflows after roughly 60 days of repository inactivity; if the site goes
  quiet for months, check the Actions tab and re-enable it.
- Ordinary pushes rebuild the site but do not re-query ADS, which keeps edits
  fast and stays well inside the API rate limit.
- Conference abstracts, proposals and errata are filtered out. Change
  `SKIP_DOCTYPES` at the top of `scripts/update_publications.py` to keep them.
- `scripts/make_bandpass_figure.py` regenerates the homepage figure. You only
  need it if you want different filters shown.
