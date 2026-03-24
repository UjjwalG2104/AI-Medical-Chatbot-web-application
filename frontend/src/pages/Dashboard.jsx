import { useState, useRef, useEffect } from 'react'
import Sidebar from '../components/Sidebar'
import ChatInput from '../components/ChatInput'
import ResponseCard from '../components/ResponseCard'
import { API_BASE_URL } from '../config'

export default function Dashboard({ token, setToken }) {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const messagesEndRef = useRef(null)

  const [language, setLanguage] = useState('en')

  async function parseApiResponse(response) {
    const text = await response.text()
    try {
      return JSON.parse(text)
    } catch {
      if (text.trim().toLowerCase().startsWith('<!doctype') || text.trim().startsWith('<html')) {
        throw new Error('API endpoint returned HTML instead of JSON. Check VITE_API_BASE_URL and backend routes.')
      }
      throw new Error(`Unexpected API response (status ${response.status}).`)
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
    },
    mr: {
      title: 'मेडीमाईंड AI',
      subtitle: 'तुमचा आरोग्य सहाय्यक',
      placeholder: 'तुमची लक्षणे येथे सांगा...',
      poweredBy: 'एआय-आधारित अंतर्दृष्टी. नेहमी वैद्यकीय व्यावसायिकांशी सल्लामसलत करा.',
      logout: 'बाहेर पडा',
      newChat: 'नवीन चॅट',
      history: 'अलीकडील चॅट',
    },
  }
  const t = texts[language]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // ─── Fetch History ───
  const [history, setHistory] = useState([])
  useEffect(() => {
    if (!token) return
    fetch(`${API_BASE_URL}/history?limit=10`, {
      headers: { 'Authorization': `Bearer ${token}` },
    })
      .then((res) => parseApiResponse(res))
      .then((data) => {
        if (!data.error) setHistory(data)
      })
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

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ message: text, language }),
      })

      const data = await parseApiResponse(response)
      if (response.status === 401) {
        handleLogout()
        return
      }

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
    <div className="flex h-screen w-screen overflow-hidden bg-gray-50" style={{ fontFamily: 'var(--font-body)' }}>
      {/* ─── Sidebar ─── */}
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        history={history}
        onHistoryClick={handleHistoryClick}
        onNewChat={handleNewChat}
        t={t}
        language={language}
      />

      {/* ─── Main Content ─── */}
      <div className="flex-1 flex flex-col min-w-0 relative">

        {/* ─── Header ─── */}
        <header className="bg-white flex items-center justify-between px-5 py-3.5 border-b border-slate-200/80 z-20 shadow-[0_1px_3px_rgba(0,0,0,0.03)]">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 -ml-1 rounded-xl text-slate-400 hover:text-cyan-600 hover:bg-cyan-50 transition-all"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-sm font-bold shadow-md shadow-cyan-500/20">
                M
              </div>
              <div className="hidden sm:block">
                <h1 className="text-base font-bold text-slate-900 tracking-tight leading-tight" style={{ fontFamily: 'var(--font-heading)' }}>{t.title}</h1>
                <p className="text-[11px] text-slate-400 font-medium">{t.subtitle}</p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Language Toggle */}
            <div className="flex items-center p-1 bg-slate-100 rounded-lg">
              <button
                onClick={() => setLanguage('en')}
                className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                  language === 'en'
                    ? 'bg-white text-cyan-600 shadow-sm'
                    : 'text-slate-400 hover:text-slate-600'
                }`}
              >
                EN
              </button>
              <button
                onClick={() => setLanguage('mr')}
                className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                  language === 'mr'
                    ? 'bg-white text-cyan-600 shadow-sm'
                    : 'text-slate-400 hover:text-slate-600'
                }`}
              >
                मराठी
              </button>
            </div>

            <button
              onClick={handleLogout}
              className="p-2 rounded-xl text-slate-400 hover:text-red-500 hover:bg-red-50 transition-all"
              title={t.logout}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </header>

        {/* ─── Chat Area ─── */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 scroll-smooth relative" id="chat-container" style={{ background: 'linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%)' }}>
          <div className="max-w-3xl mx-auto space-y-5 pb-20">
            {messages.length === 0 ? (
              /* ─── Empty State ─── */
              <div className="h-full flex flex-col items-center justify-center text-center mt-16 md:mt-28 px-4 animate-fade-in-up">
                <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-4xl mb-8 shadow-xl shadow-cyan-500/20">
                  🩺
                </div>
                <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900 mb-3 tracking-tight" style={{ fontFamily: 'var(--font-heading)' }}>
                  {language === 'mr' ? 'तुमच्या आरोग्यासाठी मी इथे आहे' : 'How can I help you today?'}
                </h2>
                <p className="text-slate-500 max-w-md mx-auto leading-relaxed text-sm mb-10">
                  {language === 'mr'
                    ? 'तुमची लक्षणे खाली सांगा आणि मी संभाव्य आजार, उपचार आणि सावधगिरी सुचवतो.'
                    : 'Describe your symptoms below and I\'ll analyze possible conditions, suggest remedies, and provide precautions.'}
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
                  {(language === 'mr'
                    ? ['ताप आणि डोकेदुखी', 'सतत खोकला आणि सर्दी']
                    : ['I have a headache and fever', 'Constant cough and cold symptoms']
                  ).map((suggestion, i) => (
                    <button
                      key={i}
                      onClick={() => handleSend(suggestion)}
                      className="group bg-white border border-slate-200/80 text-left p-4 rounded-2xl text-sm text-slate-600 hover:text-cyan-700 hover:border-cyan-300 hover:shadow-md transition-all"
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
                  style={{ animationDelay: `${idx * 0.05}s` }}
                >
                  {msg.role === 'user' ? (
                    <div className="max-w-[85%] md:max-w-[75%]">
                      <div className="px-5 py-3.5 rounded-2xl rounded-br-md text-white bg-gradient-to-r from-cyan-500 to-blue-500 shadow-md shadow-cyan-500/15">
                        <p className="text-sm md:text-base leading-relaxed whitespace-pre-line">{msg.content}</p>
                      </div>
                      <span className="text-[10px] mt-1.5 block text-right text-slate-400 font-medium">
                        {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                  ) : (
                    <div className="max-w-[92%] md:max-w-[85%] flex gap-3">
                      <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-xs font-bold shrink-0 mt-1 shadow-sm">
                        M
                      </div>
                      <div className="flex-1 min-w-0">
                        <ResponseCard data={msg.content} language={language} />
                        <span className="text-[10px] mt-1.5 block text-slate-400 font-medium">
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
                    M
                  </div>
                  <div className="bg-white rounded-2xl rounded-bl-md px-5 py-4 shadow-sm border border-slate-200/80">
                    <div className="loading-dots text-cyan-500">
                      <span></span><span></span><span></span>
                    </div>
                    <p className="text-xs text-slate-400 mt-2 font-medium">
                      {language === 'mr' ? 'विश्लेषण करत आहे...' : 'Analyzing your symptoms...'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* ─── Input Area ─── */}
        <div className="p-4 md:px-6 md:py-5 bg-white border-t border-slate-200/80 z-20">
          <div className="max-w-3xl mx-auto">
            <ChatInput
              onSend={handleSend}
              isLoading={isLoading}
              placeholder={t.placeholder}
              language={language}
            />
            <p className="text-center text-[11px] text-slate-400 mt-3 flex items-center justify-center gap-1.5">
              <svg className="w-3 h-3 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              {t.poweredBy}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
