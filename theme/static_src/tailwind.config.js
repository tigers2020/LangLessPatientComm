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
                black: '#000000',
                white: '#FFFFFF',
                neutral: {
                    50: '#FAFAFA',
                    100: '#F5F5F5',
                    200: '#EEEEEE',
                    300: '#E1E1E1',
                    400: '#CACACA',
                    500: '#8E8E8E',
                    600: '#4B4B4B',
                    700: '#1F1F1F',
                },
                primary: {
                    50: '#FFFDF2',
                    100: '#FCFAEB',
                    200: '#F7F5E8',
                    300: '#F4F4EA',
                    400: '#F4F1E6',
                    500: '#F2EFE3',
                    600: '#F2EFE4',
                    700: '#F2E0E6',
                },
                secondary: {
                    50: '#FFF6EE',
                    100: '#FFF3CB',
                    200: '#FFD6B2',
                    300: '#FFC99A',
                    400: '#FFB677',
                    500: '#FFAC64',
                    600: '#FF9407',
                    700: '#F07000',
                },
                danger: {
                    50: '#FFFBFB',
                    100: '#FFD7E0',
                    200: '#FFEBEE',
                    300: '#FFCCD2',
                    400: '#F49898',
                    500: '#EB6F70',
                    600: '#F64C4C',
                    700: '#EC2D30',
                },
                warning: {
                    50: '#FFFDFA',
                    100: '#FFF9EE',
                    200: '#FFF7E1',
                    300: '#FFEAB3',
                    400: '#FFDD82',
                    500: '#FFC62B',
                    600: '#FFAD0D',
                    700: '#FE9B0E',
                },
                success: {
                    50: '#FBFEFC',
                    100: '#F2FAF6',
                    200: '#E5F5EC',
                    300: '#00D4B4',
                    400: '#97D4B4',
                    500: '#6BC497',
                    600: '#47B881',
                    700: '#0C9D61',
                },
                info: {
                    50: '#F8FCFF',
                    100: '#F1F8FF',
                    200: '#E4F2FF',
                    300: '#BDDDFF',
                    400: '#93C8FF',
                    500: '#4BA1FF',
                    600: '#3B82F6',
                    700: '#3A70E2',
                }
            }
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
}
