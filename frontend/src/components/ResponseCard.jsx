import { useState } from 'react'

/* ─── Lightweight Markdown-to-JSX renderer ─── */
function renderMarkdown(text) {
  if (!text) return null
  const lines = text.split('\n')
  const elements = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    if (line.startsWith('## ') || line.startsWith('### ') || line.startsWith('**') && line.endsWith('**') && line.length > 4) {
      const content = line.replace(/^#{2,3}\s/, '').replace(/^\*\*(.*)\*\*$/, '$1')
      elements.push(
        <h3 key={i} className="font-bold text-xs uppercase tracking-wider text-cyan-600 dark:text-cyan-400 mt-3 mb-1 first:mt-0 flex items-center gap-1.5">
          <span className="w-1 h-3 bg-gradient-to-b from-cyan-500 to-blue-500 rounded-full inline-block" />
          {content}
        </h3>
      )
    } else if (line.startsWith('- ') || line.startsWith('• ')) {
      const bullets = []
      while (i < lines.length && (lines[i].startsWith('- ') || lines[i].startsWith('• '))) {
        bullets.push(lines[i].replace(/^[-•]\s/, ''))
        i++
      }
      elements.push(
        <ul key={`ul-${i}`} className="space-y-1 my-1.5">
          {bullets.map((b, j) => (
            <li key={j} className="flex items-start gap-2 text-[12px] leading-relaxed text-slate-600 dark:text-slate-300">
              <span className="text-cyan-500 mt-0.5 shrink-0">•</span>
              <span dangerouslySetInnerHTML={{ __html: inlineBold(b) }} />
            </li>
          ))}
        </ul>
      )
      continue
    } else if (line.trim()) {
      elements.push(
        <p key={i} className="text-[12px] leading-relaxed text-slate-600 dark:text-slate-300 my-1"
           dangerouslySetInnerHTML={{ __html: inlineBold(line) }} />
      )
    }
    i++
  }
  return elements
}

function inlineBold(text) {
  return text.replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-slate-800 dark:text-slate-100">$1</strong>')
}

/* ─── Copy Button ─── */
function CopyButton({ text }) {
  const [copied, setCopied] = useState(false)
  function copy() {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }
  return (
    <button
      onClick={copy}
      className="p-1.5 rounded-lg text-slate-400 hover:text-cyan-500 hover:bg-cyan-50 dark:hover:bg-cyan-500/10 transition-all"
      title="Copy response"
    >
      {copied ? (
        <svg className="w-3.5 h-3.5 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
        </svg>
      ) : (
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      )}
    </button>
  )
}

