import { serviceStatusQuery } from './graphql/operations/serviceStatus'

const endpoint =
  import.meta.env.VITE_GRAPHQL_URL ||
  (import.meta.env.DEV ? '/graphql' : 'http://127.0.0.1:8000/graphql')

export async function fetchServiceStatus(): Promise<boolean> {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: serviceStatusQuery }),
    signal: AbortSignal.timeout(5000),
  })

  if (!response.ok) {
    return false
  }

  const result: { data?: { serviceStatus?: string } } = await response.json()
  return result.data?.serviceStatus === 'ok'
}
