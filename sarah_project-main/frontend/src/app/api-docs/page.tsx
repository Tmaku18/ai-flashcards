'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function ApiDocsPage() {
  const router = useRouter()

  useEffect(() => {
    // Redirect to the Swagger UI docs
    window.location.href = '/api/docs'
  }, [])

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8 text-center">
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
          API Documentation
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Redirecting to API documentation...
        </p>
        <div className="mt-5">
          <button
            onClick={() => window.location.href = '/api/docs'}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Click here if you are not redirected
          </button>
        </div>
      </div>
    </div>
  )
}
