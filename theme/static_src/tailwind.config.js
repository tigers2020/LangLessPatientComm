/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    darkMode: 'class', // or 'media' if you prefer

    theme: {
        extend: {
            maxWidth: {
                'custom': '1274.9px',
            },
            colors: {
                primary: {
                    50: '#e6eae9',
                    100: '#ccd5d3',
                    200: '#99aba7',
                    300: '#66817b',
                    400: '#33574f',
                    500: '#1A3129', // Main primary color
                    600: '#152722',
                    700: '#101d1a',
                    800: '#0a1311',
                    900: '#050a09',
                },
                secondary: {
                    50: '#f9fdf0',
                    100: '#f3fbe1',
                    200: '#e7f7c3',
                    300: '#dbf3a5',
                    400: '#CBEA7B', // Main secondary color
                    500: '#b9d66f',
                    600: '#93ab59',
                    700: '#6e8043',
                    800: '#4a562c',
                    900: '#252b16',
                },
                tertiary: {
                    50: '#fdfef9',
                    100: '#FAFDF2', // Main tertiary color
                    200: '#f5fbe6',
                    300: '#f0f9d9',
                    400: '#ebf7cc',
                    500: '#d3deb7',
                    600: '#a8b292',
                    700: '#7e856e',
                    800: '#545949',
                    900: '#2a2c25',
                },
                accent: {
                    50: '#fcfdf7',
                    100: '#F6FBE9', // Main accent color
                    200: '#edf7d3',
                    300: '#e4f3bd',
                    400: '#dbefa7',
                    500: '#c5d696',
                    600: '#9eab78',
                    700: '#76805a',
                    800: '#4f563c',
                    900: '#272b1e',
                },
                highlight: {
                    50: '#e7eae9',
                    100: '#cfd5d3',
                    200: '#9faba7',
                    300: '#6f817b',
                    400: '#3f574f',
                    500: '#2b4a3f',
                    600: '#234338', // Main highlight color
                    700: '#1b332c',
                    800: '#122220',
                    900: '#091110',
                },
                warning: {
                    50: '#fef7f1',
                    100: '#fdefe3',
                    200: '#fbdfc7',
                    300: '#f9cfab',
                    400: '#f1a159', // Main warning color
                    500: '#d9914f',
                    600: '#ad743f',
                    700: '#82572f',
                    800: '#563a20',
                    900: '#2b1d10',
                },
            },
        },
    },
    variants: {
        extend: {
            backgroundColor: ['dark', 'dark:hover'],
            textColor: ['dark'],
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('autoprefixer'),
    ],
}
