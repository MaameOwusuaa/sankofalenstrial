import { getToken, logout } from './api.js';

export function initNavbar() {
    const token = getToken();
    
    // Hide elements that require auth if not logged in
    document.querySelectorAll('[data-auth-required]').forEach(el => {
        if (!token) el.style.display = 'none'
    });
    
    // Update auth link
    const authLink = document.getElementById('authLink');
    if (authLink) {
        if (token) {
            authLink.textContent = 'Logout';
            authLink.href = '#';
            authLink.onclick = (e) => {
                e.preventDefault();
                logout();
                window.location.href = '/';
            };
        } else {
            authLink.textContent = 'Login';
            authLink.href = '/login.html';
        }
    }
    
    // Highlight active navigation link
    updateActiveNavLink();
}

function updateActiveNavLink() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        const href = link.getAttribute('href');
        let isActive = false;
        
        if (href === '/passport.html' && (currentPath === '/passport.html' || currentPath.endsWith('passport.html'))) {
            isActive = true;
        } else if (href === '/explore.html' && (currentPath === '/explore.html' || currentPath.endsWith('explore.html'))) {
            isActive = true;
        } else if ((href === '/' || href === '/#discover') && 
                   (currentPath === '/' || currentPath === '/index.html' || currentPath === '')) {
            isActive = true;
        }
        
        if (isActive) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}
