/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./static/js/*.js"
  ],
  theme: {
    fontFamily: {
      'LeckerliOne': ['"Leckerli One"', 'cursive'],
      'Praise': ['Praise', 'cursive'],
      'DMSans': ['"DM Sans"', 'sans']
    },
    extend: {
      colors: {
        'nuxt-pink': '#bcb2cc',
        'deep-purp': '#140836'
      },
    },
  },
  plugins: [],
}
