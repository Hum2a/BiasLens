module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        blue: {
          100: "#bfdbfe", // Lighter blue
          200: "#93c5fd", // Hover blue
        },
        red: {
          100: "#fecaca", // Lighter red
          200: "#fca5a5", // Hover red
        },
        gray: {
          100: "#f3f4f6", // Lighter gray
          200: "#e5e7eb", // Hover gray
        },
      },
    },
  },
  plugins: [],
};
