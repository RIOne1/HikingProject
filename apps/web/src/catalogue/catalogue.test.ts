import { describe, expect, it } from 'vitest'
import Ajv2020 from 'ajv/dist/2020'
import fixture from '../../../../shared/fixtures/catalogue.sample.json'
import schema from '../../../../shared/catalogue.schema.json'
import { filterRoutes, parseCatalogue } from './catalogue'

const validateSchema = new Ajv2020().compile(schema)

describe('shared catalogue contract', () => {
  it('loads the shared fixture with explicit units and synthetic attribution', () => {
    const catalogue = parseCatalogue(fixture)
    expect(validateSchema(fixture)).toBe(true)
    expect(catalogue.routes).toHaveLength(2)
    expect(catalogue.routes[0].distanceMetres).toBe(2400)
    expect(catalogue.routes.every(route => route.sourceKind === 'synthetic')).toBe(true)
  })
  it('rejects unsupported versions and duplicate stable IDs', () => {
    expect(() => parseCatalogue({ ...fixture, schemaVersion: 2 })).toThrow(/version/)
    expect(() => parseCatalogue({ ...fixture, routes: [fixture.routes[0], fixture.routes[0]] })).toThrow(/Duplicate/)
  })
  it.each([
    ['startLatitude', 91], ['startLongitude', -181], ['distanceMetres', -1],
    ['distanceMetres', 1.5], ['estimatedMinutes', 0], ['sourceKind', 'verified'], ['name', ' '],
  ])('rejects invalid %s', (field, value) => {
    const input = structuredClone(fixture)
    Object.assign(input.routes[0], { [field]: value })
    expect(validateSchema(input)).toBe(false)
    expect(() => parseCatalogue(input)).toThrow(/Invalid/)
  })
  it('filters case-insensitively and preserves the input catalogue', () => {
    const catalogue = parseCatalogue(fixture)
    expect(filterRoutes(catalogue.routes, '  RIDGE ')).toEqual([catalogue.routes[1]])
    expect(filterRoutes(catalogue.routes, 'missing')).toEqual([])
    expect(catalogue.routes).toHaveLength(2)
  })
})
