const loginForm=document.getElementById('loginForm');
const registerForm=document.getElementById('registerForm');
loginForm?.addEventListener('submit',async e=> {
    e.preventDefault();
    const r=await fetch('/api/auth/login', {
        method:'POST',headers: {
            'Content-Type':'application/json'
        },body:JSON.stringify( {
            email:document.getElementById('email').value,password:document.getElementById('password').value
        })
    });
    const d=await r.json();
    const msg=document.getElementById('msg');
    if (!r.ok) {
        msg.textContent=d.detail || 'Login failed';
        return
    }
    localStorage.setItem('sankofa_token',d.access_token);
    location.href='/';
});
registerForm?.addEventListener('submit',async e=> {
    e.preventDefault();
    const r=await fetch('/api/auth/register', {
        method:'POST',headers: {
            'Content-Type':'application/json'
        },body:JSON.stringify( {
            first_name:document.getElementById('first_name').value,last_name:document.getElementById('last_name').value,email:document.getElementById('email').value,password:document.getElementById('password').value
        })
    });
    const d=await r.json();
    const msg=document.getElementById('msg');
    if (!r.ok) {
        msg.textContent=d.detail || 'Registration failed';
        return
    }
    msg.style.color='#176b45';
    msg.textContent='Account created. Redirecting to login...';
    setTimeout(()=>location.href='/login.html',800)
});
