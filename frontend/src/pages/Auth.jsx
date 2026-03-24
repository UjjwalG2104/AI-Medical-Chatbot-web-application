import { useState } from 'react'
import { API_BASE_URL } from '../config'

export default function Auth({ setToken }) {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)

    const endpoint = isLogin ? 'auth/login' : 'auth/signup'
    try {
      const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Authentication failed')
      }

      if (isLogin) {
        localStorage.setItem('token', data.token)
        localStorage.setItem('userEmail', email)
        setToken(data.token)
      } else {
        setError('Account created! Please sign in now.')
        setIsLogin(true)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex" style={{ fontFamily: 'var(--font-body)' }}>

      {/* ─── Left Panel — Branding ─── */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-slate-950 items-center justify-center overflow-hidden">
        {/* Animated gradient blobs */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-cyan-500/15 rounded-full blur-[100px] animate-float"></div>
          <div className="absolute bottom-1/4 right-1/4 w-60 h-60 bg-blue-500/15 rounded-full blur-[80px] animate-float" style={{ animationDelay: '2s' }}></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-violet-500/8 rounded-full blur-[120px]"></div>
        </div>

        <div className="relative z-10 text-center px-12 animate-fade-in-up">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-3xl font-bold mx-auto mb-8 shadow-2xl shadow-cyan-500/25">
            M
          </div>
          <h1 className="text-4xl font-extrabold text-white mb-4 tracking-tight" style={{ fontFamily: 'var(--font-heading)' }}>
            MediMind AI
          </h1>
          <p className="text-slate-400 text-lg leading-relaxed max-w-sm mx-auto">
            Your intelligent health companion. Get instant symptom analysis and personalized insights.
          </p>
          <div className="mt-10 flex items-center justify-center gap-6 text-slate-500 text-sm">
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              Secure
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
              AI-Powered
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" /></svg>
              Multilingual
            </div>
          </div>
        </div>
      </div>

      {/* ─── Right Panel — Auth Form ─── */}
      <div className="flex-1 flex items-center justify-center bg-slate-50 px-6 py-12 relative">
        {/* Mobile: subtle background */}
        <div className="absolute top-0 inset-x-0 h-40 bg-gradient-to-b from-cyan-50 to-transparent lg:hidden pointer-events-none"></div>

        <div className="w-full max-w-md relative z-10 animate-fade-in-up">
          {/* Mobile logo */}
          <div className="lg:hidden text-center mb-8">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4 shadow-lg shadow-cyan-500/20">
              M
            </div>
            <h2 className="text-xl font-bold text-slate-900" style={{ fontFamily: 'var(--font-heading)' }}>MediMind AI</h2>
          </div>

          {/* Card */}
          <div className="bg-white rounded-2xl p-8 shadow-[var(--shadow-soft)] border border-slate-200/80">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-slate-900 tracking-tight mb-2" style={{ fontFamily: 'var(--font-heading)' }}>
                {isLogin ? 'Welcome Back' : 'Create Account'}
              </h2>
              <p className="text-slate-500 text-sm">
                {isLogin ? 'Sign in to continue to MediMind.' : 'Join MediMind to get started.'}
              </p>
            </div>

            {error && (
              <div className={`p-4 rounded-xl mb-6 text-sm font-semibold border flex items-center gap-2 ${
                error.includes('created') || error.includes('successful')
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : 'bg-red-50 text-red-600 border-red-200'
              }`}>
                <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={error.includes('created') ? "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" : "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"} />
                </svg>
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-1.5">
                <label className="block text-sm font-semibold text-slate-700">Email Address</label>
                <div className="relative">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                  </div>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 text-slate-900 pl-12 pr-4 py-3.5 rounded-xl text-sm outline-none transition-all placeholder:text-slate-400 focus:bg-white focus:border-cyan-400 focus:ring-4 focus:ring-cyan-500/10"
                    placeholder="you@example.com"
                    required
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="block text-sm font-semibold text-slate-700">Password</label>
                <div className="relative">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                  </div>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 text-slate-900 pl-12 pr-4 py-3.5 rounded-xl text-sm outline-none transition-all placeholder:text-slate-400 focus:bg-white focus:border-cyan-400 focus:ring-4 focus:ring-cyan-500/10 tracking-widest"
                    placeholder="••••••••"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-4 rounded-xl font-bold mt-2 disabled:opacity-60 disabled:cursor-not-allowed flex justify-center items-center gap-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/35 transition-all active:scale-[0.98] text-base"
              >
                {loading ? (
                  <div className="loading-dots text-white">
                    <span></span><span></span><span></span>
                  </div>
                ) : (
                  <>
                    {isLogin ? 'Sign In' : 'Create Account'}
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                  </>
                )}
              </button>
            </form>

            <div className="mt-8 text-center text-sm text-slate-500 pt-6 border-t border-slate-100">
              {isLogin ? "Don't have an account? " : 'Already have an account? '}
              <button
                onClick={() => { setIsLogin(!isLogin); setError('') }}
                className="text-cyan-600 hover:text-cyan-700 transition-colors font-bold"
              >
                {isLogin ? 'Sign Up' : 'Sign In'}
              </button>
            </div>
          </div>

          <p className="text-center text-xs text-slate-400 mt-6">
            Protected by industry-standard encryption.
          </p>
        </div>
      </div>
    </div>
  )
}
