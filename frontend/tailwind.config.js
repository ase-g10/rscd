/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    // other paths that contain your tailwind classes
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
