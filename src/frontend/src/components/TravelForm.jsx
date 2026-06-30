import { useState } from 'react'

const initialForm = {
  location: '',
  days: 3,
  group_size: 2,
  total_budget: '',
  restaurant_preference: '',
  dietary_restrictions: 'None',
  meal_budget_per_day: '',
  hotel_preference: '',
  interests: '',
  intensity: 'moderate',
  events: '',
  schedule_style: 'balanced',
}

export default function TravelForm({ onSubmit, isLoading }) {
  const [form, setForm] = useState(initialForm)

  function handleChange(e) {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  function handleSubmit(e) {
    e.preventDefault()
    onSubmit({
      ...form,
      days: Number(form.days),
      group_size: Number(form.group_size),
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* Trip Basics */}
      <fieldset className="border border-gray-200 rounded-xl p-6 bg-white shadow-sm">
        <legend className="text-lg font-semibold text-blue-700 px-2">Trip Basics</legend>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
            <input
              type="text"
              name="location"
              value={form.location}
              onChange={handleChange}
              placeholder="e.g. Bolinao, Pangasinan, Philippines"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Days of Travel</label>
            <input
              type="number"
              name="days"
              value={form.days}
              onChange={handleChange}
              min="1"
              max="30"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Group Size</label>
            <input
              type="number"
              name="group_size"
              value={form.group_size}
              onChange={handleChange}
              min="1"
              max="50"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Total Budget</label>
            <input
              type="text"
              name="total_budget"
              value={form.total_budget}
              onChange={handleChange}
              placeholder="e.g. $1500 - $2000"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </fieldset>

      {/* Dining Preferences */}
      <fieldset className="border border-gray-200 rounded-xl p-6 bg-white shadow-sm">
        <legend className="text-lg font-semibold text-orange-600 px-2">Dining Preferences</legend>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Cuisine Preference</label>
            <input
              type="text"
              name="restaurant_preference"
              value={form.restaurant_preference}
              onChange={handleChange}
              placeholder="e.g. Filipino cuisine, seafood"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Dietary Restrictions</label>
            <input
              type="text"
              name="dietary_restrictions"
              value={form.dietary_restrictions}
              onChange={handleChange}
              placeholder="e.g. Vegetarian, Gluten-free, or None"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Meal Budget Per Day</label>
            <input
              type="text"
              name="meal_budget_per_day"
              value={form.meal_budget_per_day}
              onChange={handleChange}
              placeholder="e.g. $50"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>
        </div>
      </fieldset>

      {/* Accommodation */}
      <fieldset className="border border-gray-200 rounded-xl p-6 bg-white shadow-sm">
        <legend className="text-lg font-semibold text-purple-600 px-2">Accommodation</legend>
        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Hotel Preference</label>
          <input
            type="text"
            name="hotel_preference"
            value={form.hotel_preference}
            onChange={handleChange}
            placeholder="e.g. beachfront resort, mid-range"
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>
      </fieldset>

      {/* Activities & Itinerary */}
      <fieldset className="border border-gray-200 rounded-xl p-6 bg-white shadow-sm">
        <legend className="text-lg font-semibold text-green-600 px-2">Activities & Itinerary</legend>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Interests</label>
            <input
              type="text"
              name="interests"
              value={form.interests}
              onChange={handleChange}
              placeholder="e.g. beaches, snorkeling, historical sites, nature"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Intensity Level</label>
            <select
              name="intensity"
              value={form.intensity}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="light">Light - Relaxed pace</option>
              <option value="moderate">Moderate - Balanced</option>
              <option value="intense">Intense - Action-packed</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Schedule Style</label>
            <select
              name="schedule_style"
              value={form.schedule_style}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="relaxed">Relaxed - Lots of free time</option>
              <option value="balanced">Balanced - Mix of plans and freedom</option>
              <option value="packed">Packed - Maximize every moment</option>
            </select>
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Events of Interest</label>
            <input
              type="text"
              name="events"
              value={form.events}
              onChange={handleChange}
              placeholder="e.g. local festivals, cultural events, concerts"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
        </div>
      </fieldset>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-xl shadow-lg transition-colors text-lg cursor-pointer disabled:cursor-not-allowed"
      >
        {isLoading ? 'Generating Plan...' : 'Generate Travel Plan'}
      </button>
    </form>
  )
}
