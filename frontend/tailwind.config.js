/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#52b788',  // Light Green
          DEFAULT: '#2d6a4f', // Jungle Green
          dark: '#1b4332',   // Dark Slate Green
        },
        secondary: {
          light: '#d8f3dc',  // Mint Cream
          DEFAULT: '#b7e4c7', // Pale Green
        },
        accent: {
          DEFAULT: '#e9c46a', // Saffron
          hover: '#f4a261',
        },
        soil: {
          light: '#d4a373',
          DEFAULT: '#bc6c25', // Earth Brown
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
