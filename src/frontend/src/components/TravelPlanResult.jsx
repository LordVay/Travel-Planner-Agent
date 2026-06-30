import TripSummary from './TripSummary'
import DailyPlan from './DailyPlan'
import Accommodation from './Accommodation'
import DiningPlan from './DiningPlan'
import BudgetBreakdown from './BudgetBreakdown'

export default function TravelPlanResult({ data }) {
  if (!data) return null

  return (
    <div className="space-y-6">
      <TripSummary data={data.trip_summary} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Accommodation data={data.accommodation} />
        <DiningPlan data={data.dining_plan} />
      </div>

      <BudgetBreakdown data={data.budget_breakdown} />

      <DailyPlan data={data.daily_plan} />

      {/* Packing Tips & Safety */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {data.packing_tips && data.packing_tips.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-bold text-teal-700 mb-4">Packing Tips</h2>
            <ul className="space-y-2">
              {data.packing_tips.map((tip, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-teal-500 mt-0.5">•</span>
                  <span className="text-gray-700">{tip}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {data.safety_advice && (
          <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-bold text-red-600 mb-4">Safety & Travel Tips</h2>
            <p className="text-gray-700 whitespace-pre-line">{data.safety_advice}</p>
          </div>
        )}
      </div>
    </div>
  )
}
