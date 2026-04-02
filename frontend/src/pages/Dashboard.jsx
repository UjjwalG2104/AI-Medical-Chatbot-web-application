import { useState, useRef, useEffect } from 'react'
import Sidebar from '../components/Sidebar'
import ChatInput from '../components/ChatInput'
import ResponseCard from '../components/ResponseCard'
import { API_BASE_URL } from '../config'

/* ─── Dark mode hook ─── */
function useDarkMode() {
  const [dark, setDark] = useState(() => {
    try { return localStorage.getItem('medimind-dark') === 'true' } catch { return false }
  })
  useEffect(() => {
    const root = document.documentElement
    if (dark) root.classList.add('dark')
    else root.classList.remove('dark')
    try { localStorage.setItem('medimind-dark', String(dark)) } catch {}
  }, [dark])
  return [dark, setDark]
}

export default function Dashboard({ token, setToken }) {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [language, setLanguage] = useState('en')
  const [dark, setDark] = useDarkMode()
  const [history, setHistory] = useState([])
  const [stats, setStats] = useState(null)
  const messagesEndRef = useRef(null)

  const userEmail = (() => { try { return localStorage.getItem('userEmail') } catch { return null } })()

  async function parseApiResponse(response, endpointLabel) {
    const text = await response.text()
    const contentType = response.headers.get('content-type') || 'unknown'
    const compactPreview = text.trim().replace(/\s+/g, ' ').slice(0, 120)
    try {
      return JSON.parse(text)
    } catch {
      if (text.trim().toLowerCase().startsWith('<!doctype') || text.trim().startsWith('<html')) {
        throw new Error(
          `Expected JSON but got HTML for ${endpointLabel}. URL: ${response.url}. Status: ${response.status}. ` +
          'Set VITE_API_BASE_URL to your backend origin only and verify routes: /auth/login, /auth/signup, /chat, /history.'
        )
      }
      throw new Error(
        `Unexpected API response for ${endpointLabel}. URL: ${response.url}. Status: ${response.status}. ` +
        `Content-Type: ${contentType}. Body preview: ${compactPreview || '(empty)'}`
      )
    }
  }

  const texts = {
    en: {
      title: 'MediMind AI',
      subtitle: 'Your Health Assistant',
      placeholder: 'Describe your symptoms here...',
      poweredBy: 'AI-powered insights. Always verify with a medical professional.',
      logout: 'Logout',
      newChat: 'New Chat',
      history: 'Recent Chats',
      totalChats: 'Total Chats',
      topSymptom: 'Top Symptom',
      darkMode: 'Dark mode',
      analyzing: 'Analyzing your symptoms...',
    },
    mr: {
      title: 'मेडीमाईंड AI',
      subtitle: 'तुमचा आरोग्य सहाय्यक',
      placeholder: 'तुमची लक्षणे येथे सांगा...',
      poweredBy: 'एआय-आधारित अंतर्दृष्टी. नेहमी वैद्यकीय व्यावसायिकांशी सल्लामसलत करा.',
      logout: 'बाहेर पडा',
      newChat: 'नवीन चॅट',
      history: 'अलीकडील चॅट',
      totalChats: 'एकूण चॅट',
      topSymptom: 'मुख्य लक्षण',
      darkMode: 'डार्क मोड',
      analyzing: 'विश्लेषण करत आहे...',
    },
  }
  const t = texts[language]

  // ─── Quick suggestions ───
  const quickSuggestions = language === 'mr'
    ? ['ताप आणि डोकेदुखी', 'सतत खोकला आणि सर्दी', 'पोटदुखी आणि मळमळ', 'अंगदुखी आणि थकवा']
    : ['I have a headache and fever', 'Constant cough and cold symptoms', 'Stomach pain with nausea', 'Body ache and fatigue']

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => { scrollToBottom() }, [messages])

  // ─── Fetch History ───
  useEffect(() => {
    if (!token) return
    fetch(`${API_BASE_URL}/history?limit=15`, {
      headers: { 'Authorization': `Bearer ${token}` },
    })
      .then((res) => parseApiResponse(res, 'history'))
      .then((data) => { if (!data.error) setHistory(data) })
      .catch(console.error)
  }, [token, messages])

  // ─── Fetch Stats ───
  useEffect(() => {
    if (!token) return
    fetch(`${API_BASE_URL}/stats`, {
      headers: { 'Authorization': `Bearer ${token}` },
    })
      .then((res) => parseApiResponse(res, 'stats'))
      .then((data) => { if (!data.error) setStats(data) })
      .catch(console.error)
  }, [token, messages])

  function handleHistoryClick(item) {
    setMessages([
      { role: 'user', content: item.user_input, timestamp: item.timestamp },
      { role: 'bot', content: item.response, timestamp: item.timestamp },
    ])
    setLanguage(item.language || language)
    if (window.innerWidth < 1024) setSidebarOpen(false)
  }

  function handleNewChat() {
    setMessages([])
    if (window.innerWidth < 1024) setSidebarOpen(false)
  }

  async function handleSend(text) {
    const userMsg = { role: 'user', content: text, timestamp: new Date().toISOString() }
    setMessages((prev) => [...prev, userMsg])
    setIsLoading(true)

    // Build conversation history to send to backend for multi-turn AI context
    const conversationHistory = messages.map((m) => ({
      role: m.role,
      content: typeof m.content === 'string' ? m.content : m.content,
    }))

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ message: text, language, conversation_history: conversationHistory }),
      })

      const data = await parseApiResponse(response, 'chat')
      if (response.status === 401) { handleLogout(); return }

      const botMsg = { role: 'bot', content: data, timestamp: new Date().toISOString() }
      setMessages((prev) => [...prev, botMsg])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMsg = {
        role: 'bot',
        content: { message: error?.message || 'Connection error. Please make sure the backend server is running.' },
        timestamp: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, errorMsg])
    }

    setIsLoading(false)
  }

  function handleLogout() {
    localStorage.removeItem('token')
    localStorage.removeItem('userEmail')
    setToken(null)
  }

  return (
    <div className="flex h-screen w-screen overflow-hidden" style={{ background: 'var(--bg-primary)', fontFamily: 'var(--font-body)' }}>

      {/* ─── Sidebar ─── */}
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        history={history}
        onHistoryClick={handleHistoryClick}
        onNewChat={handleNewChat}
        t={t}
        language={language}
        userEmail={userEmail}
      />

      {/* ─── Main Content ─── */}
      <div className="flex-1 flex flex-col min-w-0 relative overflow-hidden">

        {/* ─── Header ─── */}
        <header className="flex-shrink-0 flex flex-col z-20" style={{ background: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-color)' }}>
          {/* Main header row */}
          <div className="flex items-center justify-between px-5 py-3.5">
            <div className="flex items-center gap-3">
              {/* Mobile hamburger */}
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 -ml-1 rounded-xl transition-all"
                style={{ color: 'var(--text-secondary)' }}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-sm font-bold shadow-md shadow-cyan-500/20">
                  🩺
                </div>
                <div className="hidden sm:block">
                  <h1 className="text-base font-bold tracking-tight leading-tight" style={{ fontFamily: 'var(--font-heading)', color: 'var(--text-primary)' }}>{t.title}</h1>
                  <p className="text-[11px] font-medium" style={{ color: 'var(--text-light)' }}>{t.subtitle}</p>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {/* Language Toggle */}
              <div className="flex items-center p-1 rounded-lg" style={{ background: 'var(--bg-input)' }}>
                <button
                  onClick={() => setLanguage('en')}
                  className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                    language === 'en' ? 'bg-white dark:bg-slate-700 text-cyan-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'
                  }`}
                >EN</button>
                <button
                  onClick={() => setLanguage('mr')}
                  className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                    language === 'mr' ? 'bg-white dark:bg-slate-700 text-cyan-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'
                  }`}
                >मराठी</button>
              </div>

              {/* Dark Mode Toggle */}
              <button
                onClick={() => setDark(!dark)}
                id="dark-mode-btn"
                className="p-2 rounded-xl transition-all"
                style={{ color: 'var(--text-secondary)' }}
                title={t.darkMode}
              >
                {dark ? (
                  <svg className="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2.25a.75.75 0 01.75.75v2.25a.75.75 0 01-1.5 0V3a.75.75 0 01.75-.75zM7.5 12a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM18.894 6.166a.75.75 0 00-1.06-1.06l-1.591 1.59a.75.75 0 101.06 1.061l1.591-1.59zM21.75 12a.75.75 0 01-.75.75h-2.25a.75.75 0 010-1.5H21a.75.75 0 01.75.75zM17.834 18.894a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 10-1.061 1.06l1.59 1.591zM12 18a.75.75 0 01.75.75V21a.75.75 0 01-1.5 0v-2.25A.75.75 0 0112 18zM7.166 17.834a.75.75 0 00-1.06 1.06l1.59 1.591a.75.75 0 001.061-1.06l-1.59-1.591zM6 12a.75.75 0 01-.75.75H3a.75.75 0 010-1.5h2.25A.75.75 0 016 12zM6.166 6.166a.75.75 0 001.06 1.06l-1.59 1.591a.75.75 0 01-1.061-1.06l1.59-1.591z" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                )}
              </button>

              {/* Logout */}
              <button
                onClick={handleLogout}
                className="p-2 rounded-xl transition-all hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10"
                style={{ color: 'var(--text-light)' }}
                title={t.logout}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </div>

          {/* Stats bar */}
          {stats && (
            <div className="px-5 pb-2.5 flex items-center gap-2 flex-wrap">
              <div className="stat-chip">
                <svg className="w-3 h-3 text-cyan-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <span>{stats.total_chats} {t.totalChats}</span>
              </div>
              {stats.top_symptoms?.[0] && (
                <div className="stat-chip">
                  <svg className="w-3 h-3 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <span>{t.topSymptom}: <strong>{stats.top_symptoms[0]}</strong></span>
                </div>
              )}
              {stats.severity_breakdown?.severe > 0 && (
                <div className="stat-chip !border-red-200 dark:!border-red-500/20">
                  <span className="w-2 h-2 rounded-full bg-red-500" />
                  <span className="!text-red-600 dark:!text-red-400">{stats.severity_breakdown.severe} severe</span>
                </div>
              )}
              {stats.severity_breakdown?.moderate > 0 && (
                <div className="stat-chip !border-amber-200 dark:!border-amber-500/20">
                  <span className="w-2 h-2 rounded-full bg-amber-400" />
                  <span className="!text-amber-600 dark:!text-amber-400">{stats.severity_breakdown.moderate} moderate</span>
                </div>
              )}
            </div>
          )}
        </header>

        {/* ─── Chat Area ─── */}
        <div
          className="flex-1 overflow-y-auto p-4 md:p-6 scroll-smooth"
          id="chat-container"
          style={{ background: dark ? 'var(--bg-primary)' : 'linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%)' }}
        >
          <div className="max-w-3xl mx-auto space-y-5 pb-20">
            {messages.length === 0 ? (
              /* ─── Empty State ─── */
              <div className="h-full flex flex-col items-center justify-center text-center mt-10 md:mt-20 px-4 animate-fade-in-up">
                <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-4xl mb-6 shadow-xl shadow-cyan-500/20">
                  🩺
                </div>
                <h2 className="text-2xl md:text-3xl font-extrabold mb-3 tracking-tight" style={{ fontFamily: 'var(--font-heading)', color: 'var(--text-primary)' }}>
                  {language === 'mr' ? 'तुमच्या आरोग्यासाठी मी इथे आहे' : 'How can I help you today?'}
                </h2>
                <p className="max-w-md mx-auto leading-relaxed text-sm mb-8" style={{ color: 'var(--text-secondary)' }}>
                  {language === 'mr'
                    ? 'तुमची लक्षणे खाली सांगा. मी संभाव्य आजार, उपचार आणि सावधगिरी सुचवतो.'
                    : 'Describe your symptoms below. I\'ll analyze possible conditions, suggest remedies and precautions.'}
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
                  {quickSuggestions.map((suggestion, i) => (
                    <button
                      key={i}
                      onClick={() => handleSend(suggestion)}
                      className="group text-left p-4 rounded-2xl text-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
                      style={{
                        background: 'var(--bg-secondary)',
                        border: '1px solid var(--border-color)',
                        color: 'var(--text-secondary)',
                      }}
                    >
                      <span className="text-cyan-500 mr-2 group-hover:translate-x-0.5 inline-block transition-transform">→</span>
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              /* ─── Messages ─── */
              messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in-up`}
                  style={{ animationDelay: `${idx * 0.04}s` }}
                >
                  {msg.role === 'user' ? (
                    <div className="max-w-[85%] md:max-w-[75%]">
                      <div className="px-5 py-3.5 rounded-2xl rounded-br-md text-white bg-gradient-to-r from-cyan-500 to-blue-500 shadow-md shadow-cyan-500/15">
                        <p className="text-sm md:text-base leading-relaxed whitespace-pre-line">{msg.content}</p>
                      </div>
                      <span className="text-[10px] mt-1.5 block text-right font-medium" style={{ color: 'var(--text-light)' }}>
                        {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                  ) : (
                    <div className="max-w-[92%] md:max-w-[85%] flex gap-3">
                      <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-xs font-bold shrink-0 mt-1 shadow-sm">
                        🩺
                      </div>
                      <div className="flex-1 min-w-0">
                        <ResponseCard
                          data={msg.content}
                          language={language}
                          onFollowUp={handleSend}
                        />
                        <span className="text-[10px] mt-1.5 block font-medium" style={{ color: 'var(--text-light)' }}>
                          {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}

            {/* Loading */}
            {isLoading && (
              <div className="flex justify-start animate-fade-in-up">
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-xs font-bold shrink-0 shadow-sm">
                    🩺
                  </div>
                  <div className="rounded-2xl rounded-bl-md px-5 py-4 shadow-sm" style={{ background: 'var(--bg-secondary)', border: '1px solid var(--border-color)' }}>
                    <div className="loading-dots text-cyan-500">
                      <span /><span /><span />
                    </div>
                    <p className="text-xs mt-2 font-medium" style={{ color: 'var(--text-light)' }}>
                      {t.analyzing}
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* ─── Input Area ─── */}
        <div className="flex-shrink-0 p-4 md:px-6 md:py-5 z-20" style={{ background: 'var(--bg-secondary)', borderTop: '1px solid var(--border-color)' }}>
          <div className="max-w-3xl mx-auto">
            <ChatInput
              onSend={handleSend}
              isLoading={isLoading}
              placeholder={t.placeholder}
              language={language}
            />
            <p className="text-center text-[11px] mt-3 flex items-center justify-center gap-1.5" style={{ color: 'var(--text-light)' }}>
              <svg className="w-3 h-3 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {t.poweredBy}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
