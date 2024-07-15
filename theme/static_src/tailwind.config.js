const colors = require('./tailwind.colors');

module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        // '../../**/*.js', // Uncomment if needed
        // '../../**/*.py' // Uncomment if needed
    ],
    darkMode: 'class', // or 'media' if you prefer
    theme: {
        extend: {
            colors: {
                black: colors.black,
                white: colors.white,
                neutral: colors.neutral.light,
                primary: colors.primary.light,
                secondary: colors.secondary,
                danger: colors.danger,
                warning: colors.warning,
                success: colors.success,
                info: colors.info,
                'dark-neutral': colors.neutral.dark,
                'dark-primary': colors.primary.dark,
            },
        }
    },
    variants: {
        extend: {
            backgroundColor: ['dark', 'dark:hover'],
            textColor: ['dark'],
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('autoprefixer'),
    ],
};
