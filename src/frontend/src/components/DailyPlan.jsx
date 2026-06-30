import { useState } from 'react'

function DayCard({ day }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="border border-gray-200 rounded-xl bg-white shadow-sm overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors cursor-pointer"
      >
        <div className="flex items-center gap-3">
          <span className="bg-blue-100 text-blue-700 font-bold w-10 h-10 rounded-full flex items-center justify-center">
            {day.day}
          </span>
          <span className="font-semibold text-gray-800">Day {day.day}</span>
          {day.weather_summary && (
            <span className="text-sm text-gray-500 ml-2">{day.weather_summary}</span>
          )}
        </div>
        <span className="text-gray-400 text-xl">{expanded ? '−' : '+'}</span>
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-4">
          {/* Activities */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {day.morning && (
              <ActivityBlock label="Morning" activity={day.morning} color="yellow" />
            )}
            {day.afternoon && (
              <ActivityBlock label="Afternoon" activity={day.afternoon} color="orange" />
            )}
            {day.evening && (
              <ActivityBlock label="Evening" activity={day.evening} color="indigo" />
            )}
          </div>

          {/* Meals */}
          {day.meals && (
            <div className="mt-4">
              <h4 className="text-sm font-semibold text-gray-600 mb-2">Meals</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {day.meals.breakfast && (
                  <MealBlock label="Breakfast" meal={day.meals.breakfast} />
                )}
                {day.meals.lunch && (
                  <MealBlock label="Lunch" meal={day.meals.lunch} />
                )}
                {day.meals.dinner && (
                  <MealBlock label="Dinner" meal={day.meals.dinner} />
                )}
              </div>
            </div>
          )}

          {/* Notes */}
          {day.notes && (
            <div className="mt-3 p-3 bg-amber-50 border border-amber-200 rounded-lg">
              <p className="text-sm text-amber-800">{day.notes}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function ActivityBlock({ label, activity, color }) {
  return (
    <div className={`p-3 bg-${color}-50 rounded-lg border border-${color}-100`}>
      <p className={`text-xs font-semibold text-${color}-700 uppercase`}>{label}</p>
      <p className="font-medium text-gray-800 mt-1">{activity.activity || activity.name || 'N/A'}</p>
      {activity.location && <p className="text-sm text-gray-500">{activity.location}</p>}
      {activity.estimated_cost && <p className="text-sm text-green-600 mt-1">{activity.estimated_cost}</p>}
    </div>
  )
}

function MealBlock({ label, meal }) {
  return (
    <div className="p-3 bg-gray-50 rounded-lg">
      <p className="text-xs font-semibold text-gray-500 uppercase">{label}</p>
      <p className="font-medium text-gray-800 mt-1">{meal.restaurant_name || 'N/A'}</p>
      {meal.cuisine && <p className="text-sm text-gray-500">{meal.cuisine}</p>}
      {meal.estimated_cost_per_person && (
        <p className="text-sm text-green-600">{meal.estimated_cost_per_person}/person</p>
      )}
    </div>
  )
}

export default function DailyPlan({ data }) {
  if (!data || data.length === 0) return null

  return (
    <div>
      <h2 className="text-xl font-bold text-gray-800 mb-4">Daily Itinerary</h2>
      <div className="space-y-3">
        {data.map((day, i) => (
          <DayCard key={i} day={day} />
        ))}
      </div>
    </div>
  )
}
