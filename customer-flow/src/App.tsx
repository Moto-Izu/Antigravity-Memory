import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ChevronDown,
  Upload,
  Library,
  CreditCard,
  Check,
  Download,
  Sparkles,
  Zap,
  Target
} from 'lucide-react';

const cn = (...classes: (string | boolean | undefined)[]) => classes.filter(Boolean).join(' ');

// --- Types ---
type AppState = 'IDLE' | 'PROCESSING' | 'COMPOSITE' | 'UPSCALING' | 'RESULT';

// --- Sub-components ---

const Navbar = () => (
  <nav className="fixed top-0 left-0 right-0 h-16 z-50 bg-black border-b border-white/5 flex items-center justify-between px-6">
    <div className="flex items-center gap-8">
      <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center overflow-hidden">
        <div className="w-full h-full bg-gradient-to-br from-indigo-600 to-black flex items-center justify-center">
          <span className="text-white font-black text-xl leading-none italic">n</span>
        </div>
      </div>
      <div className="hidden lg:flex items-center gap-6 text-[11px] font-black text-gray-400 uppercase tracking-widest">
        <span className="text-white">Nano Banana Pro 3</span>
        <div className="w-[1px] h-4 bg-white/10" />
        <a href="#" className="hover:text-white transition-colors">Neural Engine</a>
        <a href="#" className="hover:text-white transition-colors">Synthesis</a>
        <a href="#" className="hover:text-white transition-colors">Upscale</a>
      </div>
    </div>
    <div className="flex items-center gap-4">
      <div className="flex items-center gap-2 bg-white/5 px-4 py-1.5 rounded-full border border-white/10 text-[11px] font-black text-blue-400 uppercase tracking-tighter">
        <Zap size={12} fill="currentColor" />
        Protocol active
      </div>
      <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-gray-700 to-gray-900 border border-white/20 flex items-center justify-center font-bold text-[10px] text-white">
        AG
      </div>
    </div>
  </nav>
);

const ProcessingOverlay = ({ message }: { message: string }) => (
  <motion.div
    initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
    className="flex flex-col items-center gap-6"
  >
    <div className="relative">
      <motion.div
        animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
        className="w-24 h-24 border-2 border-white/5 border-t-white rounded-full"
      />
      <motion.div
        animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 1.5 }}
        className="absolute inset-0 flex items-center justify-center"
      >
        <Sparkles className="text-blue-500" size={32} />
      </motion.div>
    </div>
    <div className="text-center">
      <p className="text-white font-black tracking-[0.3em] uppercase text-sm mb-2">{message}</p>
      <div className="flex gap-1 justify-center">
        {[...Array(3)].map((_, i) => (
          <motion.div
            key={i} animate={{ opacity: [0, 1, 0] }}
            transition={{ repeat: Infinity, duration: 1, delay: i * 0.2 }}
            className="w-1.5 h-1.5 bg-blue-500 rounded-full"
          />
        ))}
      </div>
    </div>
  </motion.div>
);

const Stepper = ({ current }: { current: AppState }) => {
  const steps = [
    { label: "Upload", active: current === 'IDLE' || current === 'PROCESSING' },
    { label: "Synthesis", active: current === 'COMPOSITE' || current === 'UPSCALING' },
    { label: "Upscale", active: current === 'RESULT' },
  ];

  return (
    <div className="flex items-center gap-6 mb-12">
      {steps.map((s, i) => (
        <div key={i} className="flex items-center gap-3">
          <div className={cn(
            "w-2 h-2 rounded-full",
            s.active ? "bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.8)]" : "bg-white/10"
          )} />
          <span className={cn(
            "text-[10px] font-black uppercase tracking-[0.2em]",
            s.active ? "text-white" : "text-gray-600"
          )}>{s.label}</span>
          {i < steps.length - 1 && <div className="w-8 h-[1px] bg-white/5 ml-3" />}
        </div>
      ))}
    </div>
  );
};

// --- Virtual Camera Configuration ---
const CAMERA_ANGLES = [
  { label: "Establishing Shot", style: { objectPosition: "center", transform: "scale(1)" } },
  { label: "Medium Shot (L)", style: { objectPosition: "20% 40%", transform: "scale(1.8)" } },
  { label: "Medium Shot (R)", style: { objectPosition: "80% 40%", transform: "scale(1.8)" } },
  { label: "Low Angle", style: { objectPosition: "50% 100%", transform: "scale(1.4) translateY(-10%)" } },
  { label: "High Angle", style: { objectPosition: "50% 0%", transform: "scale(1.4) translateY(10%)" } },
  { label: "Extreme Close-Up", style: { objectPosition: "center", transform: "scale(2.5)" } },
  { label: "Dutch Tilt (L)", style: { objectPosition: "40% 60%", transform: "scale(1.5) rotate(-5deg)" } },
  { label: "Dutch Tilt (R)", style: { objectPosition: "60% 60%", transform: "scale(1.5) rotate(5deg)" } },
  { label: "Insert Detail", style: { objectPosition: "80% 80%", transform: "scale(2.2)" } },
];

