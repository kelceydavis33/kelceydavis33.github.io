---
layout: page
title: Curriculum vitae
permalink: /cv/
---

<p class="cv-actions">
  <a class="cv-download" href="{{ site.cv_file | relative_url }}" download>Download CV (PDF)</a>
</p>

<object class="cv-embed" data="{{ site.cv_file | relative_url }}" type="application/pdf">
  <div class="cv-fallback">
    <p>Your browser will not display the PDF inline. Use the download button above
    to open it, or read it directly at
    <a href="{{ site.cv_file | relative_url }}">{{ site.cv_file }}</a>.</p>
  </div>
</object>

<p class="figure-note">
To update this page, replace <code>assets/cv.pdf</code> in the repository with a
new file of the same name. Nothing else needs to change.
</p>
