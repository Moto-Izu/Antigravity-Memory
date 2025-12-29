import React, { useRef } from 'react';
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';
import { PersonaInsights } from './constants/personas';
import { Hexagon, ChevronDown } from 'lucide-react';

function App() {
    const containerRef = useRef(null);
    const { scrollYProgress } = useScroll({
        target: containerRef,
        offset: ["start start", "end end"]
    });

    const rotate = useTransform(scrollYProgress, [0, 1], [0, 360 * 2]);
    const scale = useSpring(useTransform(scrollYProgress, [0, 0.2], [0.8, 1]));

    return (
        <div ref={containerRef} className="spiral-container">
            {/* Background Spiral Decoration */}
            <motion.div
                style={{ rotate }}
                className="fixed inset-0 flex items-center justify-center opacity-10 pointer-events-none"
            >
                <Hexagon className="w-[800px] h-[800px] text-white" strokeWidth={0.5} />
            </motion.div>

            {/* Hero Section */}
            <section className="h-screen flex flex-col items-center justify-center text-center px-4">
                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    className="text-6xl md:text-8xl font-bold title-gradient mb-4"
                >
                    AIZU SAZAEDO
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                    className="text-xl text-gray-400 max-w-2xl"
                >
                    1796. The Double-Helix Miracle. <br />
                    Where ancient engineering meets eternal scalability.
                </motion.p>
                <motion.div
                    animate={{ y: [0, 10, 0] }}
                    transition={{ repeat: Infinity, duration: 2 }}
                    className="mt-12 opacity-50"
                >
                    <ChevronDown className="w-8 h-8" />
                </motion.div>
            </section>

            {/* Content Cards */}
            <div className="relative z-10 py-20">
                {PersonaInsights.map((persona, index) => (
                    <motion.div
                        key={persona.name}
                        initial={{ opacity: 0, x: index % 2 === 0 ? -100 : 100 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ margin: "-100px" }}
                        className="glass-card"
                    >
                        <div className={`persona-badge ${persona.badgeClass}`}>
                            {persona.role}
                        </div>
                        <div className="flex items-center gap-3 mb-4">
                            <span className="text-accent-gold">{persona.icon}</span>
                            <h2 className="text-2xl font-bold">{persona.name}</h2>
                        </div>
                        <p className="text-gray-300 mb-6 leading-relaxed italic">
                            "{persona.analysis}"
                        </p>
                        <div className="stat-grid">
                            <div className="stat-item">
                                <div className="text-xs text-secondary mb-1">Constraint</div>
                                <div className="text-sm border-t border-glass-border pt-1">
                                    {persona.constraint}
                                </div>
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* Footer / CTA */}
            <section className="h-screen flex flex-col items-center justify-center">
                <motion.div
                    style={{ scale }}
                    className="glass-card text-center"
                >
                    <h2 className="text-3xl font-bold mb-4">Architecture is Destiny.</h2>
                    <p className="text-gray-400 mb-8">
                        The Sazaedo spirit lives in every line of code we write today.
                        Scalable. Minimalist. Integrated.
                    </p>
                    <button
                        className="px-8 py-3 bg-white text-black font-bold rounded-lg hover:bg-gold-500 transition-colors"
                        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                    >
                        Ascend Again
                    </button>
                </motion.div>
            </section>

            {/* Floating Progress Bar */}
            <motion.div
                className="fixed bottom-0 left-0 right-0 h-1 bg-accent-gold origin-left z-50"
                style={{ scaleX: scrollYProgress }}
            />
        </div>
    );
}

export default App;
