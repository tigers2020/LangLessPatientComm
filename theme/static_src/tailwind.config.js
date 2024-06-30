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
            colors: {
                primary: {
                    50: '#F0F7FD',
                    100: '#DCEEF9',
                    200: '#B9DEF3', // Hospital blue color
                    300: '#8ACEEA',
                    400: '#59BEE1',
                    500: '#2AAED7',
                    600: '#1D88AC',
                    700: '#146580',
                    800: '#0D4758',
                    900: '#072B34',
                },
                secondary: {
                    50: '#FDF6F2',
                    100: '#FBEFE5',
                    200: '#F6D2C4', // Complementary to primary, but not blue
                    300: '#EEB59C',
                    400: '#E48D6A',
                    500: '#DA6641',
                    600: '#C03F22',
                    700: '#9A311A',
                    800: '#752415',
                    900: '#4E1710',
                },

            },
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
    ],
}
