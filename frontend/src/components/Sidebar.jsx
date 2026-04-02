import { useState, useMemo } from 'react'

function getRelativeTime(timestamp) {
  const now = new Date()
  const date = new Date(timestamp)
  const diff = Math.floor((now - date) / 1000)
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`
  return date.toLocaleDateString()
}

const SEVERITY_DOT = {
  severe: 'bg-red-500',
  moderate: 'bg-amber-400',
  mild: 'bg-emerald-400',
  unknown: 'bg-slate-300',
}

export default function Sidebar({ isOpen, onToggle, history, onHistoryClick, onNewChat, t, language, userEmail }) {
  const [search, setSearch] = useState('')

  const filtered = useMemo(() => {
    if (!search.trim()) return history
    const q = search.toLowerCase()
    return history.filter(h =>
      h.user_input?.toLowerCase().includes(q) ||
      h.response?.symptoms_found?.some(s => s.toLowerCase().includes(q)) ||
      h.response?.diseases?.some(d => d.name?.toLowerCase().includes(q))
    )
  }, [history, search])

  return (
    <>
      {/* ─── Mobile Overlay ─── */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-30 lg:hidden"
          onClick={onToggle}
        />
      )}

      {/* ─── Sidebar Panel ─── */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-40
          flex flex-col h-full w-72 shrink-0
          transition-transform duration-300 ease-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
        style={{
          background: 'var(--bg-secondary)',
          borderRight: '1px solid var(--border-color)',
        }}
      >
        {/* ─── Header ─── */}
        <div className="flex items-center justify-between px-5 pt-5 pb-4">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-xs font-bold shadow-md shadow-cyan-500/20">
              🩺
            </div>
            <span className="font-bold text-base tracking-tight" style={{ fontFamily: 'var(--font-heading)', color: 'var(--text-primary)' }}>
              MediMind
            </span>
          </div>
          <button
            onClick={onToggle}
            className="lg:hidden w-8 h-8 flex items-center justify-center rounded-lg transition-all"
            style={{ color: 'var(--text-light)' }}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* ─── New Chat Button ─── */}
        <div className="px-4 mb-3">
          <button
            onClick={onNewChat}
            className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-semibold transition-all hover:-translate-y-0.5 bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-md shadow-cyan-500/20 hover:shadow-cyan-500/35"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16m8-8H4" />
            </svg>
            {t.newChat || 'New Chat'}
          </button>
        </div>

        {/* ─── Search ─── */}
        <div className="px-4 mb-3">
          <div className="relative">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={language === 'mr' ? 'इतिहास शोधा...' : 'Search history...'}
              className="w-full pl-9 pr-3 py-2 rounded-xl text-xs outline-none transition-all focus:ring-2 focus:ring-cyan-400/40"
              style={{
                background: 'var(--bg-input)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-secondary)',
              }}
            />
            {search && (
              <button
                onClick={() => setSearch('')}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </div>

        {/* ─── Section Label ─── */}
        <div className="px-5 mb-2">
          <p className="text-[10px] font-semibold uppercase tracking-widest" style={{ color: 'var(--text-light)' }}>
            {t.history || 'Recent Chats'}
            {search && filtered.length > 0 && (
              <span className="ml-1 text-cyan-500">({filtered.length})</span>
            )}
          </p>
        </div>

        {/* ─── History List ─── */}
        <div className="flex-1 overflow-y-auto px-3 space-y-1 pb-2 scrollbar-thin">
          {filtered.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center px-4">
              {search ? (
                <>
                  <div className="text-2xl mb-2">🔍</div>
                  <p className="text-xs font-medium" style={{ color: 'var(--text-light)' }}>No chats match "{search}"</p>
                </>
              ) : (
                <>
                  <div className="text-3xl mb-3 opacity-50">💬</div>
                  <p className="text-xs leading-relaxed" style={{ color: 'var(--text-light)' }}>
                    {language === 'mr' ? 'अद्याप कोणतेही चॅट नाहीत' : 'No chats yet. Start a conversation!'}
                  </p>
                </>
              )}
            </div>
          ) : (
            filtered.map((item, i) => {
              const sev = item.response?.severity || 'unknown'
              const dotClass = SEVERITY_DOT[sev] || SEVERITY_DOT.unknown
              const symptoms = item.response?.symptoms_found?.slice(0, 2) || []

              return (
                <button
                  key={i}
                  onClick={() => onHistoryClick(item)}
                  className="w-full text-left px-3 py-3 rounded-xl transition-all hover:scale-[0.99] group"
                  style={{ border: '1px solid transparent' }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = 'var(--bg-input)'
                    e.currentTarget.style.borderColor = 'var(--border-color)'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'transparent'
                    e.currentTarget.style.borderColor = 'transparent'
                  }}
                >
                  <div className="flex items-start gap-2.5">
                    {/* Severity dot */}
                    <span className={`w-2 h-2 rounded-full shrink-0 mt-1.5 ${dotClass}`} />
                    <div className="flex-1 min-w-0">
                      <p
                        className="text-[13px] font-semibold truncate group-hover:text-cyan-500 transition-colors"
                        style={{ color: 'var(--text-primary)' }}
                      >
                        {item.user_input || '...'}
                      </p>
                      {symptoms.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-1">
                          {symptoms.map((s, si) => (
                            <span
                              key={si}
                              className="text-[10px] px-1.5 py-0.5 rounded-md font-medium bg-cyan-50 dark:bg-cyan-500/10 text-cyan-600 dark:text-cyan-400"
                            >
                              {s}
                            </span>
                          ))}
                        </div>
                      )}
                      <p className="text-[10px] mt-1 font-medium" style={{ color: 'var(--text-light)' }}>
                        {getRelativeTime(item.timestamp)}
                      </p>
                    </div>
                  </div>
                </button>
              )
            })
          )}
        </div>

        {/* ─── Footer ─── */}
        <div
          className="flex-shrink-0 px-4 py-4 mt-auto"
          style={{ borderTop: '1px solid var(--border-color)' }}
        >
          {userEmail && (
            <div className="flex items-center gap-2.5 mb-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-400 to-pink-500 flex items-center justify-center text-white text-xs font-bold shrink-0">
                {userEmail[0].toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-[12px] font-semibold truncate" style={{ color: 'var(--text-primary)' }}>
                  {userEmail}
                </p>
                <p className="text-[10px]" style={{ color: 'var(--text-light)' }}>
                  {language === 'mr' ? 'प्रमाणित वापरकर्ता' : 'Verified User'}
                </p>
              </div>
            </div>
          )}
          <div className="flex items-center gap-1.5 text-[11px]" style={{ color: 'var(--text-light)' }}>
            <svg className="w-3 h-3 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            MediMind AI v2.0
          </div>
        </div>
      </aside>
    </>
  )
}
