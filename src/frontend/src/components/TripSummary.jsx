export default function TripSummary({ data }) {
  if (!data) return null

  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-xl p-6 text-white shadow-lg">
      <h2 className="text-2xl font-bold mb-4">Trip Summary</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div>
          <p className="text-blue-200 text-sm">Destination</p>
          <p className="font-semibold text-lg">{data.destination || 'N/A'}</p>
        </div>
        <div>
          <p className="text-blue-200 text-sm">Duration</p>
          <p className="font-semibold text-lg">{data.days || 'N/A'} days</p>
        </div>
        <div>
          <p className="text-blue-200 text-sm">Group Size</p>
          <p className="font-semibold text-lg">{data.group_size || 'N/A'} travelers</p>
        </div>
        <div>
          <p className="text-blue-200 text-sm">Budget</p>
          <p className="font-semibold text-lg">{data.total_budget || 'N/A'}</p>
        </div>
      </div>
      {data.highlights && data.highlights.length > 0 && (
        <div className="mt-4 pt-4 border-t border-blue-400">
          <p className="text-blue-200 text-sm mb-2">Highlights</p>
          <div className="flex flex-wrap gap-2">
            {data.highlights.map((h, i) => (
              <span key={i} className="bg-blue-500/50 px-3 py-1 rounded-full text-sm">{h}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
