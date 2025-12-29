document.addEventListener('DOMContentLoaded', () => {
    const featuredStep = document.querySelector('.step.featured');

    // Create extra glowing particles for the featured node
    for (let i = 0; i < 5; i++) {
        const particle = document.createElement('div');
        particle.className = 'glow-particle';
        featuredStep.appendChild(particle);

        const size = Math.random() * 4 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 2}s`;
    }
});

// Add CSS for particles dynamically
const style = document.createElement('style');
style.textContent = `
    .glow-particle {
        position: absolute;
        background: var(--accent-gold);
        border-radius: 50%;
        pointer-events: none;
        box-shadow: 0 0 10px var(--accent-gold);
        animation: float 3s ease-in-out infinite;
        opacity: 0;
    }

    @keyframes float {
        0% { transform: translateY(0); opacity: 0; }
        50% { opacity: 0.6; }
        100% { transform: translateY(-50px); opacity: 0; }
    }
`;
document.head.appendChild(style);
