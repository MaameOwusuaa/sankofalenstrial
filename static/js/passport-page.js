import { getToken } from './api.js';
import { initNavbar } from './navbar.js';

// Initialize page on load
document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    loadPassportPage();
});

export async function loadPassportPage() {
    const token = getToken();
    
    const authRequired = document.getElementById('auth-required');
    const passportContent = document.getElementById('passport-content');
    
    if (!token) {
        authRequired.style.display = 'block';
        passportContent.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch('/api/passport', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load passport');
        }
        
        const data = await response.json();
        
        // Hide auth message and show content
        authRequired.style.display = 'none';
        passportContent.style.display = 'block';
        
        // Populate visitor info
        populateVisitorInfo(data);
        
        // Populate stats
        populateStats(data);
        
        // Populate badges
        populateBadges(data.badges);
        
        // Populate recent stamps
        populateRecentStamps(data.recent_stamps);
        
        // Populate places in passport
        populatePlaces(data.all_places);
        
    } catch (error) {
        console.error('Error loading passport:', error);
        authRequired.style.display = 'block';
        passportContent.style.display = 'none';
    }
}

function populateVisitorInfo(data) {
    const name = document.getElementById('visitor-name');
    const email = document.getElementById('visitor-email');
    const initials = document.getElementById('visitor-initials');
    
    if (name) name.textContent = `${data.first_name} ${data.last_name}`;
    if (email) email.textContent = data.email;
    
    // Generate initials
    const first = data.first_name[0] || '';
    const last = data.last_name[0] || '';
    if (initials) initials.textContent = (first + last).toUpperCase();
}

function populateStats(data) {
    document.getElementById('total-stamps').textContent = data.points;
    document.getElementById('sites-visited').textContent = data.sites_visited;
    document.getElementById('badges-earned').textContent = data.total_badges;
}

function populateBadges(badges) {
    const container = document.getElementById('badges-container');
    
    if (!badges || badges.length === 0) {
        container.innerHTML = '<div class="empty-state">No badges yet. Start exploring!</div>';
        return;
    }
    
    container.innerHTML = badges.map(badge => `
        <div class="badge-card">
            <div class="badge-icon">🏆</div>
            <div class="badge-info">
                <h3>${escapeHtml(badge.name)}</h3>
                <p>${escapeHtml(badge.description)}</p>
                <small>${formatDate(badge.awarded_at)}</small>
            </div>
        </div>
    `).join('');
}

function populateRecentStamps(stamps) {
    const container = document.getElementById('recent-stamps-container');
    
    if (!stamps || stamps.length === 0) {
        container.innerHTML = '<div class="empty-state">No stamps yet. Visit a heritage site to get started!</div>';
        return;
    }
    
    container.innerHTML = stamps.map(stamp => `
        <div class="stamp-item">
            <div class="stamp-image">
                ${stamp.image_url ? `<img src="${stamp.image_url}" alt="${escapeHtml(stamp.site_name)}">` : '<div class="no-image">📸</div>'}
            </div>
            <div class="stamp-details">
                <h3>${escapeHtml(stamp.site_name)}</h3>
                <p class="stamp-region">${escapeHtml(stamp.region)} • ${escapeHtml(stamp.category)}</p>
                <p class="stamp-date">${formatDate(stamp.scanned_at)}</p>
            </div>
        </div>
    `).join('');
}

function populatePlaces(places) {
    const container = document.getElementById('places-container');
    
    if (!places || places.length === 0) {
        container.innerHTML = '<div class="empty-state">No visits yet. Explore heritage sites to add them to your passport!</div>';
        return;
    }
    
    // Remove duplicates by site_id (keep first occurrence)
    const seen = new Set();
    const uniquePlaces = places.filter(place => {
        if (seen.has(place.site_id)) return false;
        seen.add(place.site_id);
        return true;
    });
    
    container.innerHTML = uniquePlaces.map(place => `
        <div class="place-card">
            <div class="place-image">
                ${place.image_url ? `<img src="${place.image_url}" alt="${escapeHtml(place.site_name)}">` : '<div class="no-image">📍</div>'}
            </div>
            <div class="place-content">
                <h3>${escapeHtml(place.site_name)}</h3>
                <p class="place-category">${escapeHtml(place.category)}</p>
                <p class="place-description">${escapeHtml(place.short_description)}</p>
                <p class="place-region">📍 ${escapeHtml(place.region)}</p>
                <p class="place-visited">First visited: ${formatDate(place.scanned_at)}</p>
            </div>
        </div>
    `).join('');
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
