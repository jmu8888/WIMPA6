# gwmpa.org server rules

Since 2026-10-03 the site at https://www.gwmpa.org/ is this static site, served from the `/wimpa6/` folder on the server by redirect rules in the server's root `.htaccess`. WordPress stays where it was.

- `htaccess-gwmpa-root.txt` — the live `.htaccess` (rules block followed by the standard WordPress lines).
- `htaccess-original-2026-10-03.txt` — the `.htaccess` before the change.

What the rules do:

- `/`, `/zh/`, `/about.html`, `/archive.html`, `/ceremony.html`, `/enter.html`, `/jury.html`, `/winners.html`, `/assets/…`, `/images/…` → the same paths under `/wimpa6/`.
- `/legacy` → the old WordPress home page (`/?page_id=5813`).
- Anything with a query string (`/?page_id=…`), `/wp-admin`, `/wp-content` and other paths still go to WordPress.

To undo: remove the block between `# BEGIN WMPA6` and `# END WMPA6` from the server's `.htaccess`.
