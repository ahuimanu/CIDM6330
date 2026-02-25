export default function SprintDriftLogo() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-8">
      {/* Main Container */}
      <div className="flex flex-col items-center gap-8">

        {/* Logo Mark - Square version for avatar */}
        <div className="relative">
          <svg
            width="400"
            height="400"
            viewBox="0 0 400 400"
            className="drop-shadow-2xl"
          >
            {/* Background */}
            <defs>
              {/* Gradient for depth */}
              <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#0f172a" />
                <stop offset="100%" stopColor="#1e293b" />
              </linearGradient>

              {/* Sprint gradient - active, intense */}
              <linearGradient id="sprintGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#0ea5e9" />
                <stop offset="100%" stopColor="#38bdf8" />
              </linearGradient>

              {/* Drift gradient - contemplative, fading */}
              <linearGradient id="driftGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#0ea5e9" stopOpacity="0.2" />
              </linearGradient>

              {/* Grid pattern */}
              <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#334155" strokeWidth="0.5" opacity="0.4"/>
              </pattern>

              {/* Glow filter */}
              <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge>
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>

            {/* Base rectangle */}
            <rect width="400" height="400" fill="url(#bgGrad)" rx="12"/>

            {/* Architectural grid */}
            <rect width="400" height="400" fill="url(#grid)" rx="12"/>

            {/* Horizontal architectural lines - representing layers/strata */}
            {[80, 160, 240, 320].map((y, i) => (
              <line
                key={i}
                x1="40"
                y1={y}
                x2="360"
                y2={y}
                stroke="#334155"
                strokeWidth="1"
                opacity="0.3"
              />
            ))}

            {/* Sprint waveform - sharp, active pulses */}
            <g filter="url(#glow)">
              <path
                d="M 40 200
                   L 70 200 L 80 140 L 90 260 L 100 180 L 110 220 L 120 200
                   L 150 200 L 160 120 L 170 280 L 180 160 L 190 240 L 200 200"
                fill="none"
                stroke="url(#sprintGrad)"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </g>

            {/* Drift waveform - gradual, fading oscillation */}
            <g filter="url(#glow)">
              <path
                d="M 200 200
                   Q 220 185 240 200
                   Q 260 215 280 200
                   Q 300 190 320 200
                   Q 340 205 360 200"
                fill="none"
                stroke="url(#driftGrad)"
                strokeWidth="3"
                strokeLinecap="round"
              />
            </g>

            {/* Vertical architectural elements - nodes */}
            <circle cx="80" cy="200" r="4" fill="#0ea5e9" filter="url(#glow)"/>
            <circle cx="160" cy="200" r="4" fill="#0ea5e9" opacity="0.8"/>
            <circle cx="200" cy="200" r="6" fill="#38bdf8" filter="url(#glow)"/>
            <circle cx="280" cy="200" r="3" fill="#38bdf8" opacity="0.5"/>
            <circle cx="360" cy="200" r="2" fill="#38bdf8" opacity="0.3"/>

            {/* Corner architectural details */}
            <path d="M 40 60 L 40 40 L 60 40" fill="none" stroke="#0ea5e9" strokeWidth="2" opacity="0.6"/>
            <path d="M 360 60 L 360 40 L 340 40" fill="none" stroke="#0ea5e9" strokeWidth="2" opacity="0.6"/>
            <path d="M 40 340 L 40 360 L 60 360" fill="none" stroke="#0ea5e9" strokeWidth="2" opacity="0.6"/>
            <path d="M 360 340 L 360 360 L 340 360" fill="none" stroke="#0ea5e9" strokeWidth="2" opacity="0.6"/>

          </svg>
        </div>

        {/* Typography */}
        <div className="text-center">
          <h1
            className="text-5xl font-light tracking-widest text-slate-100"
            style={{ fontFamily: "'IBM Plex Mono', monospace" }}
          >
            SPRINT <span className="text-sky-400">&</span> DRIFT
          </h1>
          <p
            className="mt-4 text-sm tracking-[0.3em] text-slate-500 uppercase"
            style={{ fontFamily: "'IBM Plex Mono', monospace" }}
          >
            Notes from the judgment layer
          </p>
        </div>

        {/* Wide header version */}
        <div className="mt-16 w-full max-w-4xl">
          <svg
            width="100%"
            height="120"
            viewBox="0 0 800 120"
            className="drop-shadow-xl"
            preserveAspectRatio="xMidYMid meet"
          >
            <defs>
              <linearGradient id="headerBg" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#0f172a" />
                <stop offset="50%" stopColor="#1e293b" />
                <stop offset="100%" stopColor="#0f172a" />
              </linearGradient>
              <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.1"/>
                <stop offset="20%" stopColor="#0ea5e9" />
                <stop offset="50%" stopColor="#38bdf8" />
                <stop offset="80%" stopColor="#38bdf8" stopOpacity="0.3"/>
                <stop offset="100%" stopColor="#0ea5e9" stopOpacity="0.1"/>
              </linearGradient>
            </defs>

            <rect width="800" height="120" fill="url(#headerBg)"/>

            {/* Subtle grid */}
            <pattern id="headerGrid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#334155" strokeWidth="0.5" opacity="0.2"/>
            </pattern>
            <rect width="800" height="120" fill="url(#headerGrid)"/>

            {/* Extended waveform across header */}
            <path
              d="M 0 60
                 L 50 60 L 70 30 L 90 90 L 110 45 L 130 75 L 150 60
                 L 200 60 L 220 25 L 240 95 L 260 40 L 280 80 L 300 60
                 Q 350 50 400 60
                 Q 450 70 500 60
                 Q 550 55 600 60
                 Q 650 62 700 60
                 L 800 60"
              fill="none"
              stroke="url(#waveGrad)"
              strokeWidth="2"
              strokeLinecap="round"
            />

            {/* Nodes */}
            <circle cx="150" cy="60" r="4" fill="#0ea5e9"/>
            <circle cx="300" cy="60" r="5" fill="#38bdf8"/>
            <circle cx="500" cy="60" r="3" fill="#38bdf8" opacity="0.5"/>
            <circle cx="700" cy="60" r="2" fill="#38bdf8" opacity="0.3"/>

          </svg>
        </div>

      </div>
    </div>
  );
}
