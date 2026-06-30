export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
      <p className="mt-6 text-lg text-gray-600 font-medium">Generating your travel plan...</p>
      <p className="mt-2 text-sm text-gray-400">Our AI agents are researching the best options for you. This may take a few minutes.</p>
    </div>
  )
}
