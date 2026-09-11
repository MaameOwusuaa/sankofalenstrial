import { getToken } from './api.js';
export async function askNaa() {
    const token=getToken();
    if (!token) {
        alert('Please sign in first.');
        location.href='/login.html';
        return
    }
    const input=document.getElementById('question');
    const log=document.getElementById('chatLog');
    const q=input?.value;
    if (!q || !log)return;
    const r=await fetch('/api/guide/ask', {
        method:'POST',headers: {
            'Content-Type':'application/json',Authorization:`Bearer ${token}`
        },body:JSON.stringify( {
            question:q
        })
    });
    const d=await r.json();
    log.innerHTML+=`<p><b>You:</b> ${q}</p><p class="naa"><b>Naa:</b> ${d.answer}</p>`;
    input.value=''
}
