'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface DashboardSummary {
  total_sets: number
  total_cards: number
  total_study_sessions: number
  total_study_time_minutes: number
  mastered_cards: number
  struggling_cards: number
  completion_percentage: number
}

interface ActivityItem {
  id: number
  type: string
  timestamp: string
  details: Record<string, string>
}

export default function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [recentActivity, setRecentActivity] = useState<ActivityItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchDashboardData = async () => {
      setIsLoading(true)
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          throw new Error('Not authenticated')
        }

        // Fetch summary data
        const summaryResponse = await fetch('/api/dashboard/summary', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!summaryResponse.ok) {
          throw new Error('Failed to fetch dashboard summary')
        }

        const summaryData = await summaryResponse.json()
        setSummary(summaryData)

        // Fetch recent activity
        const activityResponse = await fetch('/api/dashboard/activity', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!activityResponse.ok) {
          throw new Error('Failed to fetch recent activity')
        }

        const activityData = await activityResponse.json()
        setRecentActivity(activityData)
      } catch (err: any) {
        setError(err.message || 'An error occurred')
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  // Mock data for development without backend
  const mockSummary: DashboardSummary = {
    total_sets: 5,
    total_cards: 120,
    total_study_sessions: 15,
    total_study_time_minutes: 180,
    mastered_cards: 45,
    struggling_cards: 12,
    completion_percentage: 37.5
  }

  const mockActivity: ActivityItem[] = [
    {
      id: 1,
      type: 'study_session',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
      details: {
        set_id: '3',
        set_title: 'Biology Basics',
        duration: '25 minutes',
        status: 'Completed'
      }
    },
    {
      id: 2,
      type: 'flashcard_set_created',
      timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
      details: {
        set_id: '4',
        title: 'Chemistry Formulas',
        card_count: '15'
      }
    }
  ]

  // Use mock data if real data is not available
  const displaySummary = summary || mockSummary
  const displayActivity = recentActivity.length > 0 ? recentActivity : mockActivity

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
      </div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {error && (
          <div className="mt-6 rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {isLoading ? (
          <div className="mt-6 text-center">
            <p className="text-gray-500">Loading dashboard data...</p>
          </div>
        ) : (
          <>
            {/* Summary Cards */}
            <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-primary-100 rounded-md p-3">
                      <svg className="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          Flashcard Sets
                        </dt>
                        <dd>
                          <div className="text-lg font-medium text-gray-900">
                            {displaySummary.total_sets}
                          </div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
                <div className="bg-gray-50 px-4 py-4 sm:px-6">
                  <div className="text-sm">
                    <Link href="/dashboard/sets" className="font-medium text-primary-600 hover:text-primary-500">
                      View all sets
                    </Link>
                  </div>
                </div>
              </div>

              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-primary-100 rounded-md p-3">
                      <svg className="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          Total Flashcards
                        </dt>
                        <dd>
                          <div className="text-lg font-medium text-gray-900">
                            {displaySummary.total_cards}
                          </div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
                <div className="bg-gray-50 px-4 py-4 sm:px-6">
                  <div className="text-sm">
                    <Link href="/dashboard/study" className="font-medium text-primary-600 hover:text-primary-500">
                      Start studying
                    </Link>
                  </div>
                </div>
              </div>

              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-primary-100 rounded-md p-3">
                      <svg className="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          Study Progress
                        </dt>
                        <dd>
                          <div className="text-lg font-medium text-gray-900">
                            {displaySummary.completion_percentage.toFixed(1)}%
                          </div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
                <div className="bg-gray-50 px-4 py-4 sm:px-6">
                  <div className="text-sm">
                    <Link href="/dashboard/stats" className="font-medium text-primary-600 hover:text-primary-500">
                      View statistics
                    </Link>
                  </div>
                </div>
              </div>
            </div>

            {/* Progress Section */}
            <div className="mt-8">
              <h2 className="text-lg leading-6 font-medium text-gray-900">Learning Progress</h2>
              <div className="mt-2 grid grid-cols-1 gap-5 sm:grid-cols-2">
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-base font-medium text-gray-900">Mastered Cards</h3>
                    <div className="mt-1 flex items-baseline justify-between md:block lg:flex">
                      <div className="flex items-baseline text-2xl font-semibold text-primary-600">
                        {displaySummary.mastered_cards}
                        <span className="ml-2 text-sm font-medium text-gray-500">
                          of {displaySummary.total_cards} cards
                        </span>
                      </div>
                      <div className="mt-4">
                        <div className="bg-gray-200 rounded-full h-2.5 w-full">
                          <div 
                            className="bg-primary-600 h-2.5 rounded-full" 
                            style={{ width: `${(displaySummary.mastered_cards / displaySummary.total_cards) * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-base font-medium text-gray-900">Study Time</h3>
                    <div className="mt-1 flex items-baseline justify-between md:block lg:flex">
                      <div className="flex items-baseline text-2xl font-semibold text-primary-600">
                        {displaySummary.total_study_time_minutes.toFixed(0)}
                        <span className="ml-2 text-sm font-medium text-gray-500">minutes</span>
                      </div>
                      <div className="mt-4">
                        <div className="text-sm text-gray-500">
                          {displaySummary.total_study_sessions} study sessions
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="mt-8">
              <h2 className="text-lg leading-6 font-medium text-gray-900">Recent Activity</h2>
              <div className="mt-2 bg-white shadow overflow-hidden sm:rounded-md">
                <ul role="list" className="divide-y divide-gray-200">
                  {displayActivity.map((activity) => (
                    <li key={activity.id}>
                      <div className="px-4 py-4 sm:px-6">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center">
                            <div className={`flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center ${
                              activity.type === 'study_session' 
                                ? 'bg-green-100' 
                                : activity.type === 'flashcard_set_created'
                                ? 'bg-blue-100'
                                : 'bg-purple-100'
                            }`}>
                              {activity.type === 'study_session' && (
                                <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                                </svg>
                              )}
                              {activity.type === 'flashcard_set_created' && (
                                <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                                </svg>
                              )}
                              {activity.type === 'flashcard_progress' && (
                                <svg className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                              )}
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-gray-900">
                                {activity.type === 'study_session' && `Studied "${activity.details.set_title}"`}
                                {activity.type === 'flashcard_set_created' && `Created "${activity.details.title}" set`}
                                {activity.type === 'flashcard_progress' && `Practiced flashcard in "${activity.details.set_title}"`}
                              </div>
                              <div className="text-sm text-gray-500">
                                {activity.type === 'study_session' && `Duration: ${activity.details.duration}`}
                                {activity.type === 'flashcard_set_created' && `Cards: ${activity.details.card_count}`}
                                {activity.type === 'flashcard_progress' && `Result: ${activity.details.result} (${activity.details.difficulty})`}
                              </div>
                            </div>
                          </div>
                          <div className="ml-2 flex-shrink-0 flex">
                            <div className="text-sm text-gray-500">
                              {new Date(activity.timestamp).toLocaleDateString()} at {new Date(activity.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </div>
                          </div>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="mt-8">
              <h2 className="text-lg leading-6 font-medium text-gray-900">Quick Actions</h2>
              <div className="mt-2 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <div className="relative rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500">
                  <div className="flex-shrink-0">
                    <svg className="h-10 w-10 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <Link href="/dashboard/sets/new" className="focus:outline-none">
                      <span className="absolute inset-0" aria-hidden="true" />
                      <p className="text-sm font-medium text-gray-900">Create New Set</p>
                      <p className="text-sm text-gray-500 truncate">Add a new flashcard set</p>
                    </Link>
                  </div>
                </div>

                <div className="relative rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500">
                  <div className="flex-shrink-0">
                    <svg className="h-10 w-10 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <Link href="/dashboard/upload" className="focus:outline-none">
                      <span className="absolute inset-0" aria-hidden="true" />
                      <p className="text-sm font-medium text-gray-900">Upload Document</p>
                      <p className="text-sm text-gray-500 truncate">Generate flashcards from a document</p>
                    </Link>
                  </div>
                </div>

                <div className="relative rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500">
                  <div className="flex-shrink-0">
                    <svg className="h-10 w-10 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <Link href="/dashboard/study" className="focus:outline-none">
                      <span className="absolute inset-0" aria-hidden="true" />
                      <p className="text-sm font-medium text-gray-900">Start Studying</p>
                      <p className="text-sm text-gray-500 truncate">Begin a new study session</p>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
