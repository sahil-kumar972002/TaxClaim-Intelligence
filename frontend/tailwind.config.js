/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        brand: {
          dark: "#080C14",
          navy: "#0F172A",
          card: "#131C31",
          cardHover: "#18233C",
          border: "#1E293B",
          borderGlow: "#334155",
          primary: "#6366F1",
          primaryHover: "#4F46E5",
          accent: "#06B6D4",
          accentGlow: "#0891B2",
          emerald: "#10B981",
          amber: "#F59E0B",
          rose: "#F43F5E",
          purple: "#8B5CF6"
        }
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"]
      },
      boxShadow: {
        glow: "0 0 25px -5px rgba(99, 102, 241, 0.25)",
        glowCyan: "0 0 25px -5px rgba(6, 182, 212, 0.25)",
        glass: "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
      },
      backdropBlur: {
        xs: "2px"
      }
    },
  },
  plugins: [],
}