// --- Main Application ---

function App() {
  const [state, setState] = useState<AppState>('IDLE');
  const [seedImage, setSeedImage] = useState<string | null>(null);
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const url = URL.createObjectURL(file);
    setSeedImage(url);
    startSynthesis();
  };

  const startSynthesis = () => {
    setState('PROCESSING');
    setTimeout(() => setState('COMPOSITE'), 2500);
  };

  const startUpscale = () => {
    setState('UPSCALING');
    setTimeout(() => setState('RESULT'), 3000);
  };

  const triggerUpload = () => {
    fileInputRef.current?.click();
  };

  return (
    <main className="min-h-screen bg-[#030303] text-white flex flex-col font-sans selection:bg-blue-500/30 overflow-hidden">
      <Navbar />

      <div className="flex-1 flex flex-col items-center justify-center pt-16 relative">
        {/* Background Atmosphere */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60%] h-[60%] bg-blue-600/[0.02] blur-[160px] rounded-full" />
        </div>

        <AnimatePresence mode="wait">
          {state === 'IDLE' && (
            <motion.div
              key="idle" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.95 }}
              className="max-w-2xl w-full px-6 flex flex-col items-center"
            >
              <Stepper current={state} />
              <div className="mb-12 text-center">
                <h1 className="text-7xl md:text-8xl font-black tracking-tighter italic mb-6">SHOTS</h1>
                <p className="text-gray-500 text-sm font-bold uppercase tracking-[0.3em]">Neural Composite Synthesis</p>
              </div>

              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                accept="image/*"
                onChange={handleFileUpload}
              />

              <div
                onClick={triggerUpload}
                className="w-full h-80 bg-white/[0.02] border border-white/5 rounded-[4rem] flex flex-col items-center justify-center gap-8 hover:bg-white/[0.04] hover:border-blue-500/20 transition-all cursor-pointer group shadow-2xl relative overflow-hidden"
              >
                <div className="w-20 h-20 rounded-full bg-white text-black flex items-center justify-center shadow-[0_20px_40px_rgba(255,255,255,0.1)] group-hover:scale-110 transition-transform relative z-10">
                  <Upload size={32} />
                </div>
                <div className="text-center relative z-10">
                  <p className="font-black uppercase tracking-[0.3em] text-[11px] text-gray-400">Initialize Upload Protocol</p>
                  <p className="mt-2 text-[9px] text-gray-600 font-bold tracking-widest uppercase">Drop Source Material Here</p>
                </div>
              </div>
            </motion.div>
          )}

          {state === 'PROCESSING' && (
            <div className="relative flex flex-col items-center justify-center">
              {/* Seed Image Feedback */}
              {seedImage && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 0.4, scale: 1 }}
                  exit={{ opacity: 0 }}
                  className="absolute inset-0 w-64 h-64 mx-auto my-auto rounded-3xl overflow-hidden border border-white/10 opacity-30 blur-sm top-1/2 -translate-y-1/2"
                >
                  <img src={seedImage} className="w-full h-full object-cover grayscale" alt="Seed" />
                </motion.div>
              )}
              <ProcessingOverlay key="proc" message="Ingesting Seed... Neural Synthesis Active" />
            </div>
          )}

          {state === 'COMPOSITE' && (
            <motion.div
              key="composite" initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }}
              className="max-w-4xl w-full px-6 flex flex-col items-center"
            >
              <Stepper current={state} />

              <div className="relative mb-12 group">
                <div className="grid grid-cols-3 gap-1 p-2 bg-white/5 rounded-[3rem] overflow-hidden border border-white/10 shadow-[0_50px_100px_-20px_rgba(0,0,0,1)]">
                  {CAMERA_ANGLES.map((angle, i) => (
                    <div key={i} className="aspect-square bg-gray-900 overflow-hidden relative group/item">
                      {/* The Sliced Seed Image */}
                      {seedImage && (
                        <img
                          src={seedImage}
                          style={angle.style}
                          className="absolute inset-0 w-full h-full object-cover transition-transform duration-700"
                          alt={angle.label}
                        />
                      )}
                      {/* Angle Label on Hover */}
                      <div className="absolute inset-0 bg-black/50 opacity-0 group-hover/item:opacity-100 flex items-center justify-center transition-opacity duration-300">
                        <span className="text-[9px] font-black uppercase tracking-widest text-white border border-white/20 px-2 py-1 rounded-full backdrop-blur-md">
                          {angle.label}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
                {/* Tactical HUD Overlay */}
                <div className="absolute -top-4 -left-4 px-4 py-1.5 bg-blue-600 text-white text-[9px] font-black rounded uppercase tracking-widest shadow-lg">
                  Composite_Ready
                </div>
              </div>

              <div className="flex flex-col items-center gap-6">
                <p className="text-gray-500 text-xs font-bold uppercase tracking-[0.3em]">9 Cinematic Angles Synthesized in 1.2s</p>
                <button
                  onClick={startUpscale}
                  className="bg-white text-black px-16 py-6 rounded-full font-black uppercase text-sm tracking-[0.4em] shadow-[0_20px_40px_rgba(255,255,255,0.1)] hover:scale-105 active:scale-95 transition-all"
                >
                  Initiate 4K Upscale
                </button>
              </div>
            </motion.div>
          )}

          {state === 'UPSCALING' && (
            <ProcessingOverlay key="upscale" message="Neural Upscaling... High-Dynamic Expansion" />
          )}

          {state === 'RESULT' && (
            <motion.div
              key="res" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="max-w-7xl w-full px-6 flex flex-col items-center"
            >
              <Stepper current={state} />

              <div className="relative w-full aspect-video bg-black rounded-[4rem] overflow-hidden border border-white/10 shadow-[0_100px_150px_-50px_rgba(0,0,0,1)] flex items-center justify-center p-8 group">
                {/* The actual result: The 3x3 Grid but CRISP and 4K style */}
                <div className="grid grid-cols-3 gap-1 w-full max-w-[800px] rounded-[2rem] overflow-hidden shadow-2xl relative">
                  {CAMERA_ANGLES.map((angle, i) => (
                    <div key={i} className="aspect-square bg-gray-900 border-[0.5px] border-white/5 relative overflow-hidden">
                      {/* Re-render the sliced image for the final result */}
                      {seedImage && (
                        <img
                          src={seedImage}
                          style={angle.style}
                          className="absolute inset-0 w-full h-full object-cover"
                          alt={angle.label}
                        />
                      )}
                    </div>
                  ))}
                  {/* Gloss Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-tr from-blue-600/10 to-transparent pointer-events-none mix-blend-overlay" />
                </div>

                {/* Status UI */}
                <div className="absolute top-12 left-12 flex flex-col gap-3">
                  <div className="bg-blue-600 text-white text-[10px] font-black px-4 py-1.5 rounded-full flex items-center gap-2 shadow-xl">
                    <Target size={12} /> 4K_MASTERY_ACTIVE
                  </div>
                  <div className="bg-white/5 backdrop-blur-xl border border-white/10 text-gray-400 text-[8px] font-black px-4 py-1.5 rounded-full tracking-widest">
                    RESOLUTION: 7680 x 4320
                  </div>
                </div>
              </div>

              <div className="mt-12 flex gap-8">
                <button
                  onClick={() => { setState('IDLE'); setSeedImage(null); }}
                  className="px-12 py-6 rounded-full bg-white/5 border border-white/10 font-black uppercase text-[11px] tracking-[0.3em] hover:bg-white/10 transition-all text-gray-400"
                >
                  New Protocol
                </button>
                <button className="px-16 py-6 rounded-full bg-white text-black font-black uppercase text-[11px] tracking-[0.3em] shadow-2xl flex items-center gap-3 hover:scale-105 active:scale-95 transition-all">
                  <Download size={18} /> Export 4K Composite
                </button>
              </div>
            </motion.div>
          )}

        </AnimatePresence>
      </div>

      {/* Footer System Info */}
      <footer className="h-12 flex items-center justify-between px-10 text-[8px] font-black text-gray-800 uppercase tracking-[0.5em] border-t border-white/5">
        <div className="flex gap-12">
          <span>Core: Omni-11</span>
          <span>Engine: Nano Banana Pro 3</span>
        </div>
        <div className="flex gap-12">
          <span>Latency: 0.004s</span>
          <span>Integrity: Stable</span>
        </div>
      </footer>
    </main>
  );
}

export default App;
