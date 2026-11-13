# Updating the site

Edit `_data/people.yml` to update the team directory. The list was initially transcribed from IMT Atlantique and should be checked with the team.

To add an announcement, create a Markdown file in `_news/`, for example `_news/announcement_2026_11_13.md`:

```markdown
---
layout: post
date: 2026-11-13
inline: true
---
A short, confirmed team announcement goes here.
```

`inline: true` displays the text on the announcements page. For a longer item, set `inline: false`, add `title: ...`, and write the full post below the front matter. Run `bundle exec jekyll serve` to preview the site. Dates and example text above are placeholders, not a real announcement.
