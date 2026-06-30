import { useState } from 'react'
import TravelForm from './components/TravelForm'
import TravelPlanResult from './components/TravelPlanResult'
import LoadingSpinner from './components/LoadingSpinner'
import { generateTravelPlan } from './api/travelApi'

export default function App() {
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(formData) {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await generateTravelPlan(formData)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Travel Planner</h1>
          <p className="text-gray-500 mt-1">AI-powered travel planning — powered by multiple specialized agents</p>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8">
        {/* Form */}
        {!result && !isLoading && (
          <TravelForm onSubmit={handleSubmit} isLoading={isLoading} />
        )}

        {/* Loading */}
        {isLoading && <LoadingSpinner />}

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
            <p className="text-red-700 font-medium">Something went wrong</p>
            <p className="text-red-600 text-sm mt-1">{error}</p>
            <button
              onClick={() => { setError(null); setResult(null) }}
              className="mt-3 text-sm text-red-700 underline cursor-pointer"
            >
              Try again
            </button>
          </div>
        )}

        {/* Results */}
        {result && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Your Travel Plan</h2>
              <button
                onClick={() => { setResult(null); setError(null) }}
                className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg text-sm font-medium transition-colors cursor-pointer"
              >
                Plan Another Trip
              </button>
            </div>
            <TravelPlanResult data={result} />
          </div>
        )}
      </main>
    </div>
  )
}
