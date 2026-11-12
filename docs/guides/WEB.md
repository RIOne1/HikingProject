# Web foundation and planner guide

The approved Web product uses **React + TypeScript + Vite** for a public precision planner, condition reports and an administrator console. The implemented foundation still only loads the synthetic catalogue, filters names and displays metadata. There is no editing persistence, backend, authentication, upload, publication or Mapbox GL JS yet. [MVP-13 through MVP-20](../MVP.md#mvp-13--precise-web-route-planning) define the target; this guide does not claim those features work.

## Run and verify

Use Node 24.20.0 from `.nvmrc` and npm 11 or 12. From the repository root:

```bash
npm ci
npm run dev:web
```

Open the localhost URL printed by Vite. The server binds to `127.0.0.1`; do not expose an unauthenticated future content tool publicly. To check or build:

```bash
npm run check:web
npm run build:web
```

`check:web` runs ESLint, Vitest/Testing Library tests, TypeScript checking and the production build. Output is `apps/web/dist/` and is ignored. Building does not publish a site. For focused work, use `npm run test --workspace @hikingproject/web` or `npm run lint --workspace @hikingproject/web`.

## Code and dependency choices

- `src/App.tsx` owns the small catalogue UI; keep pure contract/filter logic in `src/catalogue/catalogue.ts`.
- Both clients consume `shared/fixtures/catalogue.sample.json`. Tests also compile the JSON Schema with Ajv and check representative malformed values. Follow the [data guide](DATA.md) for field/constraint changes.
- Vitest uses jsdom and React Testing Library to exercise search, selection, invalid content and empty results. Prefer observable behaviour to component-internal assertions.
- No router, state framework, UI kit or backend client is installed in the current single-screen preview. Add needed dependencies with their implementation Issue and review. Keep React/TypeScript/Vite for the planned interactive Web client; public SEO/server-rendering needs are not an implicit decision to migrate to Next.js.
- React 19.3.1, Vite 8.3.8, Vitest 5.1.0 and TypeScript 6.0.3 are locked with other dependencies in the root npm lockfile. TypeScript 7 is outside the selected typescript-eslint version's supported range; do not bypass peer checks.
- A root override pins minimatch 11.0.1 to fix [GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249) in lint tooling. Remove the override only after upstream dependency ranges select a patched version and lint/tests/build still pass. The foundation verification includes this overridden combination.

Treat client-side configuration as public. Vite variables are bundled into browser code; never put service credentials into `VITE_*` variables. The foundation needs no environment file. Use synthetic content until licensing, attribution and data provenance are verified.

## Planned responsibilities and verification

| Surface | Scope and important cases |
| --- | --- |
| Public planner | Whole trail → junction segment → partial segment, snapping and via points; preserve selection/direction/order and confirm connectors. Test loops, repeated traversal, partial boundaries and rejected disconnection/closures |
| Private plans | Email/password login for account-owned save/sync; exact route revisions and explicit stale-edit conflicts. Do not upload raw mobile history as plan data |
| Reports | Permit incomplete-hike reports; label provenance/time and unverified status separately from official/confirmed closures |
| Administrator console | User/content/status management and submitted-evidence review; server-authorized actions with reasons/revisions. No direct editing of private plans or unrestricted trip-history access |
| Publication/deletion | Completion evidence plus feedback, deliberate submission, administrator decision, revision review and withdrawal/account deletion; public pages never expose raw private tracks |

Agree network geometry, topology, attribution and version semantics with mobile before implementing the editor. Mapbox GL JS supplies rendering/interaction; checked graph data, snapping and route construction require their own validation. A provider-generated line cannot silently replace selected segments. Use the [data guide](DATA.md) and [backend guide](BACKEND.md), not the metadata-only sample as a production route model.

Add component and contract cases with each feature, plus backend tests proving ordinary users cannot invoke administrator operations or read another user's private data. Test loading/error/expired-session states and retry/conflict behaviour at meaningful boundaries. Current tests cover the catalogue only. Publication, moderation/reporting/blocking/contact and real email/recovery/deletion require their own evidence before external use. Do not label synthetic data as verified routes or invent current closures.
