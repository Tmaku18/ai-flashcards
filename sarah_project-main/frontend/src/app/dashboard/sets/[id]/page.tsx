'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { flashcardSetsAPI, flashcardsAPI } from '@/services/api'

interface Flashcard {
  id: number
  question: string
  answer: string
  created_at: string
}

interface FlashcardSet {
  id: number
  title: string
  description: string | null
  created_at: string
  updated_at: string
  flashcards: Flashcard[]
}

export default function FlashcardSetDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const setId = parseInt(params.id)

  const [set, setSet] = useState<FlashcardSet | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [showAddCard, setShowAddCard] = useState(false)
  const [newQuestion, setNewQuestion] = useState('')
  const [newAnswer, setNewAnswer] = useState('')
  const [activeCard, setActiveCard] = useState<number | null>(null)
  const [flippedCards, setFlippedCards] = useState<Set<number>>(new Set())

  // Fetch flashcard set details
  useEffect(() => {
    const fetchSetDetails = async () => {
      setIsLoading(true)
      try {
        const response = await flashcardSetsAPI.getSetById(setId)
        setSet(response.data)
      } catch (err: any) {
        setError(err.message || 'Failed to load flashcard set')
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    }

    if (!isNaN(setId)) {
      fetchSetDetails()
    } else {
      setError('Invalid set ID')
    }
  }, [setId])

  // Handle creating a new card
  const handleAddCard = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!newQuestion.trim() || !newAnswer.trim()) {
      setError('Question and answer are required')
      return
    }

    try {
      setIsLoading(true)
      const response = await flashcardsAPI.createCard(setId, {
        question: newQuestion,
        answer: newAnswer
      })

      // Add the new card to the set
      setSet(prev => {
        if (!prev) return prev
        return {
          ...prev,
          flashcards: [...prev.flashcards, response.data]
        }
      })

      // Reset form
      setNewQuestion('')
      setNewAnswer('')
      setShowAddCard(false)
      setError('')

      // Show success message and clear any error
      setError('')
      setSuccessMessage('Card added successfully. Please refresh the study page if you want to study this set.')

      // Clear success message after 5 seconds
      setTimeout(() => {
        setSuccessMessage('')
      }, 5000)
    } catch (err: any) {
      setError(err.message || 'Failed to create flashcard')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  // Handle deleting a card
  const handleDeleteCard = async (cardId: number) => {
    if (!confirm('Are you sure you want to delete this flashcard?')) {
      return
    }

    try {
      setIsLoading(true)
      await flashcardsAPI.deleteCard(setId, cardId)

      // Remove the deleted card from the set
      setSet(prev => {
        if (!prev) return prev
        return {
          ...prev,
          flashcards: prev.flashcards.filter(card => card.id !== cardId)
        }
      })
    } catch (err: any) {
      setError(err.message || 'Failed to delete flashcard')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  // Toggle card flip
  const toggleCardFlip = (cardId: number) => {
    setFlippedCards(prev => {
      const newFlipped = new Set(prev)
      if (newFlipped.has(cardId)) {
        newFlipped.delete(cardId)
      } else {
        newFlipped.add(cardId)
      }
      return newFlipped
    })
  }

  // Start a study session
  const startStudySession = async () => {
    if (!set || set.flashcards.length === 0) {
      setError('Cannot study an empty flashcard set')
      return
    }

    router.push(`/dashboard/study/session/${setId}`)
  }

  if (isLoading && !set) {
    return (
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="mt-2 text-sm text-gray-500">Loading flashcard set...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error && !set) {
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
              onClick={() => router.push('/dashboard/sets')}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Back to Sets
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-semibold text-gray-900">{set?.title}</h1>
          <div className="flex space-x-4">
            <button
              onClick={() => router.push('/dashboard/sets')}
              className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Back to Sets
            </button>
            <button
              onClick={startStudySession}
              disabled={!set || set.flashcards.length === 0}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              Study Now
            </button>
          </div>
        </div>
        {set?.description && (
          <p className="mt-2 text-sm text-gray-500">{set.description}</p>
        )}
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

        {successMessage && (
          <div className="rounded-md bg-green-50 p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">Success</h3>
                <div className="mt-2 text-sm text-green-700">
                  <p>{successMessage}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
          <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Flashcards ({set?.flashcards.length || 0})
            </h3>
            <button
              onClick={() => setShowAddCard(!showAddCard)}
              className="inline-flex items-center px-3 py-1.5 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              {showAddCard ? 'Cancel' : 'Add Card'}
            </button>
          </div>

          {showAddCard && (
            <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
              <form onSubmit={handleAddCard} className="space-y-4">
                <div>
                  <label htmlFor="question" className="block text-sm font-medium text-gray-700">
                    Question <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    name="question"
                    id="question"
                    rows={2}
                    value={newQuestion}
                    onChange={(e) => setNewQuestion(e.target.value)}
                    className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="answer" className="block text-sm font-medium text-gray-700">
                    Answer <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    name="answer"
                    id="answer"
                    rows={2}
                    value={newAnswer}
                    onChange={(e) => setNewAnswer(e.target.value)}
                    className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    required
                  />
                </div>
                <div className="flex justify-end">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    {isLoading ? 'Adding...' : 'Add Card'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {set?.flashcards.length === 0 ? (
            <div className="text-center py-12 border-t border-gray-200">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No flashcards</h3>
              <p className="mt-1 text-sm text-gray-500">Get started by adding a new flashcard.</p>
              <div className="mt-6">
                <button
                  onClick={() => setShowAddCard(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  <svg className="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                  </svg>
                  Add Card
                </button>
              </div>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {set?.flashcards.map((card) => (
                <li key={card.id} className="px-4 py-4 sm:px-6">
                  <div
                    className={`bg-white border rounded-lg shadow-sm overflow-hidden cursor-pointer transition-all duration-300 transform ${flippedCards.has(card.id) ? 'scale-[1.02]' : ''}`}
                    onClick={() => toggleCardFlip(card.id)}
                  >
                    <div className="px-4 py-5 sm:p-6">
                      {flippedCards.has(card.id) ? (
                        <div className="text-gray-900 whitespace-pre-wrap">{card.answer}</div>
                      ) : (
                        <div className="text-gray-900 whitespace-pre-wrap">{card.question}</div>
                      )}
                    </div>
                    <div className="bg-gray-50 px-4 py-3 sm:px-6 flex justify-between items-center">
                      <div className="text-xs text-gray-500">
                        {flippedCards.has(card.id) ? 'Answer (click to flip)' : 'Question (click to flip)'}
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteCard(card.id);
                        }}
                        className="text-xs text-red-600 hover:text-red-500"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
