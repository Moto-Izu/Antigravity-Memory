/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        apple: {
          red: '#DC143C',
          black: '#000000',
          grey: '#666666',
          silver: '#F5F5F7',
        }
      },
      fontFamily: {
        sans: ['Inter', 'Noto Sans JP', 'sans-serif'],
      },
      fontSize: {
        'hero': ['clamp(3.5rem, 10vw, 8rem)', { lineHeight: '1', fontWeight: '900', letterSpacing: '-0.02em' }],
      },
      spacing: {
        'break': '20vh',
      }
    },
  },
  plugins: [],
}
