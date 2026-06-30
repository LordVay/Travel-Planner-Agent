export default function DiningPlan({ data }) {
  if (!data) return null

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <h2 className="text-xl font-bold text-orange-600 mb-4">Dining Plan</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
        {data.total_meal_budget && (
          <div>
            <p className="text-xs text-gray-500">Total Meal Budget</p>
            <p className="font-semibold text-gray-800">{data.total_meal_budget}</p>
          </div>
        )}
        {data.daily_meal_budget && (
          <div>
            <p className="text-xs text-gray-500">Daily Budget</p>
            <p className="font-semibold text-gray-800">{data.daily_meal_budget}</p>
          </div>
        )}
        {data.cuisine_preferences && (
          <div>
            <p className="text-xs text-gray-500">Cuisine</p>
            <p className="font-semibold text-gray-800">{data.cuisine_preferences}</p>
          </div>
        )}
      </div>

      {data.dietary_notes && (
        <div className="mb-4 p-3 bg-orange-50 border border-orange-100 rounded-lg">
          <p className="text-sm text-orange-700">{data.dietary_notes}</p>
        </div>
      )}

      {data.top_restaurant_picks && data.top_restaurant_picks.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-600 mb-2">Top Restaurant Picks</h3>
          <ul className="space-y-2">
            {data.top_restaurant_picks.map((r, i) => (
              <li key={i} className="flex items-center gap-2">
                <span className="w-6 h-6 bg-orange-100 text-orange-600 rounded-full flex items-center justify-center text-xs font-bold">
                  {i + 1}
                </span>
                <span className="text-gray-700">{typeof r === 'string' ? r : r.name || JSON.stringify(r)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
