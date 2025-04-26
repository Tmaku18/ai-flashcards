'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { flashcardSetsAPI, flashcardsAPI } from '@/services/api'

interface FlashcardSet {
  id: number
  title: string
  description: string | null
  created_at: string
  updated_at: string
  total_cards?: number
}

export default function FlashcardSetsPage() {
  const [sets, setSets] = useState<FlashcardSet[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [isCreating, setIsCreating] = useState(false)
  const [newSetTitle, setNewSetTitle] = useState('')
  const [newSetDescription, setNewSetDescription] = useState('')

  // Fetch flashcard sets with card counts
  useEffect(() => {
    const fetchSets = async () => {
      setIsLoading(true)
      try {
        // Get all sets
        const response = await flashcardSetsAPI.getAllSets()
        const setsData = response.data

        // For each set, get the cards to count them
        const setsWithCardCounts = await Promise.all(setsData.map(async (set: FlashcardSet) => {
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

  // Handle creating a new set
  const handleCreateSet = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!newSetTitle.trim()) {
      setError('Title is required')
      return
    }

    try {
      setIsLoading(true)
      const response = await flashcardSetsAPI.createSet({
        title: newSetTitle,
        description: newSetDescription || undefined
      })

      // Add the new set to the list
      setSets(prev => [...prev, response.data])

      // Reset form
      setNewSetTitle('')
      setNewSetDescription('')
      setIsCreating(false)
      setError('')
    } catch (err: any) {
      setError(err.message || 'Failed to create flashcard set')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  // Handle deleting a set
  const handleDeleteSet = async (setId: number) => {
    if (!confirm('Are you sure you want to delete this flashcard set? This action cannot be undone.')) {
      return
    }

    try {
      setIsLoading(true)
      await flashcardSetsAPI.deleteSet(setId)

      // Remove the deleted set from the list
      setSets(prev => prev.filter(set => set.id !== setId))
    } catch (err: any) {
      setError(err.message || 'Failed to delete flashcard set')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-semibold text-gray-900">Flashcard Sets</h1>
          <button
            onClick={() => setIsCreating(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <svg className="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
            Create Set
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

        {isCreating && (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Create New Flashcard Set</h3>
              <form onSubmit={handleCreateSet} className="mt-5 space-y-4">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                    Title <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="title"
                    id="title"
                    value={newSetTitle}
                    onChange={(e) => setNewSetTitle(e.target.value)}
                    className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                    Description
                  </label>
                  <textarea
                    name="description"
                    id="description"
                    rows={3}
                    value={newSetDescription}
                    onChange={(e) => setNewSetDescription(e.target.value)}
                    className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
                <div className="flex justify-end">
                  <button
                    type="button"
                    onClick={() => {
                      setIsCreating(false)
                      setNewSetTitle('')
                      setNewSetDescription('')
                      setError('')
                    }}
                    className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    {isLoading ? 'Creating...' : 'Create'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {isLoading && !sets.length ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="mt-2 text-sm text-gray-500">Loading flashcard sets...</p>
          </div>
        ) : sets.length === 0 ? (
          <div className="text-center py-12 bg-white shadow overflow-hidden sm:rounded-lg">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No flashcard sets</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by creating a new flashcard set.</p>
            <div className="mt-6">
              <button
                onClick={() => setIsCreating(true)}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <svg className="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Create Set
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {sets.map((set) => (
              <div key={set.id} className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-gray-900 truncate">
                    {set.title}
                  </h3>
                  {set.description && (
                    <p className="mt-1 text-sm text-gray-500 line-clamp-2">
                      {set.description}
                    </p>
                  )}
                  <div className="mt-4 flex items-center text-sm text-gray-500">
                    <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                      <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                    </svg>
                    {set.total_cards || 0} cards
                  </div>
                  <div className="mt-2 flex items-center text-sm text-gray-500">
                    <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                    </svg>
                    Updated {new Date(set.updated_at).toLocaleDateString()}
                  </div>
                </div>
                <div className="bg-gray-50 px-4 py-4 sm:px-6 flex justify-between">
                  <Link
                    href={`/dashboard/sets/${set.id}`}
                    className="text-sm font-medium text-primary-600 hover:text-primary-500"
                  >
                    View Set
                  </Link>
                  <button
                    onClick={() => handleDeleteSet(set.id)}
                    className="text-sm font-medium text-red-600 hover:text-red-500"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
