export default function Accommodation({ data }) {
  if (!data) return null

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <h2 className="text-xl font-bold text-purple-700 mb-4">Accommodation</h2>
      <div className="space-y-3">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">{data.hotel_name || 'N/A'}</h3>
            {data.address && <p className="text-sm text-gray-500">{data.address}</p>}
          </div>
          {data.rating && (
            <span className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-sm font-semibold">
              {data.rating} / 5
            </span>
          )}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-3 border-t border-gray-100">
          {data.check_in && (
            <div>
              <p className="text-xs text-gray-500">Check-in</p>
              <p className="font-medium">{data.check_in}</p>
            </div>
          )}
          {data.check_out && (
            <div>
              <p className="text-xs text-gray-500">Check-out</p>
              <p className="font-medium">{data.check_out}</p>
            </div>
          )}
          {data.room_configuration && (
            <div>
              <p className="text-xs text-gray-500">Rooms</p>
              <p className="font-medium">{data.room_configuration}</p>
            </div>
          )}
          {data.estimated_total_cost && (
            <div>
              <p className="text-xs text-gray-500">Estimated Total</p>
              <p className="font-semibold text-green-600">{data.estimated_total_cost}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
