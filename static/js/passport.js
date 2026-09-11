import { getToken } from './api.js';
export async function loadPassport() {
    const token=getToken();
    if (!token)return;
    const r=await fetch('/api/passport', {
        headers: {
            Authorization:`Bearer ${token}`
        }
    });
    if (!r.ok)return;
    const d=await r.json();
    const points=document.getElementById('points');
    const badges=document.getElementById('badges');
    if (points)points.textContent=d.points;
    if (badges)badges.innerHTML=d.badges.length?d.badges.map(b=>`<div>${b.name}</div>`).join(''):'No badges yet.'
}
