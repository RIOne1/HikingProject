export interface RouteSummary {
  id: string
  name: string
  difficulty: 'easy' | 'moderate'
  distanceMetres: number
  estimatedMinutes: number
  startLatitude: number
  startLongitude: number
  sourceKind: 'synthetic'
  attribution: string
}

export interface Catalogue {
  schemaVersion: 1
  routes: RouteSummary[]
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function nonBlank(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0
}

function inRange(value: unknown, min: number, max: number): value is number {
  return typeof value === 'number' && Number.isFinite(value) && value >= min && value <= max
}

// This is the external JSON boundary. Components consume the validated type,
// rather than duplicating guards at every render or trusting a type assertion.
export function parseCatalogue(input: unknown): Catalogue {
  if (!isRecord(input) || input.schemaVersion !== 1 || !Array.isArray(input.routes)) {
    throw new Error('Unsupported catalogue format or version.')
  }
  if (input.routes.length > 100) throw new Error('The foundation catalogue limit is 100 routes.')
  const ids = new Set<string>()
  const routes = input.routes.map((route: unknown): RouteSummary => {
    if (!isRecord(route) || !nonBlank(route.id) || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(route.id)
      || !nonBlank(route.name) || !nonBlank(route.attribution)
      || (route.difficulty !== 'easy' && route.difficulty !== 'moderate')
      || !inRange(route.distanceMetres, 1, 100_000) || !Number.isInteger(route.distanceMetres)
      || !inRange(route.estimatedMinutes, 1, 1440) || !Number.isInteger(route.estimatedMinutes)
      || !inRange(route.startLatitude, -90, 90) || !inRange(route.startLongitude, -180, 180)
      || route.sourceKind !== 'synthetic') {
      throw new Error('Invalid route metadata.')
    }
    if (ids.has(route.id)) throw new Error(`Duplicate route ID: ${route.id}`)
    ids.add(route.id)
    return {
      id: route.id, name: route.name, difficulty: route.difficulty,
      distanceMetres: route.distanceMetres, estimatedMinutes: route.estimatedMinutes,
      startLatitude: route.startLatitude, startLongitude: route.startLongitude,
      sourceKind: route.sourceKind, attribution: route.attribution,
    }
  })
  return { schemaVersion: 1, routes }
}

export function filterRoutes(routes: RouteSummary[], query: string): RouteSummary[] {
  const term = query.trim().toLocaleLowerCase('en-NZ')
  return routes.filter(route => route.name.toLocaleLowerCase('en-NZ').includes(term))
}
