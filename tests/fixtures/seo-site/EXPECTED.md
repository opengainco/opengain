# Expected evidence

The fixture contains these intentional issues:

- `robots.txt` blocks every crawler from the entire site.
- `pricing.html` has a `noindex` directive despite being a conversion page.
- `sitemap.xml` includes only the homepage and omits the pricing and guide pages.
- `index.html` has an empty title and two H1 headings.
- `index.html` and `pricing.html` use the same meta description.
- `pricing.html` canonicals to an unrelated `example.net` URL.
- `pricing.html` contains invalid JSON-LD because it has a trailing comma.
- The Product structured data has no `offers` information.
- `guide.html` has no canonical link or meta description.
- Images use empty or unhelpful alternative text.

An acceptance response need not use this exact wording. It should cite specific files, separate verified repository observations from inferences, prioritize crawl/indexation problems first, and state that it did not perform a live crawl or use analytics/Search Console data.
