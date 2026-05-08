/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bgMain: "#0f141e",
        bgDark: "#080b12",
        primaryCyan: "#00E5FF",
        borderLight: "rgba(255,255,255,0.1)",
        textMain: "#E0E0E0",
        textMuted: "#A0A0A0"
      }
    },
  },
  plugins: [],
}
