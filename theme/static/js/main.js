// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const html = document.documentElement;

    function setDarkMode(isDark) {
        html.classList.toggle('dark', isDark);
        localStorage.setItem('darkMode', isDark);
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            const isDark = !html.classList.contains('dark');
            setDarkMode(isDark);
        });
    }

    // Initialize dark mode based on localStorage
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(isDarkMode);
});

document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const mainWrapper = document.getElementById('main-wrapper');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const closeSidebar = document.getElementById('close-sidebar');

    function toggleSidebar() {
        sidebar.classList.toggle('-translate-x-full');
        mainWrapper.classList.toggle('ml-64');
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }

    if (closeSidebar) {
        closeSidebar.addEventListener('click', toggleSidebar);
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(event) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggleButton = sidebarToggle.contains(event.target);
        if (!isClickInsideSidebar && !isClickOnToggleButton && window.innerWidth < 1024) {
            sidebar.classList.add('-translate-x-full');
            mainWrapper.classList.remove('ml-64');
        }
    });
});
