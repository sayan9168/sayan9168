# SAYANOX Developer Identity OS

## Architecture

The Identity OS is a static, browser-first developer identity layer. It uses public GitHub data plus local JSON metadata and requires no AI API or private token.

```text
GitHub Public API
       |
       v
 GitHub Service -----> Identity / Project Models
       |                        |
       v                        v
   Live Metrics            Project Explorer
                                |
                                v
                       Developer Card Renderer
                                |
                         Embed / Share Output
```

## Principles

1. Verifiable public data over fabricated metrics.
2. No secrets in client-side code.
3. No paid AI API dependency.
4. Progressive enhancement and mobile-first UI.
5. Accessibility and semantic HTML.
6. GitHub Actions validates every change.

## Data flow

`identity.json` stores curated identity metadata. `projects.json` stores optional featured projects. `app.js` discovers public repositories directly from GitHub and uses live repository metadata for the project explorer and metrics.
