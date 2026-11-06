# Congress / Data Center Watch

Static, accessible House and Senate research dashboard. Version 2 is a November 6, 2026 snapshot; it does not automatically update.

## Files
- `dist/index.html`, `dist/style.css`, `dist/app.js`: interface
- `dist/data.js` and `dist/research-data.json`: normalized research data
- `research/`: source research records
- `prepare_data.py`: regenerate normalized data from research records

Run `python prepare_data.py` from the checkout to regenerate data. Review manual amendments before regeneration. Serve `dist/` as a static website. Hash URLs identify each profile.

## Editorial rules
Race calls are not certification. Exclude uncalled races from profile totals. Include returning former members but identify them. Preserve early-seating caveats for Brown and Hern. Position labels overlap and require specific source evidence. Moratoria must be qualified by duration and jurisdiction. A yes/no vote on one bill is not a general judgment about regulation. Do not infer positions from party or general AI policy.

Each profile preserves quotations, source dates and URLs, policy proposals, campaign priority evidence and coding rationale. Source text is summarized with short excerpts. Federal records distinguish enactment, proposals, votes, hearings and oversight. Federal action records are selected examples, not an exhaustive census.

The interface provides filtered CSV and full JSON exports, chamber/district search and party/state/position/evidence filters, per-member URLs, printable profiles, accessible chart descriptions and underlying counts. Color is supplemented by party labels.

## GitHub upload

Extract this ZIP and upload its contents to a new GitHub repository. The package already includes README.md, so you do not need GitHub to generate another README. Keep the dist and research folders intact.

The website is in dist/. This is plain HTML, CSS and JavaScript: no npm install, API keys, database or build step is needed. For local preview with Python installed, run `python -m http.server 8000 --directory dist` and open http://localhost:8000.

For a static web host, select dist as the published directory. Uploading the code to GitHub alone does not publish a website. This export does not include the private Sites hosting configuration or authentication. A separately published static copy will have the access controls of its new host.

Research is a manual November 6, 2026 snapshot. Changes in this repository do not automatically sync to the ChatGPT-hosted dashboard. Edit research records, run `python prepare_data.py`, and commit both research and generated dist data files. Preserve citations, uncertainty notes and classification scope.

Exported from dashboard revision 1c145c905f91a41235ce574b157920a194a40c19. Includes the incoming House and Senate profiles, current-Congress records and the latest headings.
