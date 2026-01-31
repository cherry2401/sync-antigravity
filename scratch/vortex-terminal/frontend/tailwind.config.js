/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                terminal: {
                    bg: '#1a1b26',
                    fg: '#c0caf5',
                    accent: '#7aa2f7',
                    purple: '#bb9af7',
                    cyan: '#7dcfff',
                    green: '#9ece6a',
                    red: '#f7768e',
                }
            }
        },
    },
    plugins: [],
}
