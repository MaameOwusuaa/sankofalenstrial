export async function apiFetch(path,options= {
}) {
    return fetch(`${path}`,options)
}
export function getToken() {
    return localStorage.getItem('sankofa_token')
}
export function authHeaders() {
    const token=getToken();
    return token? {
        Authorization:`Bearer ${token}`
    }
    : {
    }
}
export function logout() {
    localStorage.removeItem('sankofa_token');
    localStorage.removeItem('sankofa_user');
}
