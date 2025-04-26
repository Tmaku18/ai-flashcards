'use client'

import { useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { documentAPI } from '@/services/api'

export default function UploadPage() {
  const router = useRouter()
  const fileInputRef = useRef<HTMLInputElement>(null)
  
  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState('')
  const [uploadedDocument, setUploadedDocument] = useState<{
    filename: string;
    content_type: string;
    size: number;
    text_content?: string;
  } | null>(null)
  const [setTitle, setSetTitle] = useState('')
  const [setDescription, setSetDescription] = useState('')
  const [success, setSuccess] = useState(false)

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null
    setFile(selectedFile)
    setError('')
    setUploadedDocument(null)
    setSuccess(false)
  }

  // Handle file drop
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (e.dataTransfer.files?.length) {
      const droppedFile = e.dataTransfer.files[0]
      setFile(droppedFile)
      setError('')
      setUploadedDocument(null)
      setSuccess(false)
    }
  }

  // Prevent default drag behaviors
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
  }

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file to upload')
      return
    }

    // Check file type
    const validTypes = ['.pdf', '.docx', '.txt']
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
    if (!validTypes.includes(fileExtension)) {
      setError('Invalid file type. Supported types: PDF, DOCX, TXT')
      return
    }

    // Check file size (10MB max)
    const maxSize = 10 * 1024 * 1024 // 10MB
    if (file.size > maxSize) {
      setError(`File too large. Maximum size: 10MB`)
      return
    }

    try {
      setIsUploading(true)
      setError('')
      
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await documentAPI.uploadDocument(formData)
      setUploadedDocument(response.data)
    } catch (err: any) {
      setError(err.message || 'Failed to upload document')
      console.error(err)
    } finally {
      setIsUploading(false)
    }
  }

  // Handle flashcard generation
  const handleGenerateFlashcards = async () => {
    if (!uploadedDocument) {
      setError('Please upload a document first')
      return
    }

    if (!setTitle.trim()) {
      setError('Please enter a title for the flashcard set')
      return
    }

    try {
      setIsProcessing(true)
      setError('')
      
      await documentAPI.generateFlashcardsFromDocument(
        uploadedDocument.filename,
        setTitle,
        setDescription || undefined
      )
      
      setSuccess(true)
    } catch (err: any) {
      setError(err.message || 'Failed to generate flashcards')
      console.error(err)
    } finally {
      setIsProcessing(false)
    }
  }

  // Reset the form
  const handleReset = () => {
    setFile(null)
    setUploadedDocument(null)
    setSetTitle('')
    setSetDescription('')
    setError('')
    setSuccess(false)
    
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-semibold text-gray-900">Upload Document</h1>
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

        {success ? (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6 text-center">
              <svg className="mx-auto h-12 w-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="mt-2 text-lg font-medium text-gray-900">Flashcards Generated Successfully!</h3>
              <div className="mt-3 text-sm text-gray-500">
                <p>Your flashcards have been created from the document.</p>
              </div>
              <div className="mt-6 flex justify-center space-x-4">
                <button
                  onClick={() => router.push('/dashboard/sets')}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  View Flashcard Sets
                </button>
                <button
                  onClick={handleReset}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Upload Another Document
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Upload a Document</h3>
              <div className="mt-2 max-w-xl text-sm text-gray-500">
                <p>Upload a document to automatically generate flashcards using AI.</p>
              </div>
              
              {!uploadedDocument ? (
                <div className="mt-5">
                  <div 
                    className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md"
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                  >
                    <div className="space-y-1 text-center">
                      <svg
                        className="mx-auto h-12 w-12 text-gray-400"
                        stroke="currentColor"
                        fill="none"
                        viewBox="0 0 48 48"
                        aria-hidden="true"
                      >
                        <path
                          d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                          strokeWidth={2}
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                      <div className="flex text-sm text-gray-600">
                        <label
                          htmlFor="file-upload"
                          className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                        >
                          <span>Upload a file</span>
                          <input
                            id="file-upload"
                            name="file-upload"
                            type="file"
                            className="sr-only"
                            accept=".pdf,.docx,.txt"
                            onChange={handleFileChange}
                            ref={fileInputRef}
                          />
                        </label>
                        <p className="pl-1">or drag and drop</p>
                      </div>
                      <p className="text-xs text-gray-500">PDF, DOCX, or TXT up to 10MB</p>
                    </div>
                  </div>
                  
                  {file && (
                    <div className="mt-4">
                      <div className="flex items-center justify-between bg-gray-50 p-3 rounded-md">
                        <div className="flex items-center">
                          <svg className="h-6 w-6 text-gray-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          <span className="text-sm text-gray-900 truncate">{file.name}</span>
                        </div>
                        <button
                          type="button"
                          onClick={() => setFile(null)}
                          className="text-sm text-red-600 hover:text-red-500"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  )}
                  
                  <div className="mt-5">
                    <button
                      type="button"
                      onClick={handleUpload}
                      disabled={!file || isUploading}
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
                    >
                      {isUploading ? 'Uploading...' : 'Upload Document'}
                    </button>
                  </div>
                </div>
              ) : (
                <div className="mt-5">
                  <div className="bg-gray-50 p-4 rounded-md mb-5">
                    <h4 className="text-md font-medium text-gray-900">Document Uploaded</h4>
                    <p className="mt-1 text-sm text-gray-500">{uploadedDocument.filename}</p>
                    <p className="text-xs text-gray-500">
                      {(uploadedDocument.size / 1024).toFixed(2)} KB • {uploadedDocument.content_type}
                    </p>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <label htmlFor="set-title" className="block text-sm font-medium text-gray-700">
                        Flashcard Set Title <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        name="set-title"
                        id="set-title"
                        value={setTitle}
                        onChange={(e) => setSetTitle(e.target.value)}
                        className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        required
                      />
                    </div>
                    
                    <div>
                      <label htmlFor="set-description" className="block text-sm font-medium text-gray-700">
                        Description (Optional)
                      </label>
                      <textarea
                        name="set-description"
                        id="set-description"
                        rows={3}
                        value={setDescription}
                        onChange={(e) => setSetDescription(e.target.value)}
                        className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                      />
                    </div>
                  </div>
                  
                  <div className="mt-5 flex space-x-3">
                    <button
                      type="button"
                      onClick={handleGenerateFlashcards}
                      disabled={isProcessing || !setTitle.trim()}
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
                    >
                      {isProcessing ? 'Generating Flashcards...' : 'Generate Flashcards'}
                    </button>
                    
                    <button
                      type="button"
                      onClick={handleReset}
                      className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="mt-6 bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">How It Works</h3>
            <div className="mt-2 max-w-xl text-sm text-gray-500">
              <ol className="list-decimal pl-5 space-y-2">
                <li>Upload a document (PDF, DOCX, or TXT)</li>
                <li>Our AI will analyze the content and extract key concepts</li>
                <li>Flashcards will be automatically generated based on the document content</li>
                <li>Review and study the generated flashcards</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
