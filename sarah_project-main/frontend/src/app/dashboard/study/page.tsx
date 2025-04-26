'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { flashcardSetsAPI, flashcardsAPI, studyAPI } from '@/services/api'

interface FlashcardSet {
  id: number
  title: string
  description: string | null
  created_at: string
  updated_at: string
  total_cards?: number
}

export default function StudyPage() {
  const router = useRouter()
  const [sets, setSets] = useState<FlashcardSet[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedSetId, setSelectedSetId] = useState<number | null>(null)
  const [startingSession, setStartingSession] = useState(false)

  // Fetch flashcard sets with card counts
  useEffect(() => {
    const fetchSets = async () => {
      setIsLoading(true)
      try {
        // Get all sets
        const response = await flashcardSetsAPI.getAllSets()
        const setsData = response.data

        // For each set, get the cards to count them
        const setsWithCardCounts = await Promise.all(setsData.map(async (set) => {
          try {
            const cardsResponse = await flashcardsAPI.getCardsBySetId(set.id)
            return {
              ...set,
              total_cards: cardsResponse.data.length
            }
          } catch (error) {
            console.error(`Error fetching cards for set ${set.id}:`, error)
            return {
              ...set,
              total_cards: 0
            }
          }
        }))

        setSets(setsWithCardCounts)
      } catch (err: any) {
        setError(err.message || 'Failed to load flashcard sets')
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchSets()
  }, [])

  // Start a study session
  const startStudySession = async () => {
    if (!selectedSetId) {
      setError('Please select a flashcard set to study')
      return
    }

    try {
      setStartingSession(true)
      const response = await studyAPI.startSession(selectedSetId)
      router.push(`/dashboard/study/session/${response.data.id}`)
    } catch (err: any) {
      setError(err.message || 'Failed to start study session')
      console.error(err)
      setStartingSession(false)
    }
  }

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-semibold text-gray-900">Study</h1>
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

        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Start a Study Session</h3>
            <div className="mt-2 max-w-xl text-sm text-gray-500">
              <p>Select a flashcard set to study and improve your knowledge.</p>
            </div>

            {isLoading ? (
              <div className="mt-5 text-center py-4">
                <svg className="mx-auto h-8 w-8 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p className="mt-2 text-sm text-gray-500">Loading flashcard sets...</p>
              </div>
            ) : sets.length === 0 ? (
              <div className="mt-5 text-center py-4">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No flashcard sets</h3>
                <p className="mt-1 text-sm text-gray-500">Create a flashcard set before starting a study session.</p>
                <div className="mt-6">
                  <button
                    onClick={() => router.push('/dashboard/sets')}
                    className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Create Flashcard Set
                  </button>
                </div>
              </div>
            ) : (
              <div className="mt-5">
                <label htmlFor="set-select" className="block text-sm font-medium text-gray-700">
                  Flashcard Set
                </label>
                <select
                  id="set-select"
                  name="set-select"
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
                  value={selectedSetId || ''}
                  onChange={(e) => setSelectedSetId(e.target.value ? parseInt(e.target.value) : null)}
                >
                  <option value="">Select a flashcard set</option>
                  {sets.map((set) => (
                    <option key={set.id} value={set.id} disabled={set.total_cards === 0}>
                      {set.title} {set.total_cards > 0 ? `(${set.total_cards} cards)` : '(empty)'}
                    </option>
                  ))}
                </select>

                <div className="mt-5">
                  <button
                    type="button"
                    onClick={startStudySession}
                    disabled={!selectedSetId || startingSession}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
                  >
                    {startingSession ? 'Starting Session...' : 'Start Study Session'}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="mt-6 bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Study Tips</h3>
            <div className="mt-2 max-w-xl text-sm text-gray-500">
              <ul className="list-disc pl-5 space-y-2">
                <li>Study regularly for shorter periods rather than cramming</li>
                <li>Rate each card based on how well you know it</li>
                <li>Focus more on cards you find difficult</li>
                <li>Review cards you've mastered periodically to maintain knowledge</li>
                <li>Create clear, concise flashcards for better retention</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
