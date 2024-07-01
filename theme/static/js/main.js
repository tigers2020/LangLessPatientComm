// static/js/main.js

// Dark mode toggle functionality
document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const html = document.documentElement;

    function setDarkMode(isDark) {
        html.classList.toggle('dark', isDark);
        localStorage.setItem('darkMode', isDark);
    }

    darkModeToggle.addEventListener('click', () => {
        const isDark = !html.classList.contains('dark');
        setDarkMode(isDark);
    });
});

// Add any other global JavaScript functionality here