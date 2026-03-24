/**
 * ChatWindow.jsx — Scrollable message list.
 * Updated with new premium theme styling.
 */

import ResponseCard from './ResponseCard'

export default function ChatWindow({ messages, isLoading, language, messagesEndRef }) {
  // ─── Welcome screen (no messages yet) ────────────────────────
  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center overflow-y-auto p-6">
        <div className="text-center max-w-md animate-fade-in-up">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-4xl mx-auto mb-6 shadow-xl shadow-cyan-500/20">
            🩺
          </div>
          <h2 className="text-2xl font-bold mb-3 text-slate-900" style={{ fontFamily: 'var(--font-heading)' }}>
            {language === 'mr' ? 'नमस्कार! मी तुमचा MediMind AI सहाय्यक आहे' : 'Hello! I\'m MediMind AI'}
          </h2>
          <p className="text-slate-500 mb-8 leading-relaxed">
            {language === 'mr'
              ? 'तुमची लक्षणे खाली लिहा किंवा बोला, आणि मी संभाव्य आजार आणि उपचार सुचवतो.'
              : 'Describe your symptoms below or use voice input, and I\'ll suggest possible conditions and remedies.'}
          </p>

          {/* Quick-start chips */}
          <div className="flex flex-wrap gap-2 justify-center">
            {(language === 'mr'
              ? ['ताप आणि डोकेदुखी', 'सर्दी आणि खोकला', 'पोटदुखी आणि उलटी', 'त्वचेवर पुरळ']
              : ['Fever and headache', 'Cold and cough', 'Stomach pain', 'Skin rash']
            ).map((chip, i) => (
              <span key={i} className="px-4 py-2 rounded-full text-sm cursor-default bg-white border border-slate-200/80 shadow-sm
                text-slate-500 hover:text-cyan-600 hover:border-cyan-300 transition-all">
                💡 {chip}
              </span>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // ─── Message list ────────────────────────────────────────────
  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`flex animate-fade-in-up ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          style={{ animationDelay: `${idx * 0.05}s` }}
        >
          {msg.role === 'user' ? (
            <div className="max-w-[80%] md:max-w-[60%]">
              <div className="px-5 py-3.5 rounded-2xl rounded-br-md text-white bg-gradient-to-r from-cyan-500 to-blue-500 shadow-md shadow-cyan-500/15">
                <p className="text-sm md:text-base leading-relaxed">{msg.content}</p>
              </div>
              <p className="text-[10px] text-slate-400 mt-1 text-right font-medium">
                {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          ) : (
            <div className="max-w-[90%] md:max-w-[75%] flex gap-3">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-xs font-bold shrink-0 mt-1 shadow-sm">
                M
              </div>
              <div className="flex-1">
                <ResponseCard data={msg.content} language={language} />
                <p className="text-[10px] text-slate-400 mt-1 font-medium">
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>
          )}
        </div>
      ))}

      {/* ─── Loading indicator ──────────────────────────── */}
      {isLoading && (
        <div className="flex justify-start animate-fade-in-up">
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-xs font-bold shadow-sm">
              M
            </div>
            <div className="bg-white rounded-2xl rounded-bl-md px-5 py-4 shadow-sm border border-slate-200/80">
              <div className="loading-dots text-cyan-500">
                <span></span><span></span><span></span>
              </div>
              <p className="text-xs text-slate-400 mt-2 font-medium">
                {language === 'mr' ? 'विश्लेषण करत आहे...' : 'Analyzing symptoms...'}
              </p>
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  )
}
