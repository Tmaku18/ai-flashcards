'use client'

import { useState, useEffect } from 'react'
import { dashboardAPI } from '@/services/api'

interface SetStatistics {
  set_id: number
  title: string
  total_cards: number
  mastery_percentage: number
  last_studied: string | null
  study_count: number
  average_session_minutes: number | null
}

interface TimePoint {
  date: string
  minutes: number
}

interface StudyTimeDistribution {
  daily: TimePoint[]
  weekly: TimePoint[]
  monthly: TimePoint[]
}

export default function StatisticsPage() {
  const [setStats, setSetStats] = useState<SetStatistics[]>([])
  const [timeDistribution, setTimeDistribution] = useState<StudyTimeDistribution | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  // Fetch statistics data
  useEffect(() => {
    const fetchStatistics = async () => {
      setIsLoading(true)
      try {
        // Get set statistics
        const setStatsResponse = await dashboardAPI.getSetStatistics()
        setSetStats(setStatsResponse.data)
        
        // Get study time distribution
        const timeDistResponse = await dashboardAPI.getStudyTimeDistribution()
        setTimeDistribution(timeDistResponse.data)
      } catch (err: any) {
        setError(err.message || 'Failed to load statistics')
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchStatistics()
  }, [])

  // Format date for display
  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never'
    return new Date(dateString).toLocaleDateString()
  }

  // Calculate total study time
  const calculateTotalStudyTime = () => {
    if (!timeDistribution) return 0
    
    return timeDistribution.daily.reduce((total, point) => total + point.minutes, 0)
  }

  // Get most studied set
  const getMostStudiedSet = () => {
    if (!setStats.length) return null
    
    return setStats.reduce((prev, current) => 
      (prev.study_count > current.study_count) ? prev : current
    )
  }

  // Get highest mastery set
  const getHighestMasterySet = () => {
    if (!setStats.length) return null
    
    return setStats.reduce((prev, current) => 
      (prev.mastery_percentage > current.mastery_percentage) ? prev : current
    )
  }

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-semibold text-gray-900">Statistics</h1>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        {error && (
          <div className="rounded-md bg-red-50 p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
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
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="mt-2 text-sm text-gray-500">Loading statistics...</p>
          </div>
        ) : (
          <>
            {/* Summary Cards */}
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Study Time
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-gray-900">
                    {calculateTotalStudyTime().toFixed(0)} min
                  </dd>
                </div>
              </div>
              
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Flashcard Sets
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-gray-900">
                    {setStats.length}
                  </dd>
                </div>
              </div>
              
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Cards
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-gray-900">
                    {setStats.reduce((total, set) => total + set.total_cards, 0)}
                  </dd>
                </div>
              </div>
              
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Average Mastery
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-gray-900">
                    {setStats.length 
                      ? (setStats.reduce((total, set) => total + set.mastery_percentage, 0) / setStats.length).toFixed(1)
                      : 0}%
                  </dd>
                </div>
              </div>
            </div>

            {/* Study Time Distribution */}
            <div className="mt-6 bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">Study Time Distribution</h3>
                <p className="mt-1 max-w-2xl text-sm text-gray-500">Daily study time for the past week</p>
              </div>
              <div className="px-4 py-5 sm:p-6">
                {timeDistribution && timeDistribution.daily.length > 0 ? (
                  <div className="h-64 flex items-end space-x-2">
                    {timeDistribution.daily.map((point, index) => (
                      <div key={index} className="flex-1 flex flex-col items-center">
                        <div 
                          className="w-full bg-primary-200 rounded-t"
                          style={{ 
                            height: `${Math.max(4, (point.minutes / Math.max(...timeDistribution.daily.map(p => p.minutes))) * 200)}px` 
                          }}
                        ></div>
                        <div className="mt-2 text-xs text-gray-500">
                          {new Date(point.date).toLocaleDateString(undefined, { weekday: 'short' })}
                        </div>
                        <div className="text-xs font-medium text-gray-900">
                          {point.minutes.toFixed(0)} min
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-6 text-gray-500">
                    No study data available yet
                  </div>
                )}
              </div>
            </div>

            {/* Set Statistics */}
            <div className="mt-6 bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">Flashcard Set Statistics</h3>
                <p className="mt-1 max-w-2xl text-sm text-gray-500">Performance metrics for each set</p>
              </div>
              <div className="border-t border-gray-200">
                {setStats.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Set Name
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Cards
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Mastery
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Study Sessions
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Last Studied
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {setStats.map((set) => (
                          <tr key={set.set_id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                              {set.title}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {set.total_cards}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center">
                                <div className="w-full bg-gray-200 rounded-full h-2.5">
                                  <div 
                                    className="bg-primary-600 h-2.5 rounded-full" 
                                    style={{ width: `${set.mastery_percentage}%` }}
                                  ></div>
                                </div>
                                <span className="ml-2 text-sm text-gray-500">{set.mastery_percentage.toFixed(1)}%</span>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {set.study_count}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {formatDate(set.last_studied)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="text-center py-6 text-gray-500">
                    No flashcard sets available yet
                  </div>
                )}
              </div>
            </div>

            {/* Insights */}
            <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2">
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Most Studied Set</h3>
                  {getMostStudiedSet() ? (
                    <div className="mt-2">
                      <p className="text-xl font-semibold text-gray-900">{getMostStudiedSet()?.title}</p>
                      <p className="text-sm text-gray-500">
                        Studied {getMostStudiedSet()?.study_count} times
                      </p>
                    </div>
                  ) : (
                    <p className="mt-2 text-sm text-gray-500">No study data available yet</p>
                  )}
                </div>
              </div>
              
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Highest Mastery</h3>
                  {getHighestMasterySet() && getHighestMasterySet()?.mastery_percentage > 0 ? (
                    <div className="mt-2">
                      <p className="text-xl font-semibold text-gray-900">{getHighestMasterySet()?.title}</p>
                      <p className="text-sm text-gray-500">
                        {getHighestMasterySet()?.mastery_percentage.toFixed(1)}% mastery
                      </p>
                    </div>
                  ) : (
                    <p className="mt-2 text-sm text-gray-500">No mastery data available yet</p>
                  )}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
