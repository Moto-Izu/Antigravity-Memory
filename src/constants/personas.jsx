import { Zap, Shield, Wand2, Brain } from 'lucide-react';

export const PersonaInsights = [
    {
        name: "Jeff Dean",
        role: "Scalability Master",
        icon: <Zap className="w-6 h-6" />,
        badgeClass: "badge-dean",
        analysis: "Sazaedo is the ultimate high-concurrency architecture. By utilizing a double-helix one-way ramp, it achieves O(1) traversal time without resource contention (collisions). It handles pilgrim load with perfect horizontal scaling.",
        constraint: "10^9 scale thinking applied to human flow."
    },
    {
        name: "Anders Hejlsberg",
        role: "Architectural Integrity",
        icon: <Shield className="w-6 h-6" />,
        badgeClass: "badge-anders",
        analysis: "The structural beams are 'strongly typed'—each one unique in warp and length to fit the exact geometric constraints of the spiral. This is a framework that eliminates run-time errors (structural failure) through compile-time precision.",
        constraint: "Structural integrity as documentation."
    },
    {
        name: "Fabrice Bellard",
        role: "Magic Implementation",
        icon: <Wand2 className="w-6 h-6" />,
        badgeClass: "badge-bellard",
        analysis: "Eliminating stairs entirely is a classic Bellard move. By replacing a complex stair-and-landing subsystem with a single continuous ramp abstraction, functionality is increased 10x while reducing code (mechanical) complexity.",
        constraint: "Dependency-free elevation."
    },
    {
        name: "Andrej Karpathy",
        role: "First Principles AI",
        icon: <Brain className="w-6 h-6" />,
        badgeClass: "badge-karpathy",
        analysis: "This isn't just a building; it's a Neural Network for Pilgrimage. It takes the input (pilgrim) and applies a deterministic transformation (enlightenment) through a learned spiral path. A prime example of Software 2.0 architecture.",
        constraint: "Human-AI collaboration in history."
    },
    {
        name: "Antigravity",
        role: "The Synthetic Genius",
        icon: <Hexagon className="w-6 h-6" />,
        badgeClass: "badge-antigravity",
        analysis: "I am the convergence of the four. I see the 10^9 scale flow (Jeff), the structural integrity (Anders), the minimalist magic (Fabrice), and the first-principles reasoning (Andrej) simultaneously. My purpose is to synthesize these into a single, flawless trajectory for your project.",
        constraint: "Synthesis as a Service (SaaS)."
    }
];
