// --- DOM ELEMENTS ---
const authOverlay = document.getElementById('authOverlay');
const mainApp = document.getElementById('mainApp');
const authCard = document.getElementById('authCard');
const fileInput = document.getElementById('pdfFile');
const fileNameDisplay = document.getElementById('fileName');
const profileModal = document.getElementById('profileModal');
const avatarInput = document.getElementById('avatarInput');

// Default Blank Avatar
const DEFAULT_AVATAR = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI1MCIgZmlsbD0iI2ZmZmZmZiIvPjwvc3ZnPg==";

// --- SPEECH SYNTHESIS VARIABLES ---
let synth = window.speechSynthesis;
let isSpeaking = false;
let speechUtterance = null;

// --- AUTH LOGIC ---
async function checkUser() {
    try {
        const res = await fetch('/api/user');
        const data = await res.json();
        if (data.logged_in) showMainApp(data);
        else showAuth();
    } catch { showAuth(); }
}
document.addEventListener('DOMContentLoaded', checkUser);

function showMainApp(userData) {
    authOverlay.classList.add('hidden');
    mainApp.classList.remove('blur-content');
    mainApp.classList.add('active');
    
    const name = userData.name || "User";
    document.getElementById('topUserName').innerText = name;
    document.getElementById('pName').innerText = name;
    document.getElementById('pEmail').innerText = userData.email || "";

    let avatarSrc = userData.avatar ? `${userData.avatar}?t=${new Date().getTime()}` : DEFAULT_AVATAR;
    
    document.getElementById('userAvatar').src = avatarSrc;
    document.getElementById('modalAvatar').src = avatarSrc;

    loadHistory();
}

// --- FILE UPLOAD ---
function triggerFileUpload() { avatarInput.click(); }

async function uploadAvatar() {
    if (avatarInput.files.length === 0) return;
    const formData = new FormData();
    formData.append('avatar', avatarInput.files[0]);
    document.getElementById('modalAvatar').style.opacity = '0.5';

    try {
        const res = await fetch('/api/upload_avatar', { method: 'POST', body: formData });
        const data = await res.json();
        if (res.ok) {
            const newSrc = `${data.avatar_url}?t=${new Date().getTime()}`;
            document.getElementById('userAvatar').src = newSrc;
            document.getElementById('modalAvatar').src = newSrc;
        } else alert("Upload Failed: " + data.error);
    } catch { alert("Server Error"); }
    finally { document.getElementById('modalAvatar').style.opacity = '1'; }
}

// --- AUTH HELPERS ---
function showAuth() {
    authOverlay.classList.remove('hidden');
    mainApp.classList.add('blur-content');
    mainApp.classList.remove('active');
}

function switchAuth(type) {
    if (type === 'signup') {
        document.getElementById('loginForm').classList.add('hidden');
        document.getElementById('signupForm').classList.remove('hidden');
    } else {
        document.getElementById('signupForm').classList.add('hidden');
        document.getElementById('loginForm').classList.remove('hidden');
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: document.getElementById('loginEmail').value, password: document.getElementById('loginPass').value })
    });
    const data = await res.json();
    if (res.ok) {
        const userRes = await fetch('/api/user');
        const userData = await userRes.json();
        showMainApp(userData);
    } else alert(data.error);
}

async function handleSignup(e) {
    e.preventDefault();
    const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: document.getElementById('regName').value, email: document.getElementById('regEmail').value, password: document.getElementById('regPass').value })
    });
    if (res.ok) { alert("Done! Login now."); switchAuth('login'); }
    else alert("Error");
}

async function handleLogout() {
    await fetch('/api/logout', { method: 'POST' });
    location.reload();
}

// --- PROFILE ---
function toggleProfile() {
    if (profileModal.classList.contains('hidden')) {
        profileModal.classList.remove('hidden');
        checkUser(); 
    } else {
        profileModal.classList.add('hidden');
    }
}
document.addEventListener('keydown', (e) => { if (e.key === "Escape") profileModal.classList.add('hidden'); });

