const API_BASE = 'http://localhost:8000'

export async function generateTravelPlan(formData) {
  const response = await fetch(`${API_BASE}/travel/plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Server error' }))
    throw new Error(error.detail || `Request failed with status ${response.status}`)
  }

  return response.json()
}
