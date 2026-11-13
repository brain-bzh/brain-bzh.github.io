# BRAIN team website

An al-folio/Jekyll site for the BRAIN research team at IMT Atlantique and Lab-STICC. The custom homepage keeps the team's visual identity; the publications page uses al-folio and Jekyll Scholar to render the HAL bibliography. Content is a draft for team review.

## Preview locally

Install Ruby 3.3 and Bundler, then from the repository root:

```sh
bundle install
bundle exec jekyll serve
```

Open http://127.0.0.1:4000/. Edit the homepage in `index.html`, its styling in `assets/style.css`, the publications page in `_pages/publications.md`, and team members in `_data/people.yml`. The announcements page displays al-folio news entries added to `_news/` (see `CONTRIBUTING.md`). The homepage's selected papers are manually curated; edit them there after checking conference acceptance. The gem's bibliography and theme layouts handle the publications page. `assets/css/main.scss` is a local visual override of al-folio's main stylesheet, so review it when upgrading the core gem.

## HAL bibliography

```sh
python3 scripts/update_hal.py
bundle exec jekyll build
```

The importer queries HAL for the former (1149551) and current (1251172) `Lab_STICC_BRAIn` structure IDs, then writes `_bibliography/papers.bib` for Jekyll Scholar and `data/hal-publications.json`. HAL's BibTeX is preserved apart from adding an `HTML` field for each HAL landing page so al-folio can link to it. The importer paginates and validates counts before writing. It includes all document types. Records without these affiliations or absent from HAL will be missing; affiliated historical work can also predate the structures. Verify coverage with the team and correct affiliations in HAL where appropriate. The two highlighted papers on the homepage are maintained separately.

The weekly and manually runnable `update-hal.yml` workflow proposes generated changes in a pull request. Repository Actions settings must permit Actions to create pull requests. Review changes before merging. No HAL credentials are needed.

## Deployment when ready

The Pages workflow builds the Jekyll site with Ruby 3.3 and deploys on pushes to `main` after Pages is set to GitHub Actions. The root URL is `https://brain-bzh.github.io` with an empty `baseurl`. Existing project sites such as `/reve/` and `/llm-course/` are maintained separately; verify them after launch. Nothing has been pushed or deployed during local development.

## Visual identity

`assets/img/brain-logo.svg` is a vector conversion of the team-provided BRAIN logo PDF; its page was cropped around the artwork. `assets/img/imt-atlantique.svg` is the transparent RGB logo for light backgrounds from [IMT Atlantique's official logo page](https://www.imt-atlantique.fr/en/about/logos). The homepage's own header is in `index.html`; the other pages use a local override of al-folio's `_includes/header.liquid`. Both that override and the custom `assets/css/main.scss` are recorded in `.al-folio-overrides.yml` for upgrade reviews.

### Featured venues and publication search

`data/featured-venues.json` is the editable list of major conference and journal names used for highlights. All conference and journal records with venue metadata receive a colored venue badge, regardless of highlight status. The HAL updater matches conference or journal metadata for conference and journal records and adds `FEATURED = {true}` for a highlight; `ABBR` and `VENUECOLOR` provide the label and color of each venue badge. The initial list is a starting point for team review, not an objective ranking. Workshops, Findings and related tracks are excluded from automatic conference matches. HAL metadata may be incomplete or inaccurate; a badge is a venue match, not independent verification of acceptance. After changing the list, rerun `python3 scripts/update_hal.py` and review the generated differences. The homepage's selected work remains independently curated.

The Publications page uses al-folio's bibliography search to filter by text. Check the venue classifier with `python3 -m unittest discover -s tests`.

Publication categories are derived from HAL's document type (`HALTYPE` in generated BibTeX). HAL `UNDEFINED` is displayed as “Preprint / working paper”; it is a broad HAL category, so check individual records. Highlight status is a separate venue-based flag. The local `_layouts/bib.liquid` override displays both and should be reviewed when updating al-folio.

ArXiv badges use `arxivId_s` from HAL. Where a verified paper is missing that field, add its HAL ID and arXiv ID to `data/arxiv-overrides.json`, then rerun the importer. A missing badge does not mean that a paper is absent from arXiv.
