# Internal web foundation guide

This is the team's route/content workspace, implemented with **React + TypeScript + Vite**. It is not the consumer hiking client. Local preview currently loads the shared synthetic catalogue, filters route names and displays metadata details. There is no editing persistence, backend, authentication, upload, publication or Mapbox GL JS.

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
- No router, state framework, UI kit or backend client is needed for this single local tool. Add one only when an Issue demonstrates a concrete need. Vite is suitable for this internal client; public SEO/server-rendering requirements would need a separate decision.
- React 19.3.1, Vite 8.3.8, Vitest 5.1.0 and TypeScript 6.0.3 are locked with other dependencies in the root npm lockfile. TypeScript 7 is outside the selected typescript-eslint version's supported range; do not bypass peer checks.
- A root override pins minimatch 11.0.1 to fix [GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249) in lint tooling. Remove the override only after upstream dependency ranges select a patched version and lint/tests/build still pass. The foundation verification includes this overridden combination.

Treat client-side configuration as public. Vite variables are bundled into browser code; never put service credentials into `VITE_*` variables. The foundation needs no environment file. Use synthetic content until licensing, attribution and data provenance are verified.

## Suggested first content work

Agree with the mobile owner on route geometry, provenance, verification timestamps and versioning before building an editor/exporter. A local validation/import preview can be a separate Issue without a hosted service. Display official access information separately from user reports; do not invent current closures or label synthetic data as verified routes.
