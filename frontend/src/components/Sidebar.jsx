export default function Sidebar({ isOpen, onToggle, history, onHistoryClick, onNewChat, t, language }) {
  return (
    <>
      {/* ─── Mobile overlay ─── */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-20 lg:hidden"
          onClick={onToggle}
        />
      )}

      {/* ─── Sidebar panel ─── */}
      <aside
        className={`
          fixed lg:relative z-30 h-full
          w-72 bg-slate-900 text-white
          flex flex-col transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:hidden'}
        `}
        id="sidebar"
      >
        {/* ─── Header ─── */}
        <div className="p-5 border-b border-white/10">
          <button
            onClick={onNewChat}
            id="new-chat-btn"
            className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold text-sm rounded-xl py-3 flex items-center justify-center gap-2 transition-all hover:shadow-lg hover:shadow-cyan-500/25 active:scale-[0.98]"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16m8-8H4" />
            </svg>
            {t.newChat}
          </button>
        </div>

        {/* ─── History list ─── */}
        <div className="flex-1 overflow-y-auto p-4">
          <h3 className="text-[10px] font-semibold uppercase tracking-widest text-slate-500 px-2 mb-3">
            {t.history}
          </h3>

          {history.length === 0 ? (
            <div className="px-3 py-8 text-center">
              <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center mx-auto mb-3 text-slate-600">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
              </div>
              <p className="text-sm text-slate-500">
                {language === 'mr' ? 'अद्याप कोणताही चॅट नाही' : 'No chats yet'}
              </p>
            </div>
          ) : (
            <div className="space-y-1.5">
              {history.map((item, i) => (
                <button
                  key={i}
                  onClick={() => onHistoryClick(item)}
                  className="w-full text-left px-3 py-3 rounded-xl text-sm
                    text-slate-300 hover:bg-white/10 hover:text-white
                    transition-all group flex items-center gap-3"
                >
                  <svg className="w-4 h-4 shrink-0 text-slate-600 group-hover:text-cyan-400 transition-colors" fill="none"
                       stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                          d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  <span className="truncate">{item.user_input}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* ─── Footer ─── */}
        <div className="p-5 border-t border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-sm font-bold shadow-md shadow-cyan-500/20">
              M
            </div>
            <div>
              <p className="text-sm font-semibold text-white tracking-tight">MediMind</p>
              <p className="text-[10px] text-slate-500 font-medium">v2.0 · AI Health</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
