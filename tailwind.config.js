/** BaseDJ demo: tokens de la "cabina" */
module.exports = {
  content: ['./src/*.html'],
  theme: {
    extend: {
      colors: {
        ink: '#121013',      // sala
        booth: '#1B171C',    // superficie de cabina
        deck: '#252027',     // controles
        paper: '#E3DDD2',    // mesa iluminada donde se apoya el producto
        cream: '#F3EEE6',    // texto principal
        mute: '#A9A1A8',     // texto secundario (AA sobre ink)
        volt: '#F2E205',     // amarillo del logo BaseDJ
      },
      fontFamily: {
        display: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
      },
      maxWidth: { page: '1320px' },
    },
  },
  plugins: [],
};
