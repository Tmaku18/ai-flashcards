'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { studyAPI, flashcardsAPI, flashcardSetsAPI } from '@/services/api'

interface Flashcard {
  id: number
  question: string
  answer: string
  created_at: string
}

interface StudySession {
  id: number
  set_id: number
  user_id: number
  start_time: string
  end_time: string | null
}

interface FlashcardSet {
  id: number
  title: string
}

export default function StudySessionPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const sessionId = parseInt(params.id)

  const [session, setSession] = useState<StudySession | null>(null)
  const [set, setSet] = useState<FlashcardSet | null>(null)
  const [cards, setCards] = useState<Flashcard[]>([])
  const [currentCardIndex, setCurrentCardIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [endingSession, setEndingSession] = useState(false)
  const [studyComplete, setStudyComplete] = useState(false)

  // Track progress
  const [studiedCards, setStudiedCards] = useState<Set<number>>(new Set())
  const [startTime, setStartTime] = useState<Date | null>(null)

  // Fetch session data
  useEffect(() => {
    const fetchSessionData = async () => {
      setIsLoading(true)
      try {
        // Get session details
        const sessionResponse = await studyAPI.getSessionById(sessionId)
        setSession(sessionResponse.data)
        setStartTime(new Date())

        // Get set details
        const setResponse = await flashcardSetsAPI.getSetById(sessionResponse.data.set_id)
        setSet(setResponse.data)

        // Get cards
        const cardsResponse = await flashcardsAPI.getCardsBySetId(sessionResponse.data.set_id)

        if (cardsResponse.data.length === 0) {
          setError('This flashcard set has no cards to study')
          setCards([])
        } else {
          // Shuffle the cards
          const shuffledCards = [...cardsResponse.data].sort(() => Math.random() - 0.5)
          setCards(shuffledCards)
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load study session')
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    }

    if (!isNaN(sessionId)) {
      fetchSessionData()
    } else {
      setError('Invalid session ID')
    }
  }, [sessionId])

  // Handle card flip
  const flipCard = () => {
    setIsFlipped(!isFlipped)
  }

  // Handle difficulty rating
  const rateCard = async (isCorrect: boolean, difficulty: 'easy' | 'medium' | 'hard') => {
    if (!session || !cards.length) return

    const currentCard = cards[currentCardIndex]

    try {
      // Record progress
      await studyAPI.updateProgress(
        sessionId,
        currentCard.id,
        isCorrect,
        difficulty
      )

      // Add to studied cards
      setStudiedCards(prev => {
        const newSet = new Set(prev)
        newSet.add(currentCard.id)
        return newSet
      })

      // Move to next card or end session
      if (currentCardIndex < cards.length - 1) {
        setCurrentCardIndex(currentCardIndex + 1)
        setIsFlipped(false)
      } else {
        setStudyComplete(true)
        endSession()
      }
    } catch (err: any) {
      setError(err.message || 'Failed to record progress')
      console.error(err)
    }
  }

  // End the study session
  const endSession = async () => {
    if (!session) return

    try {
      setEndingSession(true)
      await studyAPI.endSession(sessionId)

      // Don't redirect if we're showing the completion screen
      if (!studyComplete) {
        router.push('/dashboard/study')
      }
    } catch (err: any) {
      setError(err.message || 'Failed to end study session')
      console.error(err)
    } finally {
      setEndingSession(false)
    }
  }

  // Calculate study statistics
  const getStudyStats = () => {
    if (!startTime || !cards.length) return { duration: '0 minutes', cardsStudied: 0 }

    const duration = Math.round((new Date().getTime() - startTime.getTime()) / 60000)
    return {
      duration: `${duration} minute${duration !== 1 ? 's' : ''}`,
      cardsStudied: studiedCards.size
    }
  }

  if (isLoading && !session) {
    return (
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="mt-2 text-sm text-gray-500">Loading study session...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error && !session) {
    return (
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="rounded-md bg-red-50 p-4">
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
          <div className="mt-6">
            <button
              onClick={() => router.push('/dashboard/study')}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Back to Study
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (studyComplete) {
    const stats = getStudyStats()

    return (
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6 text-center">
              <svg className="mx-auto h-12 w-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="mt-2 text-lg font-medium text-gray-900">Study Session Complete!</h3>
              <div className="mt-3 text-sm text-gray-500">
                <p>You've completed your study session for {set?.title}.</p>
              </div>

              <div className="mt-6 border-t border-b border-gray-200 py-6">
                <dl className="grid grid-cols-2 gap-x-4 gap-y-8">
                  <div className="col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Cards Studied</dt>
                    <dd className="mt-1 text-2xl font-semibold text-gray-900">{stats.cardsStudied}</dd>
                  </div>
                  <div className="col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Duration</dt>
                    <dd className="mt-1 text-2xl font-semibold text-gray-900">{stats.duration}</dd>
                  </div>
                </dl>
              </div>

              <div className="mt-6">
                <button
                  onClick={() => router.push('/dashboard/study')}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Back to Study
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!cards.length) {
    return (
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6 text-center">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 className="mt-2 text-lg font-medium text-gray-900">No Flashcards</h3>
              <div className="mt-3 text-sm text-gray-500">
                <p>This flashcard set doesn't have any cards to study.</p>
              </div>
              <div className="mt-6">
                <button
                  onClick={() => router.push('/dashboard/study')}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Back to Study
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const currentCard = cards[currentCardIndex]
  const progress = Math.round((currentCardIndex / cards.length) * 100)

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-semibold text-gray-900">Studying: {set?.title}</h1>
          <button
            onClick={endSession}
            disabled={endingSession}
            className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            {endingSession ? 'Ending...' : 'End Session'}
          </button>
        </div>
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
            {/* Progress bar */}
            <div className="w-full bg-gray-200 rounded-full h-2.5 mb-6">
              <div
                className="bg-primary-600 h-2.5 rounded-full"
                style={{ width: `${progress}%` }}
              ></div>
            </div>

            <div className="text-sm text-gray-500 mb-4">
              Card {currentCardIndex + 1} of {cards.length}
            </div>

            {/* Flashcard */}
            <div
              className="border rounded-lg shadow-lg p-6 min-h-[200px] flex items-center justify-center cursor-pointer transition-all duration-300 transform hover:shadow-xl"
              onClick={flipCard}
            >
              <div className="text-center">
                <div className="text-xl font-medium text-gray-900 whitespace-pre-wrap">
                  {isFlipped ? currentCard.answer : currentCard.question}
                </div>
                <div className="mt-4 text-sm text-gray-500">
                  {isFlipped ? 'Answer (click to flip)' : 'Question (click to flip)'}
                </div>
              </div>
            </div>

            {/* Rating buttons - only show when card is flipped */}
            {isFlipped && (
              <div className="mt-6">
                <div className="text-sm font-medium text-gray-700 mb-2">
                  How well did you know this?
                </div>
                <div className="flex space-x-4">
                  <button
                    onClick={() => rateCard(false, 'hard')}
                    className="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    Didn't Know
                  </button>
                  <button
                    onClick={() => rateCard(true, 'medium')}
                    className="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-yellow-500 hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500"
                  >
                    Somewhat Knew
                  </button>
                  <button
                    onClick={() => rateCard(true, 'easy')}
                    className="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  >
                    Knew Well
                  </button>
                </div>
              </div>
            )}

            {/* Navigation buttons */}
            <div className="mt-6 flex justify-between">
              <button
                onClick={() => {
                  if (currentCardIndex > 0) {
                    setCurrentCardIndex(currentCardIndex - 1)
                    setIsFlipped(false)
                  }
                }}
                disabled={currentCardIndex === 0}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                onClick={() => {
                  if (currentCardIndex < cards.length - 1) {
                    setCurrentCardIndex(currentCardIndex + 1)
                    setIsFlipped(false)
                  }
                }}
                disabled={currentCardIndex === cards.length - 1}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Skip
              </button>
            </div>
          </div>
        </div>

        <div className="mt-6 bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Keyboard Shortcuts</h3>
            <div className="mt-2 max-w-xl text-sm text-gray-500">
              <ul className="grid grid-cols-2 gap-x-4 gap-y-2">
                <li className="flex items-center">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded text-xs mr-2">Space</span>
                  <span>Flip card</span>
                </li>
                <li className="flex items-center">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded text-xs mr-2">→</span>
                  <span>Next card</span>
                </li>
                <li className="flex items-center">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded text-xs mr-2">←</span>
                  <span>Previous card</span>
                </li>
                <li className="flex items-center">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded text-xs mr-2">1</span>
                  <span>Didn't know</span>
                </li>
                <li className="flex items-center">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded text-xs mr-2">2</span>
                  <span>Somewhat knew</span>
                </li>
                <li className="flex items-center">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded text-xs mr-2">3</span>
                  <span>Knew well</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
