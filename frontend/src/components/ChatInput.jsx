import { useState, useRef, useEffect } from 'react'

export default function ChatInput({ onSend, isLoading, placeholder, language }) {
  const [text, setText] = useState('')
  const [isListening, setIsListening] = useState(false)
  const recognitionRef = useRef(null)
  const inputRef = useRef(null)

  // ─── Set up speech recognition ───
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) return

    const recognition = new SpeechRecognition()
    recognition.continuous = false
    recognition.interimResults = false

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      setText((prev) => prev + (prev ? ' ' : '') + transcript)
      setIsListening(false)
    }

    recognition.onerror = () => setIsListening(false)
    recognition.onend = () => setIsListening(false)

    recognitionRef.current = recognition
  }, [])

  // ─── Update language for speech recognition ───
  useEffect(() => {
    if (recognitionRef.current) {
      recognitionRef.current.lang = language === 'mr' ? 'mr-IN' : 'en-US'
    }
  }, [language])

  function toggleListening() {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in this browser. Please use Chrome.')
      return
    }
    if (isListening) {
      recognitionRef.current.stop()
      setIsListening(false)
    } else {
      recognitionRef.current.start()
      setIsListening(true)
    }
  }

  function handleSubmit(e) {
    e.preventDefault()
    if (!text.trim() || isLoading) return
    onSend(text.trim())
    setText('')
    inputRef.current?.focus()
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="relative w-full" id="chat-input-form">
      <div className="bg-white rounded-2xl flex items-center gap-2 px-4 py-2.5
                      border border-slate-200/80 shadow-[var(--shadow-card)] transition-all
                      focus-within:border-cyan-400 focus-within:ring-4 focus-within:ring-cyan-500/10 focus-within:shadow-[var(--shadow-glow)]">
        
        {/* Mic Button */}
        <button
          type="button"
          onClick={toggleListening}
          id="mic-button"
          className={`p-2.5 rounded-xl transition-all shrink-0 ${
            isListening
              ? 'bg-red-50 text-red-500 animate-pulse-glow'
              : 'hover:bg-slate-100 text-slate-400 hover:text-cyan-500'
          }`}
          title={isListening ? 'Stop listening' : 'Voice input'}
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        </button>

        {/* Text Input */}
        <input
          ref={inputRef}
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={isLoading}
          id="symptom-input"
          className="flex-1 bg-transparent border-none outline-none text-slate-800
                     placeholder:text-slate-400 text-sm md:text-base py-2 min-w-0 font-medium"
          autoComplete="off"
        />

        {/* Send Button */}
        <button
          type="submit"
          disabled={!text.trim() || isLoading}
          id="send-button"
          className="p-3 rounded-xl transition-all shrink-0 disabled:opacity-30 disabled:cursor-not-allowed text-white flex items-center justify-center bg-gradient-to-r from-cyan-500 to-blue-500 shadow-md shadow-cyan-500/20 hover:shadow-lg hover:shadow-cyan-500/30 active:scale-95"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5}
                  d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* Listening indicator */}
      {isListening && (
        <p className="absolute -top-8 left-5 text-[11px] font-semibold text-red-500 bg-red-50 px-3 py-1 rounded-full border border-red-200 shadow-sm flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping"></span>
          {language === 'mr' ? 'रेकॉर्डिंग सुरू आहे...' : 'Listening...'}
        </p>
      )}
    </form>
  )
}
