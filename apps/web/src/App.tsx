import { useState } from 'react'
import sampleCatalogue from '../../../shared/fixtures/catalogue.sample.json'
import { filterRoutes, parseCatalogue } from './catalogue/catalogue'

export function App({ source = sampleCatalogue }: { source?: unknown }) {
  const [query, setQuery] = useState('')
  const [selectedID, setSelectedID] = useState<string>()
  let catalogue
  try {
    catalogue = parseCatalogue(source)
  } catch {
    return <main className="workspace"><h1>Route workspace</h1><p role="alert">The catalogue could not be loaded. Check its format and version before continuing.</p></main>
  }
  const routes = filterRoutes(catalogue.routes, query)
  const selected = catalogue.routes.find(route => route.id === selectedID)

  return (
    <main className="workspace">
      <header className="header">
        <div className="brand"><span className="brand-mark" aria-hidden="true">△</span> HikingProject <span className="team-tag">TEAM WORKSPACE</span></div>
        <p className="eyebrow">ROUTES & CONTENT</p>
        <h1>A clear starting point<br />for every trail.</h1>
        <p className="intro">Review route metadata in one shared workspace before preparing it for the mobile catalogue.</p>
      </header>
      <aside className="notice" aria-label="Sample data notice">
        <strong>Sample catalogue</strong><span>These fictional routes are development fixtures. They are not verified hiking guidance.</span>
      </aside>
      <section aria-labelledby="catalogue-heading">
        <div className="section-heading"><h2 id="catalogue-heading">Route catalogue</h2><span>{routes.length} of {catalogue.routes.length} routes</span></div>
        <label className="search-label">Find a route<input type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder="Search route names" /></label>
        <div className="route-grid">
          {routes.map(route => (
            <article className="route-card" key={route.id}>
              <span className={`difficulty ${route.difficulty}`}>{route.difficulty}</span>
              <h3>{route.name}</h3>
              <p className="route-metrics">{(route.distanceMetres / 1000).toFixed(1)} km <span aria-hidden="true">·</span> {route.estimatedMinutes} min</p>
              <p className="muted">Synthetic route · source check required</p>
              <button aria-pressed={selectedID === route.id} onClick={() => setSelectedID(route.id)}>Inspect {route.name}<span aria-hidden="true"> ↗</span></button>
            </article>
          ))}
        </div>
        {routes.length === 0 && <p role="status" className="empty">No routes match “{query}”. Try another name.</p>}
      </section>
      {selected && <section className="details" aria-label="Selected route details">
        <div className="section-heading"><h2>{selected.name}</h2><button onClick={() => setSelectedID(undefined)}>Close details</button></div>
        <dl><div><dt>Route ID</dt><dd>{selected.id}</dd></div><div><dt>Sample start coordinate</dt><dd>{selected.startLatitude}, {selected.startLongitude}</dd></div><div><dt>Attribution</dt><dd>{selected.attribution}</dd></div></dl>
      </section>}
      <footer>HikingProject <span>Internal content preview · no publishing connection</span></footer>
    </main>
  )
}
