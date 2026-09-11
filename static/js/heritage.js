import { apiFetch } from './api.js';
import { drawMap } from './map.js';
export async function loadSites() {
    const search=document.getElementById('search');
    const category=document.getElementById('category');
    if (!search || !category)return;
    const q=search.value;
    const categoryValue=category.value;
    let url='/api/sites?';
    if (q)url+=`q=${encodeURIComponent(q)}&`;
    if (categoryValue)url+=`category=${encodeURIComponent(categoryValue)}`;
    const res=await apiFetch(url);
    if (!res.ok)return;
    const sites=await res.json();
    const grid=document.getElementById('siteGrid');
    grid.innerHTML=sites.map(s=>`<article class="card"><img src="${s.image_url || 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=1200&q=80'}" alt="${s.name}"><div class="card-body"><span class="tag">${s.category}</span><h3>${s.name}</h3><p>${s.short_description}</p><button class="btn primary" data-site-id="${s.id}">Explore story</button></div></article>`).join('');
    grid.querySelectorAll('[data-site-id]').forEach(btn=>btn.addEventListener('click',()=>experience(Number(btn.dataset.siteId))));
    drawMap(sites)
}
export async function experience(id) {
    const r=await apiFetch('/api/sites/'+id);
    const s=await r.json();
    alert(`${s.name}\n\n${s.story}\n\nQR code: ${s.qr_code}\n\nSign in to scan the experience and earn passport points.`)
}
