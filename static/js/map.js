import { DEFAULT_HERITAGE_CENTER,MAP_TILE_URL } from './config.js';
import { experience } from './heritage.js';
let map;
export function drawMap(sites) {
    if (!window.L || !document.getElementById('map'))return;
    if (map)map.remove();
    map=L.map('map').setView(DEFAULT_HERITAGE_CENTER,6);
    L.tileLayer(MAP_TILE_URL, {
        attribution:'© OpenStreetMap contributors'
    }).addTo(map);
    sites.filter(s=>s.latitude && s.longitude).forEach(s=>L.marker([s.latitude,s.longitude]).addTo(map).bindPopup(`<b>${s.name}</b><br>${s.region}<br><a href="#" data-map-site="${s.id}">Open experience</a>`));
    document.querySelectorAll('[data-map-site]').forEach(link=>link.addEventListener('click',e=> {
        e.preventDefault();
        experience(Number(link.dataset.mapSite))
    }))
}