/* ─── Confidence Bar ─── */
function ConfidenceBar({ score }) {
  const pct = Math.min(Math.round(score * 25), 100)
  const color = pct >= 70 ? 'from-emerald-400 to-teal-400'
    : pct >= 40 ? 'from-cyan-400 to-blue-500'
    : 'from-amber-400 to-orange-400'
  return (
    <div className="flex items-center gap-2 min-w-[80px]">
      <div className="flex-1 h-1.5 rounded-full bg-slate-100 dark:bg-slate-700 overflow-hidden">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${color} transition-all duration-700`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 w-7 text-right">{pct}%</span>
    </div>
  )
}

/* ─── Disease Card ─── */
function DiseaseCard({ disease, index, labels }) {
  const [expanded, setExpanded] = useState(index === 0)
  return (
    <div className="rounded-xl border border-slate-100 dark:border-white/5 overflow-hidden bg-slate-50 dark:bg-slate-800/50">
      {/* Card header — always visible, clickable */}
      <button
        className="w-full text-left px-4 py-3 flex items-center justify-between gap-3 hover:bg-slate-100 dark:hover:bg-white/5 transition-all"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-2 min-w-0">
          <span className="w-5 h-5 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 text-white text-[10px] font-bold flex items-center justify-center shrink-0">
            {index + 1}
          </span>
          <h5 className="font-bold text-slate-900 dark:text-slate-100 text-sm truncate" style={{ fontFamily: 'var(--font-heading)' }}>
            {disease.name}
          </h5>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <ConfidenceBar score={disease.score} />
          <svg
            className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${expanded ? 'rotate-180' : ''}`}
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {/* Expandable body */}
      {expanded && (
        <div className="px-4 pb-4 border-t border-slate-100 dark:border-white/5 pt-3 space-y-3 animate-fade-in">
          <p className="text-[12px] text-slate-500 dark:text-slate-400 leading-relaxed">{disease.description}</p>
          {disease.precautions?.length > 0 && (
            <div className="bg-white dark:bg-slate-800 rounded-lg p-3 border border-slate-100 dark:border-white/5">
              <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-2">{labels.precautions}</p>
              <ul className="space-y-1.5">
                {disease.precautions.map((p, j) => (
                  <li key={j} className="text-[12px] text-slate-600 dark:text-slate-300 flex items-start gap-2">
                    <svg className="w-4 h-4 text-cyan-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 13l4 4L19 7" />
                    </svg>
                    <span>{p}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

/* ─── Feedback Buttons ─── */
function FeedbackButtons() {
  const [vote, setVote] = useState(null)
  return (
    <div className="flex items-center gap-2 mt-3 pt-3 border-t border-slate-100 dark:border-white/5">
      <span className="text-[10px] text-slate-400 font-medium mr-1">Was this helpful?</span>
      <button
        className={`feedback-btn up ${vote === 'up' ? 'active-up' : ''}`}
        onClick={() => setVote(vote === 'up' ? null : 'up')}
      >
        👍 <span>{vote === 'up' ? 'Thanks!' : 'Yes'}</span>
      </button>
      <button
        className={`feedback-btn down ${vote === 'down' ? 'active-down' : ''}`}
        onClick={() => setVote(vote === 'down' ? null : 'down')}
      >
        👎 <span>No</span>
      </button>
    </div>
  )
}

/* ═══════════════════════════════════════════════════
   Main ResponseCard Component
   ═══════════════════════════════════════════════════ */
export default function ResponseCard({ data, language, onFollowUp }) {
  if (!data) return null

  const {
    message,
    symptoms_found = [],
    diseases = [],
    medicines = [],
    home_remedies = [],
    severity = 'unknown',
    emergency = false,
    emergency_reason = null,
    confidence = null,
    ai_advice,
    follow_up_questions = [],
    disclaimer,
  } = data

  const labels = language === 'mr'
    ? {
        symptoms: 'आढळलेली लक्षणे',
        possibleConditions: 'संभाव्य आजार',
        suggestedMedicines: 'सुचवलेली औषधे',
        homeRemedies: '🌿 घरगुती उपाय',
        precautions: 'सावधगिरी',
        aiAdvice: 'AI विश्लेषण',
        warning: '⚠️ सावधानता',
        severity: { mild: 'सौम्य', moderate: 'मध्यम', severe: 'तीव्र', unknown: 'अज्ञात' },
        urgentTitle: '🚨 तत्काळ वैद्यकीय मदत घ्या!',
        urgentDesc: 'तुमची लक्षणे गंभीर असू शकतात. कृपया ताबडतोब डॉक्टरांशी संपर्क करा किंवा आपत्कालीन सेवा कॉल करा.',
        emergencyTitle: '🆘 आपत्कालीन — आत्ता 112 / 108 कॉल करा!',
        followUpTitle: 'पुढील प्रश्न',
        aiConfidence: 'AI आत्मविश्वास',
      }
    : {
        symptoms: 'Detected Symptoms',
        possibleConditions: 'Possible Conditions',
        suggestedMedicines: 'Suggested Medicines',
        homeRemedies: '🌿 Home Remedies',
        precautions: 'Precautions',
        aiAdvice: 'AI Analysis',
        warning: '⚠️ Warning',
        severity: { mild: 'Mild', moderate: 'Moderate', severe: 'Severe', unknown: 'Unknown' },
        urgentTitle: '🚨 Seek Urgent Medical Attention',
        urgentDesc: 'Your symptoms may indicate a serious condition. Please contact a doctor or emergency service immediately.',
        emergencyTitle: '🆘 EMERGENCY — Call 112 / 108 Now!',
        followUpTitle: 'Follow-up Questions',
        aiConfidence: 'AI Confidence',
      }

  const severityLabel = labels.severity[severity] || labels.severity.unknown

  // Build plain text for copy
  const plainText = [
    symptoms_found.length > 0 && `Symptoms: ${symptoms_found.join(', ')}`,
    diseases.length > 0 && `Conditions: ${diseases.map(d => d.name).join(', ')}`,
    medicines.length > 0 && `Remedies: ${medicines.map(m => m.name).join(', ')}`,
    ai_advice && `AI Advice:\n${ai_advice}`,
  ].filter(Boolean).join('\n\n')

  return (
    <div className="space-y-3">
      {/* ─── EMERGENCY Banner (AI-flagged true emergency) ─── */}
      {emergency && (
        <div className="rounded-xl p-4 flex items-start gap-3 animate-pulse-glow"
             style={{ background: 'linear-gradient(135deg,#450a0a,#7f1d1d)', border: '2px solid #ef4444' }}>
          <span className="text-2xl shrink-0">🆘</span>
          <div>
            <p className="font-black text-red-200 text-sm">{labels.emergencyTitle}</p>
            {emergency_reason && (
              <p className="text-red-300 text-[11px] mt-1 leading-relaxed">{emergency_reason}</p>
            )}
          </div>
        </div>
      )}

      {/* ─── Urgent Care Alert (severe severity) ─── */}
      {!emergency && severity === 'severe' && (
        <div className="urgent-alert">
          <div className="w-8 h-8 rounded-full bg-red-100 dark:bg-red-500/20 flex items-center justify-center shrink-0">
            <svg className="w-4 h-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <p className="text-sm font-bold text-red-700 dark:text-red-400">{labels.urgentTitle}</p>
            <p className="text-[11px] text-red-600 dark:text-red-500 mt-0.5 leading-relaxed">{labels.urgentDesc}</p>
          </div>
        </div>
      )}

      {/* ─── Fallback message ─── */}
      {message && (
        <div className="bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-white/5 rounded-2xl rounded-tl-md p-4 shadow-[var(--shadow-card)]">
          <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">{message}</p>
        </div>
      )}

      {/* ─── Severity + Symptoms ─── */}
      {symptoms_found.length > 0 && (
        <div className="bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-white/5 rounded-2xl p-5 shadow-[var(--shadow-card)]">
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100 dark:border-white/5">
            <h4 className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              {labels.symptoms}
            </h4>
            <span className={`badge-${severity}`}>{severityLabel}</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {symptoms_found.map((s, i) => (
              <span key={i} className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-50 text-cyan-700 border border-cyan-200 dark:bg-cyan-500/10 dark:text-cyan-300 dark:border-cyan-500/20">
                {s}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* ─── Diseases (collapsible) ─── */}
      {diseases.length > 0 && (
        <div className="bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-white/5 rounded-2xl p-5 shadow-[var(--shadow-card)]">
          <h4 className="text-[11px] font-semibold uppercase tracking-wider text-indigo-500 dark:text-indigo-400 mb-4 flex items-center gap-2 pb-3 border-b border-slate-100 dark:border-white/5">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {labels.possibleConditions}
            <span className="text-[10px] text-slate-400 font-normal ml-1">(click to expand)</span>
          </h4>
          <div className="space-y-2">
            {diseases.map((disease, i) => (
              <DiseaseCard key={i} disease={disease} index={i} labels={labels} />
            ))}
          </div>
        </div>
      )}

      {/* ─── Medicines ─── */}
      {medicines.length > 0 && (
        <div className="bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-white/5 rounded-2xl p-5 shadow-[var(--shadow-card)]">
          <h4 className="text-[11px] font-semibold uppercase tracking-wider text-teal-500 dark:text-teal-400 mb-4 flex items-center gap-2 pb-3 border-b border-slate-100 dark:border-white/5">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            {labels.suggestedMedicines}
          </h4>
          <div className="space-y-2.5">
            {medicines.map((med, i) => (
              <div key={i} className="bg-slate-50 dark:bg-slate-700/50 border border-slate-100 dark:border-white/5 rounded-xl p-3.5">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-400 to-emerald-400 flex items-center justify-center text-lg shrink-0 shadow-sm">
                    💊
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-slate-900 dark:text-slate-100">{med.name}</p>
                    <p className="text-xs text-slate-400 mt-0.5 font-medium">{med.dosage}</p>
                    {med.notes && (
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">{med.notes}</p>
                    )}
                    {med.warning && (
                      <p className="text-[11px] text-amber-600 dark:text-amber-400 mt-1.5 bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/20 rounded-lg px-2 py-1 leading-relaxed font-medium">
                        ⚠️ {med.warning}
                      </p>
                    )}
                  </div>
                  <span className="text-[10px] uppercase font-semibold tracking-wider text-teal-600 dark:text-teal-400 bg-teal-50 dark:bg-teal-500/10 border border-teal-200 dark:border-teal-500/20 px-2.5 py-1 rounded-md shrink-0">
                    {med.type}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ─── Home Remedies ─── */}
      {home_remedies.length > 0 && (
        <div className="bg-white dark:bg-slate-800 border border-emerald-200/60 dark:border-emerald-500/20 rounded-2xl p-4 shadow-[var(--shadow-card)]">
          <div className="absolute-left-strip bg-gradient-to-b from-emerald-400 to-teal-400" />
          <h4 className="text-[11px] font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 mb-3 flex items-center gap-2">
            <span className="text-base">🌿</span>
            {labels.homeRemedies}
          </h4>
          <ul className="space-y-2">
            {home_remedies.map((r, i) => (
              <li key={i} className="flex items-start gap-2.5 text-sm" style={{ color: 'var(--text-secondary)' }}>
                <span className="text-emerald-400 mt-0.5 shrink-0 text-base">🍃</span>
                <span className="leading-relaxed font-medium">{r}</span>
              </li>
            ))}
          </ul>
          <p className="text-[10px] text-slate-400 mt-3 italic">These are supportive measures only — not a substitute for medical treatment.</p>
        </div>
      )}

      {/* ─── AI Advice (with markdown rendering + confidence) ─── */}
      {ai_advice && (
        <div className="relative overflow-hidden bg-gradient-to-br from-indigo-50 to-blue-50 dark:from-indigo-950/40 dark:to-blue-950/40 border border-indigo-200/50 dark:border-indigo-500/20 rounded-2xl p-5 shadow-[var(--shadow-card)]">
          <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-indigo-500 to-blue-500 rounded-r" />
          <div className="flex items-center justify-between mb-3 pl-3">
            <h4 className="text-[11px] font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 flex items-center gap-2 flex-wrap">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              {labels.aiAdvice}
              {confidence !== null && (
                <span className="px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-300 text-[10px] font-bold">
                  {labels.aiConfidence}: {Math.round(confidence * 100)}%
                </span>
              )}
            </h4>
            <CopyButton text={plainText} />
          </div>
          <div className="pl-3 prose-medical">
            {renderMarkdown(ai_advice)}
          </div>
          <FeedbackButtons />
        </div>
      )}

      {/* ─── Follow-up Questions ─── */}
      {follow_up_questions.length > 0 && onFollowUp && (
        <div className="bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-white/5 rounded-2xl p-4 shadow-[var(--shadow-card)]">
          <h4 className="text-[11px] font-semibold uppercase tracking-wider text-violet-600 dark:text-violet-400 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {labels.followUpTitle}
          </h4>
          <div className="flex flex-wrap gap-2">
            {follow_up_questions.map((q, i) => (
              <button
                key={i}
                onClick={() => onFollowUp(q)}
                className="text-left px-3 py-2 rounded-xl text-[12px] font-medium transition-all hover:-translate-y-0.5 hover:shadow-md border group"
                style={{ background: 'var(--bg-primary)', borderColor: 'var(--border-color)', color: 'var(--text-secondary)' }}
              >
                <span className="text-violet-400 mr-1.5 group-hover:text-violet-500">→</span>
                {q}
              </button>
            ))}
          </div>
        </div>
      )}


      {/* ─── Copy button when no ai_advice ─── */}
      {!ai_advice && (symptoms_found.length > 0 || diseases.length > 0) && (
        <div className="flex justify-end">
          <div className="flex items-center gap-1 text-[10px] text-slate-400">
            <CopyButton text={plainText} />
            <span>Copy</span>
          </div>
        </div>
      )}

      {/* ─── Disclaimer ─── */}
      {disclaimer && (
        <div className="rounded-xl p-3.5 bg-amber-50 dark:bg-amber-500/10 border border-amber-200/80 dark:border-amber-500/20">
          <p className="text-[11px] text-amber-700 dark:text-amber-400 flex items-start gap-2 leading-relaxed font-medium">
            <svg className="w-4 h-4 shrink-0 mt-0.5 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {disclaimer}
          </p>
        </div>
      )}
    </div>
  )
}
