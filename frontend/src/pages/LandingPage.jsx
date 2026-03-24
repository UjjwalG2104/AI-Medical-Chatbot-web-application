import { useState } from 'react'

export default function LandingPage({ onGetStarted }) {
  const [language, setLanguage] = useState('en')

  const content = {
    en: {
      badge: 'AI-Powered Health Assistant',
      headline: 'Your Smart',
      headlineAccent: 'Health Companion.',
      subtext: 'Get instant symptom analysis, possible conditions, recommended remedies, and precautions — all powered by advanced AI. Available in English and Marathi.',
      cta: 'Get Started Free',
      ctaSub: 'No credit card required',
      features: [
        {
          icon: '🧠',
          title: 'Smart Symptom Analysis',
          desc: 'Describe your symptoms in natural language and get AI-powered insights about possible conditions.',
          color: 'from-blue-500 to-cyan-400',
          bg: 'bg-blue-50',
        },
        {
          icon: '🎙️',
          title: 'Voice Input Support',
          desc: 'Speak your symptoms aloud in English or Marathi — our voice recognition does the rest.',
          color: 'from-violet-500 to-purple-400',
          bg: 'bg-violet-50',
        },
        {
          icon: '💊',
          title: 'Remedies & Precautions',
          desc: 'Receive suggested medicines, dosage info, and clinical precautions for each identified condition.',
          color: 'from-emerald-500 to-teal-400',
          bg: 'bg-emerald-50',
        },
      ],
      steps: [
        { num: '01', title: 'Describe Symptoms', desc: 'Type or speak your symptoms in your preferred language.' },
        { num: '02', title: 'AI Analysis', desc: 'Our AI analyzes patterns and identifies possible conditions.' },
        { num: '03', title: 'Get Insights', desc: 'Review conditions, remedies, precautions, and expert AI advice.' },
      ],
      howItWorks: 'How It Works',
      footer: '© 2026 MediMind AI. All rights reserved. Not a substitute for professional medical advice.',
    },
    mr: {
      badge: 'एआय-आधारित आरोग्य सहाय्यक',
      headline: 'तुमचा स्मार्ट',
      headlineAccent: 'आरोग्य सहाय्यक.',
      subtext: 'तात्काळ लक्षण विश्लेषण, संभाव्य आजार, शिफारस केलेले उपाय आणि सावधगिरी मिळवा — सर्व प्रगत एआय द्वारे. इंग्रजी आणि मराठीमध्ये उपलब्ध.',
      cta: 'मोफत सुरू करा',
      ctaSub: 'क्रेडिट कार्ड आवश्यक नाही',
      features: [
        {
          icon: '🧠',
          title: 'स्मार्ट लक्षण विश्लेषण',
          desc: 'तुमची लक्षणे नैसर्गिक भाषेत सांगा आणि एआय-आधारित अंतर्दृष्टी मिळवा.',
          color: 'from-blue-500 to-cyan-400',
          bg: 'bg-blue-50',
        },
        {
          icon: '🎙️',
          title: 'आवाज ओळख',
          desc: 'इंग्रजी किंवा मराठीमध्ये बोलून तुमची लक्षणे सांगा.',
          color: 'from-violet-500 to-purple-400',
          bg: 'bg-violet-50',
        },
        {
          icon: '💊',
          title: 'उपचार आणि सावधगिरी',
          desc: 'प्रत्येक ओळखलेल्या आजारासाठी सुचवलेली औषधे आणि सावधगिरी मिळवा.',
          color: 'from-emerald-500 to-teal-400',
          bg: 'bg-emerald-50',
        },
      ],
      steps: [
        { num: '01', title: 'लक्षणे सांगा', desc: 'तुमच्या पसंतीच्या भाषेत लक्षणे टाइप करा किंवा बोला.' },
        { num: '02', title: 'एआय विश्लेषण', desc: 'आमचे एआय नमुने विश्लेषित करते आणि संभाव्य परिस्थिती ओळखते.' },
        { num: '03', title: 'अंतर्दृष्टी मिळवा', desc: 'आजार, उपाय, सावधगिरी आणि तज्ञ सल्ला पहा.' },
      ],
      howItWorks: 'कसे कार्य करते',
      footer: '© 2026 MediMind AI. सर्व हक्क राखीव. व्यावसायिक वैद्यकीय सल्ल्याचा पर्याय नाही.',
    },
  }

  const t = content[language]

  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-hidden" style={{ fontFamily: 'var(--font-body)' }}>

      {/* ─── Navbar ─── */}
      <nav className="fixed w-full z-50 top-0">
        <div className="mx-auto max-w-7xl px-6">
          <div className="flex items-center justify-between h-20 glass-dark rounded-b-2xl px-6 border-t-0" style={{ borderTop: 'none' }}>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-cyan-500/25">
                M
              </div>
              <span className="text-lg font-bold tracking-tight" style={{ fontFamily: 'var(--font-heading)' }}>MediMind</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center p-1 rounded-lg bg-white/10 border border-white/10">
                <button onClick={() => setLanguage('en')} className={`px-3 py-1.5 rounded-md text-sm font-semibold transition-all ${language === 'en' ? 'bg-white text-slate-900 shadow-sm' : 'text-white/70 hover:text-white'}`}>EN</button>
                <button onClick={() => setLanguage('mr')} className={`px-3 py-1.5 rounded-md text-sm font-semibold transition-all ${language === 'mr' ? 'bg-white text-slate-900 shadow-sm' : 'text-white/70 hover:text-white'}`}>मराठी</button>
              </div>
              <button
                onClick={onGetStarted}
                className="hidden sm:inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:-translate-y-0.5 transition-all active:scale-[0.98]"
              >
                {t.cta}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* ─── Hero ─── */}
      <section className="relative pt-36 pb-24 lg:pt-48 lg:pb-36">
        {/* Background effects */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-[120px] animate-float"></div>
          <div className="absolute bottom-20 right-1/4 w-80 h-80 bg-blue-500/10 rounded-full blur-[100px] animate-float" style={{ animationDelay: '3s' }}></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-violet-500/5 rounded-full blur-[150px]"></div>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 text-center">
          {/* Badge */}
          <div className="animate-fade-in-up inline-flex items-center gap-2 px-5 py-2 rounded-full bg-white/5 border border-white/10 text-cyan-300 text-sm font-semibold mb-8 backdrop-blur-sm">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            {t.badge}
          </div>

          {/* Headline */}
          <h1 className="animate-fade-in-up stagger-1 text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.1] mb-6 max-w-4xl mx-auto" style={{ fontFamily: 'var(--font-heading)', opacity: 0 }}>
            {t.headline}{' '}
            <span className="gradient-text">{t.headlineAccent}</span>
          </h1>

          {/* Subtext */}
          <p className="animate-fade-in-up stagger-2 text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed font-medium" style={{ opacity: 0 }}>
            {t.subtext}
          </p>

          {/* CTA */}
          <div className="animate-fade-in-up stagger-3 flex flex-col items-center gap-3" style={{ opacity: 0 }}>
            <button
              onClick={onGetStarted}
              className="group relative inline-flex items-center gap-3 px-8 py-4 rounded-2xl text-lg font-bold bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-[0_8px_32px_rgba(14,165,233,0.35)] hover:shadow-[0_12px_40px_rgba(14,165,233,0.5)] hover:-translate-y-1 transition-all active:scale-[0.98]"
            >
              <span>{t.cta}</span>
              <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </button>
            <span className="text-sm text-slate-500">{t.ctaSub}</span>
          </div>
        </div>
      </section>

      {/* ─── Features ─── */}
      <section className="py-24 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900/50 to-slate-950 pointer-events-none"></div>
        <div className="relative z-10 max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-3 gap-6">
            {t.features.map((f, i) => (
              <div
                key={i}
                className="group p-8 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm hover:bg-white/10 hover:border-white/20 hover:-translate-y-1 transition-all duration-300"
              >
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${f.color} flex items-center justify-center text-2xl mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                  {f.icon}
                </div>
                <h3 className="text-xl font-bold text-white mb-3" style={{ fontFamily: 'var(--font-heading)' }}>{f.title}</h3>
                <p className="text-slate-400 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── How It Works ─── */}
      <section className="py-24 relative">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl md:text-4xl font-extrabold text-center mb-16" style={{ fontFamily: 'var(--font-heading)' }}>
            {t.howItWorks}
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {t.steps.map((step, i) => (
              <div key={i} className="relative text-center">
                <div className="text-6xl font-black gradient-text mb-4 opacity-50" style={{ fontFamily: 'var(--font-heading)' }}>
                  {step.num}
                </div>
                <h3 className="text-xl font-bold text-white mb-2" style={{ fontFamily: 'var(--font-heading)' }}>{step.title}</h3>
                <p className="text-slate-400">{step.desc}</p>
                {i < 2 && (
                  <div className="hidden md:block absolute top-10 -right-4 w-8 text-slate-700">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="border-t border-white/10 py-10">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white text-xs font-bold">M</div>
            <span className="text-sm font-bold text-white tracking-tight">MediMind</span>
          </div>
          <p className="text-sm text-slate-500">{t.footer}</p>
        </div>
      </footer>
    </div>
  )
}
