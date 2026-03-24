export default function ResponseCard({ data, language }) {
  if (!data) return null

  const {
    message,
    symptoms_found = [],
    diseases = [],
    medicines = [],
    severity = 'unknown',
    ai_advice,
    disclaimer,
  } = data

  const labels =
    language === 'mr'
      ? {
          symptoms: 'आढळलेली लक्षणे',
          possibleConditions: 'संभाव्य आजार',
          suggestedMedicines: 'सुचवलेली औषधे',
          precautions: 'सावधगिरी',
          aiAdvice: 'AI विश्लेषण',
          severity: { mild: 'सौम्य', moderate: 'मध्यम', severe: 'तीव्र', unknown: 'अज्ञात' },
          matchScore: 'जुळणी',
        }
      : {
          symptoms: 'Detected Symptoms',
          possibleConditions: 'Possible Conditions',
          suggestedMedicines: 'Suggested Remedies',
          precautions: 'Precautions',
          aiAdvice: 'AI Analysis',
          severity: { mild: 'Mild', moderate: 'Moderate', severe: 'Severe', unknown: 'Unknown' },
          matchScore: 'Match',
        }

  const severityLabel = labels.severity[severity] || labels.severity.unknown

  return (
    <div className="space-y-3">
      {/* ─── Fallback message ─── */}
      {message && (
        <div className="bg-white border border-slate-200/80 rounded-2xl rounded-tl-md p-4 shadow-[var(--shadow-card)]">
          <p className="text-sm md:text-base text-slate-700 leading-relaxed">{message}</p>
        </div>
      )}

      {/* ─── Severity + Symptoms ─── */}
      {symptoms_found.length > 0 && (
        <div className="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-[var(--shadow-card)]">
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
            <h4 className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              {labels.symptoms}
            </h4>
            <span className={`badge-${severity}`}>
              {severityLabel}
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {symptoms_found.map((s, i) => (
              <span
                key={i}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-50 text-cyan-700 border border-cyan-200"
              >
                {s}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* ─── Diseases ─── */}
      {diseases.length > 0 && (
        <div className="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-[var(--shadow-card)]">
          <h4 className="text-[11px] font-semibold uppercase tracking-wider text-indigo-500 mb-4 flex items-center gap-2 pb-3 border-b border-slate-100">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {labels.possibleConditions}
          </h4>
          <div className="space-y-3">
            {diseases.map((disease, i) => (
              <div key={i} className="rounded-xl p-4 bg-slate-50 border border-slate-100">
                <div className="flex items-start justify-between mb-2">
                  <h5 className="font-bold text-slate-900 text-sm" style={{ fontFamily: 'var(--font-heading)' }}>
                    {i + 1}. {disease.name}
                  </h5>
                  <span className="text-[10px] text-indigo-600 bg-indigo-50 border border-indigo-200 px-2.5 py-1 rounded-md font-semibold shrink-0 ml-2">
                    {labels.matchScore}: {Math.round(disease.score * 25)}%
                  </span>
                </div>
                <p className="text-sm text-slate-500 leading-relaxed mb-3">{disease.description}</p>

                {disease.precautions?.length > 0 && (
                  <div className="bg-white rounded-lg p-3.5 border border-slate-200/80">
                    <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-2">
                      {labels.precautions}
                    </p>
                    <ul className="space-y-1.5">
                      {disease.precautions.map((p, j) => (
                        <li key={j} className="text-sm text-slate-600 flex items-start gap-2">
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
            ))}
          </div>
        </div>
      )}

      {/* ─── Medicines ─── */}
      {medicines.length > 0 && (
        <div className="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-[var(--shadow-card)]">
          <h4 className="text-[11px] font-semibold uppercase tracking-wider text-teal-500 mb-4 flex items-center gap-2 pb-3 border-b border-slate-100">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            {labels.suggestedMedicines}
          </h4>
          <div className="space-y-2.5">
            {medicines.map((med, i) => (
              <div key={i} className="flex items-center gap-3 bg-slate-50 border border-slate-100 rounded-xl p-3.5">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-400 to-emerald-400 flex items-center justify-center text-lg shrink-0 shadow-sm">
                  💊
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-slate-900 truncate">{med.name}</p>
                  <p className="text-xs text-slate-400 mt-0.5 font-medium">{med.dosage}</p>
                  {med.notes && (
                    <p className="text-[11px] text-slate-500 mt-1 bg-white border border-slate-100 px-2 py-0.5 rounded inline-block">{med.notes}</p>
                  )}
                </div>
                <span className="text-[10px] uppercase font-semibold tracking-wider text-teal-600 bg-teal-50 border border-teal-200 px-2.5 py-1 rounded-md shrink-0">
                  {med.type}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ─── AI Advice ─── */}
      {ai_advice && (
        <div className="relative overflow-hidden bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-200/50 rounded-2xl p-5 shadow-[var(--shadow-card)]">
          <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-indigo-500 to-blue-500 rounded-r"></div>
          <h4 className="text-[11px] font-semibold uppercase tracking-wider text-indigo-600 mb-3 flex items-center gap-2 pl-3">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            {labels.aiAdvice}
          </h4>
          <div className="text-sm text-slate-700 leading-relaxed pl-3">
            <p className="whitespace-pre-line">{ai_advice}</p>
          </div>
        </div>
      )}

      {/* ─── Disclaimer ─── */}
      {disclaimer && (
        <div className="rounded-xl p-3.5 bg-amber-50 border border-amber-200/80">
          <p className="text-[11px] text-amber-700 flex items-start gap-2 leading-relaxed font-medium">
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
