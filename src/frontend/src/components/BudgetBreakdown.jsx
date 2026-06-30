export default function BudgetBreakdown({ data }) {
  if (!data) return null

  const items = [
    { label: 'Accommodation', value: data.accommodation_cost },
    { label: 'Meals', value: data.meal_cost },
    { label: 'Activities', value: data.activity_cost },
    { label: 'Transportation', value: data.transportation_cost },
    { label: 'Miscellaneous', value: data.miscellaneous },
  ].filter(item => item.value)

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <h2 className="text-xl font-bold text-green-700 mb-4">Budget Breakdown</h2>
      <div className="space-y-3">
        {items.map((item, i) => (
          <div key={i} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
            <span className="text-gray-600">{item.label}</span>
            <span className="font-semibold text-gray-800">{item.value}</span>
          </div>
        ))}
        {data.total_estimated_cost && (
          <div className="flex items-center justify-between pt-3 mt-3 border-t-2 border-green-200">
            <span className="font-bold text-gray-800 text-lg">Total Estimated Cost</span>
            <span className="font-bold text-green-700 text-lg">{data.total_estimated_cost}</span>
          </div>
        )}
      </div>
    </div>
  )
}
