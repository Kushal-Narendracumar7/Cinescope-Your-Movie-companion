document.addEventListener('DOMContentLoaded', () => {
    // Get the current page URL
    const currentPath = window.location.pathname;

    // Select all sidebar menu items
    const menuItems = document.querySelectorAll('.sidebar-menu a');

    // Remove any existing active class
    menuItems.forEach(item => {
        item.classList.remove('active');
    });

    // Find and add active class to the matching menu item
    menuItems.forEach(item => {
        const href = item.getAttribute('href');
        
        // Normalize paths to handle different URL formats
        const normalizePath = (path) => {
            return path.endsWith('/') ? path.slice(0, -1) : path;
        };

        // Check if the current path matches the menu item's href
        if (
            normalizePath(currentPath) === normalizePath(href) || 
            currentPath.includes(href)
        ) {
            item.classList.add('active');
        }
    });
});