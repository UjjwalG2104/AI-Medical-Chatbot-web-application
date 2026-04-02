import { useState, useRef, useEffect } from 'react'

const SYMPTOM_SUGGESTIONS = [
  'fever', 'headache', 'cough', 'cold', 'sore throat', 'body ache', 'fatigue',
  'nausea', 'vomiting', 'diarrhea', 'stomach pain', 'chest pain', 'breathlessness',
  'dizziness', 'joint pain', 'rash', 'itching', 'swelling', 'back pain', 'muscle pain',
  'runny nose', 'sneezing', 'chills', 'sweating', 'loss of appetite', 'insomnia',
  'anxiety', 'palpitations', 'blurred vision', 'ear pain', 'toothache', 'constipation',
]

const MARATHI_SUGGESTIONS = [
  'ताप', 'डोकेदुखी', 'खोकला', 'सर्दी', 'घसादुखी', 'अंगदुखी', 'थकवा',
  'मळमळ', 'उलटी', 'जुलाब', 'पोटदुखी', 'छातीदुखी', 'श्वास घेण्यास त्रास',
  'चक्कर', 'सांधेदुखी', 'पुरळ', 'खाज', 'सूज', 'पाठदुखी',
]

export default function ChatInput({ onSend, isLoading, placeholder, language }) {
  const [text, setText] = useState('')
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [suggestions, setSuggestions] = useState([])
  const [isListening, setIsListening] = useState(false)
  const [voiceError, setVoiceError] = useState(null)
  const textareaRef = useRef(null)
  const containerRef = useRef(null)
  const recognitionRef = useRef(null)

  const MAX_CHARS = 500
  const charPercent = (text.length / MAX_CHARS) * 100

  // ─── Autoresize textarea ───
  useEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 160) + 'px'
  }, [text])

  // ─── Autocomplete ───
  function handleTextChange(val) {
    if (val.length > MAX_CHARS) return
    setText(val)
    const words = val.split(/\s+/)
    const last = words[words.length - 1].toLowerCase()

    if (last.length >= 2) {
      const pool = language === 'mr' ? MARATHI_SUGGESTIONS : SYMPTOM_SUGGESTIONS
      const filtered = pool.filter(s => s.toLowerCase().includes(last)).slice(0, 5)
      setSuggestions(filtered)
      setShowSuggestions(filtered.length > 0)
    } else {
      setShowSuggestions(false)
    }
  }

  function applySuggestion(s) {
    const words = text.split(/\s+/)
    words[words.length - 1] = s
    setText(words.join(' ') + ' ')
    setShowSuggestions(false)
    textareaRef.current?.focus()
  }

  // ─── Close on outside click ───
  useEffect(() => {
    function handleClick(e) {
      if (!containerRef.current?.contains(e.target)) setShowSuggestions(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  // ─── Voice Input (Web Speech API) ───
  function toggleVoice() {
    setVoiceError(null)
    if (isListening) {
      recognitionRef.current?.stop()
      setIsListening(false)
      return
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) {
      setVoiceError('Voice input not supported in this browser. Try Chrome.')
      return
    }

    const recognition = new SpeechRecognition()
    recognitionRef.current = recognition
    recognition.lang = language === 'mr' ? 'mr-IN' : 'en-IN'
    recognition.interimResults = true
    recognition.continuous = false
    recognition.maxAlternatives = 1

    recognition.onstart = () => setIsListening(true)
    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(r => r[0].transcript)
        .join('')
      setText(transcript)
    }
    recognition.onerror = (e) => {
      setIsListening(false)
      if (e.error === 'not-allowed') setVoiceError('Microphone permission denied.')
      else setVoiceError('Voice recognition error. Please try again.')
    }
    recognition.onend = () => setIsListening(false)
    recognition.start()
  }

  // ─── Submit ───
  function handleSubmit(e) {
    e?.preventDefault()
    const trimmed = text.trim()
    if (!trimmed || isLoading) return
    onSend(trimmed)
    setText('')
    setShowSuggestions(false)
    if (textareaRef.current) textareaRef.current.style.height = 'auto'
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
    if (e.key === 'Escape') setShowSuggestions(false)
  }

  return (
    <div ref={containerRef} className="relative">
      {/* ─── Autocomplete Dropdown ─── */}
      {showSuggestions && (
        <div
          className="absolute bottom-full mb-2 left-0 right-0 rounded-2xl overflow-hidden shadow-xl z-50 border"
          style={{ background: 'var(--bg-secondary)', borderColor: 'var(--border-color)' }}
        >
          {suggestions.map((s, i) => (
            <button
              key={i}
              type="button"
              onClick={() => applySuggestion(s)}
              className="w-full text-left px-4 py-2.5 text-sm flex items-center gap-2.5 transition-colors hover:bg-cyan-50 dark:hover:bg-cyan-500/10"
              style={{ color: 'var(--text-secondary)' }}
            >
              <svg className="w-3.5 h-3.5 text-cyan-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span className="font-medium">{s}</span>
            </button>
          ))}
        </div>
      )}

      {/* ─── Voice Error ─── */}
      {voiceError && (
        <div className="mb-2 px-4 py-2 rounded-xl text-xs font-medium text-red-600 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20">
          {voiceError}
        </div>
      )}

      {/* ─── Input Row ─── */}
      <div
        className={`flex items-end gap-2 rounded-2xl transition-all duration-200 shadow-[var(--shadow-card)] ${isListening ? 'ring-2 ring-red-400/60' : 'ring-1 focus-within:ring-2 focus-within:ring-cyan-400/60'}`}
        style={{ background: 'var(--bg-secondary)', ringColor: 'var(--border-color)' }}
      >
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => handleTextChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={isListening ? '🎙️ Listening... speak clearly' : placeholder}
          rows={1}
          disabled={isLoading}
          className="flex-1 resize-none bg-transparent border-0 outline-none px-5 py-4 text-sm leading-relaxed placeholder:text-slate-400 disabled:opacity-50 max-h-40 overflow-y-auto"
          style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-body)' }}
        />

        <div className="flex items-center gap-1 pr-3 pb-3">
          {/* Character counter */}
          {text.length > MAX_CHARS * 0.8 && (
            <span className={`text-[10px] font-bold tabular-nums ${text.length >= MAX_CHARS ? 'text-red-500' : 'text-amber-400'}`}>
              {MAX_CHARS - text.length}
            </span>
          )}

          {/* Voice Button */}
          <button
            type="button"
            onClick={toggleVoice}
            disabled={isLoading}
            title={isListening ? 'Stop recording' : 'Voice input'}
            className={`w-9 h-9 rounded-xl flex items-center justify-center transition-all ${
              isListening
                ? 'bg-red-500 text-white animate-pulse'
                : 'text-slate-400 hover:text-cyan-500 hover:bg-cyan-50 dark:hover:bg-cyan-500/10'
            }`}
          >
            <svg className="w-4 h-4" fill={isListening ? 'currentColor' : 'none'} viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </button>

          {/* Send Button */}
          <button
            type="button"
            onClick={handleSubmit}
            disabled={isLoading || !text.trim()}
            className="w-10 h-10 rounded-xl flex items-center justify-center font-bold transition-all bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-md shadow-cyan-500/20 hover:shadow-cyan-500/40 hover:scale-105 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {isLoading ? (
              <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* ─── Live Voice Waveform Indicator ─── */}
      {isListening && (
        <div className="flex items-center justify-center gap-1 mt-2">
          {[1, 2, 3, 4, 5, 4, 3, 2, 1].map((h, i) => (
            <div
              key={i}
              className="rounded-full bg-red-400"
              style={{
                width: 3,
                height: h * 4,
                animation: `wave ${0.5 + i * 0.07}s ease-in-out infinite alternate`,
              }}
            />
          ))}
          <span className="ml-2 text-[11px] text-red-400 font-semibold">Recording...</span>
        </div>
      )}
    </div>
  )
}
