import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, it } from 'vitest'
import { App } from './App'

it('lets a teammate search and inspect sample route provenance', async () => {
  const user = userEvent.setup()
  render(<App />)
  expect(screen.getByLabelText('Sample data notice')).toHaveTextContent('fictional')
  await user.type(screen.getByRole('searchbox', { name: 'Find a route' }), 'ridge')
  expect(screen.queryByRole('heading', { name: 'Sample Coastal Loop' })).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Inspect Sample Ridge Walk' }))
  expect(screen.getByRole('region', { name: 'Selected route details' })).toHaveTextContent('sample-ridge-walk')
  await user.click(screen.getByRole('button', { name: 'Close details' }))
  expect(screen.queryByRole('region', { name: 'Selected route details' })).not.toBeInTheDocument()
})

it('shows an explicit empty search result', async () => {
  render(<App />)
  await userEvent.type(screen.getByRole('searchbox'), 'unknown')
  expect(screen.getByRole('status')).toHaveTextContent('No routes match')
})

it('reports invalid source data without displaying misleading routes', () => {
  render(<App source={{ schemaVersion: 999, routes: [] }} />)
  expect(screen.getByRole('alert')).toHaveTextContent('could not be loaded')
  expect(screen.queryByRole('article')).not.toBeInTheDocument()
})
