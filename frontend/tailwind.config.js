/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {},
	},
	plugins: [],
	theme: {
		fontFamily: {
			'sans': ['"Manrope Variable"', 'ui-sans-serif', 'system-ui'],
			'body': ['"Manrope Variable"']
		}
	}
}

