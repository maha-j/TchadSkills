const API_BASE = '/api/';
const TOKEN_KEY = 'tchadskills_token';
const REFRESH_KEY = 'tchadskills_refresh';
const USER_KEY = 'tchadskills_user';

function getAuthToken() {
    return localStorage.getItem(TOKEN_KEY);
}

function setAuthData(token, refresh, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(REFRESH_KEY, refresh);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
}

function clearAuthData() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
}

function getAuthUser() {
    return JSON.parse(localStorage.getItem(USER_KEY) || 'null');
}

async function fetchJson(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
    };

    const response = await fetch(url, {
        ...options,
        headers,
    });

    const body = await response.json().catch(() => null);
    return { response, body };
}

async function fetchCurrentUser(accessToken) {
    if (!accessToken) return null;
    const { response, body } = await fetchJson('me/', {
        headers: { Authorization: `Bearer ${accessToken}` },
    });
    return response.ok ? body : null;
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    if (!notification) {
        alert(message);
        return;
    }

    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3500);
}

function updateAuthUi() {
    const currentUser = getAuthUser();
    const loginLink = document.querySelector('a[href="/login/"]');
    const registerLink = document.querySelector('a[href="/register/"]');
    const logoutLink = document.querySelector('a[href="/logout/"]');

    if (currentUser) {
        if (loginLink) {
            loginLink.textContent = currentUser.username;
            loginLink.href = '/';
        }
        if (registerLink) {
            registerLink.style.display = 'none';
        }
        if (logoutLink) {
            logoutLink.style.display = 'inline-block';
        }
    }
}

async function handleLoginForm(event) {
    if (event) event.preventDefault();

    const username = document.getElementById('loginUsername')?.value.trim() || '';
    const password = document.getElementById('loginPassword')?.value || '';
    const button = document.getElementById('loginBtn');
    const errorDiv = document.getElementById('loginError');

    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
    if (button) {
        button.disabled = true;
        button.textContent = 'Connexion...';
    }

    try {
        const { response, body } = await fetchJson('login/', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });

        if (response.ok && body?.access) {
            const user = await fetchCurrentUser(body.access);
            setAuthData(body.access, body.refresh, user || { username });
            showNotification('Connexion réussie !', 'success');
            updateAuthUi();
            window.location.href = '/';
            return;
        }

        const message = body?.detail || Object.values(body || {}).flat().join(' ') || 'Identifiants incorrects.';
        if (errorDiv) {
            errorDiv.textContent = `❌ ${message}`;
            errorDiv.style.display = 'block';
        } else {
            showNotification(`Erreur: ${message}`, 'error');
        }
    } catch (err) {
        if (errorDiv) {
            errorDiv.textContent = '❌ Impossible de contacter le serveur.';
            errorDiv.style.display = 'block';
        } else {
            showNotification('Impossible de contacter le serveur.', 'error');
        }
    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = 'Se connecter';
        }
    }
}

async function handleSendVerificationCode(event) {
    if (event) event.preventDefault();

    const email = document.getElementById('registerEmail')?.value.trim() || '';
    const phone = document.getElementById('registerPhone')?.value.trim() || '';
    const errorDiv = document.getElementById('registerError');
    const verificationSection = document.getElementById('verificationSection');
    const sendBtn = document.getElementById('sendCodeBtn');

    if (errorDiv) {
        errorDiv.style.display = 'none';
    }

    const contact = email || phone;
    if (!contact) {
        if (errorDiv) {
            errorDiv.textContent = '❌ Veuillez saisir un email ou un numéro de téléphone.';
            errorDiv.style.display = 'block';
        }
        return;
    }

    if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.textContent = 'Envoi en cours...';
    }

    try {
        const { response, body } = await fetchJson('send-code/', {
            method: 'POST',
            body: JSON.stringify({ contact }),
        });

        if (response.ok) {
            if (verificationSection) verificationSection.style.display = 'block';
            showNotification('Code de vérification envoyé.', 'success');
            return;
        }

        const message = body?.detail || Object.values(body || {}).flat().join(' ') || 'Impossible d’envoyer le code.';
        if (errorDiv) {
            errorDiv.textContent = `❌ ${message}`;
            errorDiv.style.display = 'block';
        } else {
            showNotification(message, 'error');
        }
    } catch (err) {
        if (errorDiv) {
            errorDiv.textContent = '❌ Impossible de contacter le serveur.';
            errorDiv.style.display = 'block';
        } else {
            showNotification('Impossible de contacter le serveur.', 'error');
        }
    } finally {
        if (sendBtn) {
            sendBtn.disabled = false;
            sendBtn.textContent = 'Envoyer le code';
        }
    }
}

async function handleRegisterForm(event) {
    if (event) event.preventDefault();

    const username = document.getElementById('registerUsername')?.value.trim() || '';
    const fullName = document.getElementById('registerFullName')?.value.trim() || '';
    const email = document.getElementById('registerEmail')?.value.trim() || '';
    const phone = document.getElementById('registerPhone')?.value.trim() || '';
    const password = document.getElementById('registerPassword')?.value || '';
    const verification_code = document.getElementById('verificationCode')?.value.trim() || '';
    const user_type = document.getElementById('registerType')?.value || 'student';
    const button = document.getElementById('registerBtn');
    const errorDiv = document.getElementById('registerError');

    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
    if (button) {
        button.disabled = true;
        button.textContent = 'Inscription...';
    }

    const [first_name, ...rest] = fullName.split(' ');
    const last_name = rest.join(' ');

    try {
        const { response, body } = await fetchJson('register/', {
            method: 'POST',
            body: JSON.stringify({
                username,
                email,
                first_name,
                last_name,
                phone,
                user_type,
                password,
                verification_code,
            }),
        });

        if (response.ok && body?.access) {
            const user = { ...body };
            delete user.access;
            delete user.refresh;
            setAuthData(body.access, body.refresh, user);
            showNotification('Inscription réussie !', 'success');
            updateAuthUi();
            window.location.href = '/';
            return;
        }

        const messages = [];
        if (body && typeof body === 'object') {
            for (const [key, value] of Object.entries(body)) {
                if (Array.isArray(value)) {
                    messages.push(`${key}: ${value.join(' ')}`);
                } else {
                    messages.push(`${key}: ${value}`);
                }
            }
        }
        const message = messages.length ? messages.join(' | ') : 'Impossible de vous inscrire.';

        if (errorDiv) {
            errorDiv.textContent = `❌ ${message}`;
            errorDiv.style.display = 'block';
        } else {
            showNotification(message, 'error');
        }
    } catch (err) {
        if (errorDiv) {
            errorDiv.textContent = '❌ Impossible de contacter le serveur.';
            errorDiv.style.display = 'block';
        } else {
            showNotification('Impossible de contacter le serveur.', 'error');
        }
    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = "S'inscrire";
        }
    }
}

function handleLogout(redirect = true) {
    clearAuthData();
    if (redirect) {
        window.location.href = '/';
    }
}

window.handleLoginForm = handleLoginForm;
window.handleRegisterForm = handleRegisterForm;
window.handleLogout = handleLogout;
window.authUpdateUi = updateAuthUi;

document.addEventListener('DOMContentLoaded', updateAuthUi);