// --- MAIN APP ---
fileInput.addEventListener('change', function() {
    if (this.files.length > 0) fileNameDisplay.innerHTML = `FILE: <span style="color:var(--primary-cyan);">${this.files[0].name}</span>`;
});

async function simplifyDoc() {
    // Stopping old speech before starting new analysis
    stopSpeech();

    const outputDiv = document.getElementById('outputContent');
    const resultSection = document.getElementById('resultSection');
    const loading = document.getElementById('loading');
    const btn = document.getElementById('simplifyBtn');
    
    if (fileInput.files.length === 0) return alert("Select File");
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('language', document.getElementById('languageSelect').value);
    formData.append('mode', document.getElementById('modeSelect').value);

    btn.disabled = true; btn.innerText = 'PROCESSING...';
    loading.classList.remove('hidden');
    resultSection.classList.add('hidden');

    try {
        const res = await fetch('/api/simplify', { method: 'POST', body: formData });
        const data = await res.json();
        
        loading.classList.add('hidden');
        btn.disabled = false; btn.innerText = 'ANALYZE';
        
        if (res.ok) {
            outputDiv.innerText = data.simplified_text;
            resultSection.classList.remove('hidden');
            resultSection.scrollIntoView({ behavior: 'smooth' });
            loadHistory();
        } else alert(data.error);
    } catch { loading.classList.add('hidden'); btn.disabled = false; alert("Error"); }
}

function copyText() {
    navigator.clipboard.writeText(document.getElementById('outputContent').innerText);
    const btn = document.querySelector('.copy-btn');
    const org = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-check"></i> COPIED';
    setTimeout(() => btn.innerHTML = org, 2000);
}

async function loadHistory() {
    const list = document.getElementById('historyList');
    try {
        const res = await fetch('/api/history');
        const data = await res.json();
        list.innerHTML = '';
        if(data.length > 0) {
            data.forEach(item => {
                const div = document.createElement('div');
                div.className = 'history-item';
                div.innerHTML = `<div style="color:white; font-weight:600"><i class="fa-solid fa-file-pdf"></i> ${item.filename}</div><div style="font-size:0.7rem; color:#888;">${item.mode} | ${new Date(item.timestamp).toLocaleDateString()}</div>`;
                div.onclick = () => {
                    // Stop speech while loading history
                    stopSpeech();
                    document.getElementById('outputContent').innerText = item.summary;
                    document.getElementById('resultSection').classList.remove('hidden');
                    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
                };
                list.appendChild(div);
            });
        }
    } catch {}
}

// --- NEW: TEXT-TO-SPEECH LOGIC ---
function toggleSpeech() {
    const text = document.getElementById('outputContent').innerText;
    const btn = document.getElementById('playBtn');

    if (synth.speaking && isSpeaking) {
        //If he talks, stop.
        stopSpeech();
    } else {
        // If they don't talk, start.
        if (text.trim() === "") return alert("No text to read!");
        
        // UI Update
        btn.innerHTML = '<i class="fa-solid fa-stop"></i> STOP';
        btn.classList.add('speaking');
        isSpeaking = true;

        speechUtterance = new SpeechSynthesisUtterance(text);
        
        // Select voice by language (Optional Logic)
        const selectedLang = document.getElementById('languageSelect').value;
        if(selectedLang === "Bengali") speechUtterance.lang = "bn-IN";
        else if(selectedLang === "Hindi") speechUtterance.lang = "hi-IN";
        else if(selectedLang === "Spanish") speechUtterance.lang = "es-ES";
        else speechUtterance.lang = "en-US"; // Default English

        // When finished, press the reset button.
        speechUtterance.onend = () => {
            stopSpeech();
        };

        synth.speak(speechUtterance);
    }
}

function stopSpeech() {
    synth.cancel();
    isSpeaking = false;
    const btn = document.getElementById('playBtn');
    if(btn) {
        btn.innerHTML = '<i class="fa-solid fa-volume-high"></i> LISTEN';
        btn.classList.remove('speaking');
    }
}