// ============================================================
// FloodAI — Complete script.js (Updated with Weather Forecast)
// ============================================================

const BACKEND = "";

// ⚠️ FIX (২০২৬-০৮): এখন district/station নাম static config থেকে আসে বলে
// XSS ঝুঁকি বাস্তবে কম, কিন্তু ভবিষ্যতে scraped/API/user-submitted ডেটা এই
// টেমপ্লেটগুলোতে ঢুকলে ঝুঁকি তৈরি হতে পারে — তাই সব dynamic টেক্সট এখন থেকেই
// escape করে বসানো হচ্ছে, ভবিষ্যতের জন্য নিরাপদ থাকতে।
function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

const LEVEL_STYLE = {
    'বিপদ':     { icon: 'fa-circle-exclamation',    text: '#943126', bg: '#fdedec', border: '#c0392b' },
    'সতর্ক':    { icon: 'fa-triangle-exclamation',  text: '#af601a', bg: '#fdf0e4', border: '#e67e22' },
    'সাবধান':   { icon: 'fa-triangle-exclamation',  text: '#b9770e', bg: '#fef5e7', border: '#f39c12' },
    'স্বাভাবিক': { icon: 'fa-circle-check',          text: '#1e8449', bg: '#eafaf1', border: '#27ae60' },
    'নিরাপদ':   { icon: 'fa-circle-check',          text: '#1e8449', bg: '#eafaf1', border: '#27ae60' }
};
function levelStyleFor(level) {
    return LEVEL_STYLE[level] || LEVEL_STYLE['নিরাপদ'];
}
function iconForColor(hex) {
    if (hex === '#c0392b') return levelIcon('বিপদ');
    if (hex === '#e67e22') return levelIcon('সতর্ক');
    if (hex === '#f39c12') return levelIcon('সাবধান');
    return levelIcon('নিরাপদ');
}
function levelIcon(level) {
    return `<i class="fa-solid ${levelStyleFor(level).icon}" aria-hidden="true"></i>`;
}
function levelBadge(level, label) {
    const s = levelStyleFor(level);
    return `<span style="display:inline-flex;align-items:center;gap:7px;background:${s.bg};
                border-left:3px solid ${s.border};color:${s.text};font-weight:600;
                padding:6px 12px;border-radius:6px;">
                <i class="fa-solid ${s.icon}" aria-hidden="true"></i>${label || level}
            </span>`;
}

// ── NAVBAR SCROLL EFFECT ──
window.addEventListener('scroll', () => {
    const nav = document.getElementById('navbar');
    if (window.scrollY > 50) {
        nav.style.background = 'rgba(255,255,255,0.97)';
        nav.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    } else {
        nav.style.background = 'rgba(240,244,248,0.88)';
        nav.style.boxShadow = 'none';
    }

    const sections = ['home','upstream','river','weather','map','emergency','stats','chatbot'];
    const links = document.querySelectorAll('.nav-links a');
    let current = 'home';
    sections.forEach(id => {
        const el = document.getElementById(id);
        if (el && window.scrollY >= el.offsetTop - 120) current = id;
    });
    links.forEach(l => {
        l.classList.toggle('active', l.getAttribute('href') === '#' + current);
    });
});

function toggleMenu() {
    document.getElementById('navLinks').classList.toggle('open');
}

function scrollToSection(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({behavior:'smooth'});
}

async function detectLocation() {
    if (!navigator.geolocation) {
        alert('Browser location সাপোর্ট করে না');
        return;
    }
    navigator.geolocation.getCurrentPosition(async pos => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;

        // ── আগে এখানে শুধু lat/lon একটা alert-এ দেখানো হতো, জেলা
        // auto-select করার কোনো লজিক ছিল না। এখন /api/districts/map
        // থেকে পাওয়া প্রতিটা জেলার lat/lon-এর সাথে distance মিলিয়ে
        // সবচেয়ে কাছেরটা বের করে dropdown-এ বসিয়ে সেই জেলার ডেটা
        // লোড করা হচ্ছে (বাংলাদেশের ছোট আয়তনের জন্য simple Euclidean
        // distance যথেষ্ট, haversine লাগবে না) ──
        try {
            const res = await fetch(`${BACKEND}/api/districts/map`);
            if (!res.ok) throw new Error('districts/map fetch failed');
            const districts = await res.json();

            let nearest = null;
            let minDist = Infinity;
            districts.forEach(d => {
                if (typeof d.lat !== 'number' || typeof d.lon !== 'number') return;
                const dist = Math.hypot(d.lat - lat, d.lon - lon);
                if (dist < minDist) {
                    minDist = dist;
                    nearest = d.name;
                }
            });

            if (nearest) {
                const select = document.getElementById('districtSelect');
                if (select) select.value = nearest;
                loadDistrict(nearest);
                scrollToSection('river');
                alert(`✅ আপনার এলাকা: ${nearest}`);
            } else {
                alert('❌ কাছের জেলা খুঁজে পাওয়া যায়নি');
            }
        } catch (e) {
            console.error('District match error:', e);
            alert('❌ জেলা মেলাতে সমস্যা হয়েছে। Backend চালু আছে কিনা চেক করুন।');
        }
    }, () => {
        alert('Location পাওয়া যায়নি। ব্রাউজারে location permission দিন।');
    });
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.style.display = 'none';
}

function switchModal(hideId, showId) {
    const hideModal = document.getElementById(hideId);
    const showModal = document.getElementById(showId);
    if (hideModal) hideModal.style.display = 'none';
    if (showModal) showModal.style.display = 'flex';
}

async function submitReport() {
    const district = document.getElementById('reportDistrict')?.value;
    const status = document.getElementById('reportStatus')?.value;
    const description = document.getElementById('reportDesc')?.value || '';

    if (!district) {
        alert('আগে জেলা বেছে নিন!');
        return;
    }

    try {
        const res = await fetch(`${BACKEND}/api/report`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ district, status, description, lat: 0, lon: 0 })
        });
        if (!res.ok) throw new Error('Server error: ' + res.status);
        alert('✅ রিপোর্ট সফলভাবে পাঠানো হয়েছে!');
        closeModal('reportModal');
        document.getElementById('reportDesc').value = '';
    } catch (e) {
        console.error('Report submit error:', e);
        alert('❌ রিপোর্ট পাঠাতে সমস্যা হয়েছে। Backend চালু আছে কিনা চেক করুন।');
    }
}

async function submitLogin() {
    const email = document.getElementById('loginEmail')?.value;
    const password = document.getElementById('loginPassword')?.value;

    if (!email || !password) {
        alert('Email ও Password দিন!');
        return;
    }

    try {
        const res = await fetch(`${BACKEND}/api/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (!res.ok) {
            alert('❌ ' + (data.error || 'Login ব্যর্থ হয়েছে'));
            return;
        }
        alert(`✅ স্বাগতম, ${data.user.name}!`);
        closeModal('loginModal');
    } catch (e) {
        console.error('Login error:', e);
        alert('❌ Login করতে সমস্যা হয়েছে। Backend চালু আছে কিনা চেক করুন।');
    }
}

async function submitSignup() {
    const name = document.getElementById('signupName')?.value;
    const email = document.getElementById('signupEmail')?.value;
    const password = document.getElementById('signupPassword')?.value;
    const phone = document.getElementById('signupPhone')?.value || '';
    const district = document.getElementById('signupDistrict')?.value;

    if (!name || !email || !password || !district) {
        alert('নাম, Email, Password ও জেলা আবশ্যক!');
        return;
    }

    try {
        const res = await fetch(`${BACKEND}/api/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ name, email, password, phone, district })
        });
        const data = await res.json();
        if (!res.ok) {
            alert('❌ ' + (data.error || 'Sign Up ব্যর্থ হয়েছে'));
            return;
        }
        alert('✅ নতুন অ্যাকাউন্ট সফলভাবে তৈরি হয়েছে! এখন Login করুন।');
        closeModal('signupModal');
    } catch (e) {
        console.error('Signup error:', e);
        alert('❌ Sign Up করতে সমস্যা হয়েছে। Backend চালু আছে কিনা চেক করুন।');
    }
}

// ── MAP INIT ──
const RISK_COLORS = {
    "অতি উচ্চ": "#c0392b",
    "উচ্চ": "#e67e22",
    "মাঝারি": "#f39c12",
    "কম": "#27ae60"
};
const LIVE_LEVEL_COLORS = {
    "বিপদ": "#c0392b",
    "সতর্ক": "#e67e22",
    "সাবধান": "#f39c12",
    "নিরাপদ": "#27ae60"
};
let floodLeafletMap = null;

function initMap() {
    const mapEl = document.getElementById('floodMap');
    if (!mapEl || typeof L === 'undefined') return;

    floodLeafletMap = L.map('floodMap').setView([23.8, 90.3], 6.6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(floodLeafletMap);

    loadDistrictMarkers();
    loadAllStationMarkers();
    loadMapWarnings();
}

async function loadDistrictMarkers() {
    if (!floodLeafletMap) return;
    try {
        const res = await fetch(`${BACKEND}/api/districts/map`);
        if (!res.ok) throw new Error("districts/map fetch failed");
        const districts = await res.json();

        districts.forEach(d => {
            // ── marker এখন city center না, নদীর station-এর কাছাকাছি
            // coordinate-এ বসছে (river_lat/river_lon)। fallback হিসেবে
            // city coordinate ব্যবহার হবে যদি river coordinate না থাকে ──
            const markerLat = typeof d.river_lat === 'number' ? d.river_lat : d.lat;
            const markerLon = typeof d.river_lon === 'number' ? d.river_lon : d.lon;
            if (typeof markerLat !== 'number' || typeof markerLon !== 'number') return;

            const isLive = !!d.live_warning_level;
            const color = isLive
                ? (LIVE_LEVEL_COLORS[d.live_warning_level] || '#4a6080')
                : '#27ae60';

            const marker = L.circleMarker([markerLat, markerLon], {
                radius: isLive ? 9 : 5,
                fillColor: color,
                color: isLive ? '#fff' : '#27ae60',
                weight: isLive ? 2 : 1,
                fillOpacity: isLive ? 0.9 : 0.45
            }).addTo(floodLeafletMap);

            const statusLine = isLive
                ? `<div style="display:inline-block;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:700;color:#fff;background:${color}">🔴 লাইভ: ${d.live_warning_level} (${d.live_risk_score ?? '—'}%)</div>`
                : `<div style="display:inline-block;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:700;color:#fff;background:${color}">স্বাভাবিক (লাইভ চেক করা হয়নি)</div>`;

            // ffwc_verified: true হলে real FFWC station data, "coordinate-only"
            // হলে শুধু coordinate verified (danger_level পুরনো), false হলে
            // পুরোটাই এখনো placeholder — ব্যবহারকারীকে সততার সাথে জানানো দরকার
            let verifyBadge = '';
            if (d.ffwc_verified === true) {
                verifyBadge = `<div style="font-size:10px;color:#27ae60;margin-bottom:4px">✓ FFWC station দিয়ে ভেরিফাইড</div>`;
            } else if (d.ffwc_verified === 'coordinate-only') {
                verifyBadge = `<div style="font-size:10px;color:#e67e22;margin-bottom:4px">⚠ শুধু coordinate ভেরিফাইড, danger level আনুমানিক</div>`;
            } else if (d.ffwc_verified === 'borrowed_from_neighbor') {
                verifyBadge = `<div style="font-size:10px;color:#e67e22;margin-bottom:4px">⚠ এই জেলার নিজস্ব station নেই — প্রতিবেশী জেলার gauge থেকে ধার করা ডেটা</div>`;
            } else {
                verifyBadge = `<div style="font-size:10px;color:#c0392b;margin-bottom:4px">⚠ এখনো আনুমানিক ডেটা (station পাওয়া যায়নি)</div>`;
            }

            marker.bindPopup(`
                <div style="font-family:'Segoe UI',sans-serif;min-width:170px">
                    <div style="font-weight:700;font-size:14px;margin-bottom:4px">${escapeHtml(d.name)}</div>
                    <div style="font-size:12px;color:#4a6080;margin-bottom:2px">নদী: ${d.river || '—'}</div>
                    <div style="font-size:12px;color:#4a6080;margin-bottom:2px">বিপদসীমা: ${d.danger_level ?? '—'} মি</div>
                    ${d.ffwc_station ? `<div style="font-size:11px;color:#4a6080;margin-bottom:4px">Station: ${d.ffwc_station}</div>` : ''}
                    ${verifyBadge}
                    ${statusLine}
                    <div style="margin-top:8px">
                        <button onclick="selectDistrictFromMap('${escapeHtml(d.name)}')" style="width:100%;padding:6px;background:#1a5fa8;color:#fff;border:none;border-radius:6px;font-size:12px;cursor:pointer">এই জেলার বিস্তারিত দেখুন →</button>
                    </div>
                </div>
            `);
        });
    } catch (e) {
        console.error('District marker load error:', e);
    }
}

function selectDistrictFromMap(name) {
    const select = document.getElementById('districtSelect');
    if (select) select.value = name;
    loadDistrict(name);
    scrollToSection('river');
}

// ── FFWC-র সব station (যেগুলো ইতিমধ্যে জেলা-marker হিসেবে দেখানো হয়নি —
// "linked_district" থাকলে ওটা district marker-এই কাভার হয়ে গেছে, তাই এখানে
// শুধু বাকি 'extra' reference station দেখানো হচ্ছে) — page load-এ হালকা
// রাখার জন্য এখানে live discharge fetch হয় না, ক্লিক করলে তখনই হয় ──
async function loadAllStationMarkers() {
    if (!floodLeafletMap) return;
    try {
        const res = await fetch(`${BACKEND}/api/stations/map`);
        if (!res.ok) throw new Error("stations/map fetch failed");
        const stations = await res.json();

        stations.forEach(s => {
            if (s.linked_district) return;
            if (typeof s.lat !== 'number' || typeof s.lon !== 'number') return;

            const marker = L.circleMarker([s.lat, s.lon], {
                radius: 4,
                fillColor: '#8a99ad',
                color: '#8a99ad',
                weight: 1,
                fillOpacity: 0.55
            }).addTo(floodLeafletMap);

            marker.bindPopup(`
                <div style="font-family:'Segoe UI',sans-serif;min-width:170px" id="stationPopup-${s.id.replace(/\W/g,'')}">
                    <div style="font-weight:700;font-size:14px;margin-bottom:4px">${escapeHtml(s.name)}</div>
                    <div style="font-size:12px;color:#4a6080;margin-bottom:2px">নদী: ${s.river || '—'}</div>
                    <div style="font-size:12px;color:#4a6080;margin-bottom:2px">জেলা: ${s.district || '—'}</div>
                    <div style="font-size:12px;color:#4a6080;margin-bottom:8px">বিপদসীমা: ${s.danger_level ?? '—'} মি</div>
                    <button onclick="fetchStationLive('${s.id}')" style="width:100%;padding:6px;background:#4a6080;color:#fff;border:none;border-radius:6px;font-size:12px;cursor:pointer">লাইভ পানির স্তর দেখুন</button>
                    <div id="stationLive-${s.id.replace(/\W/g,'')}" style="margin-top:6px;font-size:12px;color:#4a6080"></div>
                </div>
            `);
        });
    } catch (e) {
        console.error('Station marker load error:', e);
    }
}

async function fetchStationLive(stationId) {
    const safeId = stationId.replace(/\W/g, '');
    const box = document.getElementById(`stationLive-${safeId}`);
    if (!box) return;
    box.innerHTML = 'লোড হচ্ছে...';
    try {
        const res = await fetch(`${BACKEND}/api/stations/${encodeURIComponent(stationId)}/live`);
        if (!res.ok) throw new Error("station live fetch failed");
        const data = await res.json();

        if (data.source === 'ffwc_live' && data.water_level != null) {
            const danger = data.danger_level;
            const isOverDanger = danger != null && data.water_level >= danger;
            const levelColor = isOverDanger ? '#c0392b' : '#2e7d32';
            box.innerHTML = `
                পানির স্তর (FFWC): <b style="color:${levelColor}">${data.water_level}</b> মি (mMSL)
                ${data.recorded_at ? `<div style="font-size:11px;color:#7a8ba0">রেকর্ড: ${data.recorded_at}</div>` : ''}
                <div style="font-size:11px;color:#7a8ba0">ডিসচার্জ (আনুমানিক): ${data.discharge} m³/s</div>
            `;
        } else {
            // FFWC scrape এই মুহূর্তে পাওয়া যায়নি — শুধু modeled discharge দেখানো হচ্ছে,
            // এটাকে real observed water level হিসেবে না দেখিয়ে আলাদাভাবে লেবেল করা
            box.innerHTML = `
                FFWC লাইভ পানির স্তর এখন পাওয়া যায়নি।
                <div style="font-size:11px;color:#7a8ba0">আনুমানিক ডিসচার্জ: ${data.discharge} m³/s</div>
            `;
        }
    } catch (e) {
        box.innerHTML = 'লাইভ ডেটা আনা যায়নি';
    }
}

async function loadMapWarnings() {
    const panel = document.getElementById('mapWarningsPanel');
    if (!panel) return;
    try {
        const res = await fetch(`${BACKEND}/api/warnings/active`);
        const warnings = await res.json();

        if (!warnings || warnings.length === 0) {
            panel.innerHTML = `<div style="text-align:center;padding:2rem 1rem;color:var(--muted);font-size:13px">
                বর্তমানে কোনো সক্রিয় সতর্কতা নেই
            </div>`;
            return;
        }

        panel.innerHTML = warnings.map(w => {
            const color = w.warning_level === 'বিপদ' ? '#c0392b' : w.warning_level === 'সতর্ক' ? '#e67e22' : '#f39c12';
            return `
                <div style="border-left:3px solid ${color};background:var(--bg);border-radius:6px;padding:10px 12px;margin-bottom:8px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
                        <span style="font-weight:700;font-size:13px;color:var(--text)">${w.district || 'অজানা জেলা'}</span>
                        <span style="font-size:10px;font-weight:700;color:${color}">${w.warning_level || ''}</span>
                    </div>
                    <div style="font-size:11px;color:var(--muted)">${w.timestamp ? new Date(w.timestamp).toLocaleString('bn-BD') : ''}</div>
                </div>
            `;
        }).join('');
    } catch (e) {
        panel.innerHTML = `<div style="text-align:center;padding:2rem 1rem;color:var(--muted);font-size:13px">সতর্কতা লোড করা যায়নি</div>`;
        console.error('Map warnings load error:', e);
    }
}

// ── MAIN FLOOD DATA LOADER ──
async function loadDistrict(name) {
    if (!name) return;

    try {
        const res = await fetch(`${BACKEND}/api/flood/${encodeURIComponent(name)}`);
        const data = await res.json();

        const metRiver = document.getElementById('metRiver');
        if(metRiver) metRiver.textContent = data.river;

        const metDanger = document.getElementById('metDanger');
        if(metDanger) metDanger.textContent = data.danger_level;

        const metDischarge = document.getElementById('metDischarge');
        if(metDischarge && data.discharge_today) {
            metDischarge.textContent = Math.round(data.discharge_today).toLocaleString();
        }

        const metRisk = document.getElementById('metRisk');
        if(metRisk) metRisk.textContent = data.risk_category || '—';

        const predForRef = data.prediction || data.ml_prediction || {};
        const predLocalRef = predForRef.input_summary ? predForRef.input_summary.reference_discharge_m3s : null;

        const riverTableBody = document.getElementById('riverTableBody');
        if(riverTableBody) {
            const riversStatus = Array.isArray(data.rivers_status) && data.rivers_status.length
                ? data.rivers_status
                // পুরনো backend response (rivers_status ছাড়া) হলে single-row fallback
                : [{ name: data.river, discharge_today: data.discharge_today || 0, danger_level: data.danger_level || 0, is_primary: true }];

            riverTableBody.innerHTML = riversStatus.map(r => {
                const isScoring = r.name === data.scoring_river || riversStatus.length === 1;
                const discharge = r.discharge_today || 0;
                const dangerLevel = r.danger_level || 0;
                let statusCell;
                if (isScoring) {
                    // যে নদী দিয়ে ML prediction চালানো হয়েছে, শুধু তারই আসল warning_level দেখানো হচ্ছে
                    statusCell = levelBadge(data.warning_level || 'অনির্ণীত') +
                        `<div style="font-size:10px;color:#7a8ba0;margin-top:3px">★ ঝুঁকি নির্ধারণকারী নদী</div>`;
                } else {
                    // বাকি নদীগুলোর জন্য আলাদা ML prediction চালানো হয় না। আগে এখানে
                    // discharge/danger_level থেকে একটা % দেখানো হতো, কিন্তু danger_level
                    // (মিটার, water-level threshold) আর discharge (m³/s, প্রবাহের হার)
                    // সরাসরি তুলনাযোগ্য না — real rating curve (Q=a(H-h0)^b) ছাড়া এই
                    // অনুপাতকে সত্যিকারের "% of danger" বলে দাবি করা যায় না। তাই এখন
                    // শুধু raw discharge সংখ্যাটাই দেখানো হচ্ছে, কোনো ব্যাখ্যামূলক % না।
                    statusCell = `<span style="color:#5a6b85;font-size:12.5px">তথ্যের জন্য — আলাদা প্রেডিকশন চালানো হয়নি</span>`;
                }
                return `<tr>
                    <td>${r.name || '—'}${r.is_primary ? '' : ''}</td>
                    <td>${discharge.toLocaleString()} m³/s</td>
                    <td>${dangerLevel} মি</td>
                    <td>${statusCell}</td>
                </tr>`;
            }).join('');
        }

        if(data.weather) {
            document.getElementById('wTemp').textContent = data.weather.temp || '—';
            document.getElementById('wHumidity').textContent = data.weather.humidity || '—';
            document.getElementById('wRain').textContent = data.weather.rain || '0';
            document.getElementById('wWind').textContent = data.weather.wind || '—';
        }

        const warningCard = document.getElementById('warningCard');
        if(warningCard) warningCard.style.display = 'block';

        const upCity = data.upstream_weather || {};
        const upstreamCards = document.getElementById('upstreamCards');

        const predLocal = data.prediction || data.ml_prediction || {};
        const localLevel = predLocal.level || data.warning_level || 'নিরাপদ';
        let localLevelColor = '#27ae60';
        if(localLevel === 'বিপদ') localLevelColor = '#c0392b';
        else if(localLevel === 'সতর্ক') localLevelColor = '#e67e22';
        else if(localLevel === 'সাবধান') localLevelColor = '#f39c12';

        let actualUpstreamCity = upCity.city;
        if (!actualUpstreamCity || actualUpstreamCity === 'উজান') {
            const riverToCityMap = {
                'তিস্তা': 'জলপাইগুড়ি',
                'ব্রহ্মপুত্র': 'গুয়াহাটি',
                'সুরমা': 'শিলং',
                'পদ্মা': 'মালদা',
                'মেঘনা': 'আগরতলা',
                'যমুনা': 'গুয়াহাটি',
                'করতোয়া': 'জলপাইগুড়ি',
                'কংস': 'শিলং',
                'তিতাস': 'আগরতলা',
                'মাতামুহুরী': 'আগরতলা',
                'সাঙ্গু': 'আগরতলা',
                'চেঙ্গী': 'আগরতলা',
                'কর্ণফুলী': 'আগরতলা',
                'পায়রা': 'আগরতলা',
                'ইছামতী': 'কলকাতা',
                'ভৈরব': 'কলকাতা',
                'গড়াই': 'মালদা',
                'রূপসা': 'কলকাতা',
                'কীর্তনখোলা': 'আগরতলা',
                'বুড়িগঙ্গা': 'ঢাকা'
            };
            actualUpstreamCity = riverToCityMap[data.river] || 'উজান';
        }

        const upstreamFlow = document.getElementById('upstreamFlow');
        if(upstreamFlow) {
            upstreamFlow.style.textAlign = 'center';
            upstreamFlow.style.padding = '1.5rem';
            upstreamFlow.style.border = '1px solid var(--border)';
            upstreamFlow.style.background = '#ffffff';
            upstreamFlow.style.borderRadius = '8px';

            upstreamFlow.innerHTML =
                `<div style="font-size: 15px; color:var(--blue); font-weight:700;">
                    <i class="fa-solid fa-cloud-showers-heavy"></i> ${actualUpstreamCity} (ভারত)
                 </div>
                 <div style="margin: 10px 0; color:var(--muted); font-size:12px; font-weight:600; background: var(--bg); padding: 6px 12px; border-radius: 20px; display: inline-block; border: 1px solid var(--border);">
                    <i class="fa-solid fa-water" style="color:var(--blue);"></i> <strong>${data.river}</strong> নদী দিয়ে <strong>${data.lag_time}</strong> ঘণ্টায় পানি আসে
                 </div>
                 <div style="font-size: 15px; color:#27ae60; font-weight:700;">
                    <i class="fa-solid fa-location-dot"></i> ${data.district || name} (বাংলাদেশ)
                 </div>`;
        }

        const forecastArr = Array.isArray(data.forecast) ? data.forecast : [];
        const todayDischarge = data.discharge_today || forecastArr[0] || 0;
        const lookAheadDays = Math.min(Math.max(Math.round((data.lag_time || 24) / 24), 1), Math.max(forecastArr.length - 1, 0));
        const futureDischarge = forecastArr[lookAheadDays] !== undefined ? forecastArr[lookAheadDays] : todayDischarge;
        const pctChange = todayDischarge > 0 ? ((futureDischarge - todayDischarge) / todayDischarge) * 100 : 0;

        let trendColor = '#607d8b', trendMsg = '';
        // ⚠️ trend (বাড়ছে/কমছে/স্থিতিশীল) শুধু forecast-এর *পরিবর্তনের হার* মাপে —
        // বর্তমানে নদী আদৌ বিপদসীমার উপরে আছে কিনা সেটা আলাদা তথ্য (localLevel)।
        // আগে এই দুটো আলাদাভাবে দেখানো হতো, ফলে "বিপদ" ব্যাজের ঠিক নিচেই
        // "স্থিতিশীল থাকার সম্ভাবনা" (নিরপেক্ষ ধূসর রং) দেখাতো — যা বিভ্রান্তিকর,
        // কারণ "স্থিতিশীল" মানে "নিরাপদ" না, মানে শুধু "আর বাড়ছে না"। এখন
        // localLevel বিবেচনা করে মেসেজ/রং ঠিক করা হচ্ছে।
        const isElevated = (localLevel === 'বিপদ' || localLevel === 'সতর্ক');
        if (pctChange > 15) {
            trendColor = isElevated ? '#c0392b' : '#e67e22';
            trendMsg = `<i class="fa-solid fa-arrow-trend-up" style="color:${trendColor}" aria-hidden="true"></i> <strong>আগামী কয়েকদিনে ${data.river} নদীর প্রবাহ বাড়ার সম্ভাবনা আছে</strong> (প্রায় ${Math.round(pctChange)}%)।` +
                (isElevated ? ` নদী <strong>এখনই ${localLevel}</strong> অবস্থায় আছে — অবস্থা আরও খারাপ হতে পারে, সতর্ক থাকুন। ` : ' ') +
                (upCity.rain > 3
                    ? `উজানে (${actualUpstreamCity}) এখন বৃষ্টি হচ্ছে (${upCity.rain}mm), যা <strong>${data.lag_time}</strong> ঘণ্টার মধ্যে এই বৃদ্ধির একটা কারণ হতে পারে।`
                    : `উজানে এই মুহূর্তে উল্লেখযোগ্য বৃষ্টি নেই, তাই এই বৃদ্ধি মূলত আগে থেকে জমে থাকা পানি বা অন্য প্রভাবক থেকে আসছে।`);
        } else if (pctChange < -15) {
            trendColor = isElevated ? '#e67e22' : '#27ae60';
            trendMsg = `<i class="fa-solid fa-arrow-trend-down" style="color:${trendColor}" aria-hidden="true"></i> <strong>আগামী কয়েকদিনে প্রবাহ কমার সম্ভাবনা আছে।</strong>` +
                (isElevated ? ` তবে নদী <strong>এখনও ${localLevel}</strong> অবস্থায় আছে — কমলেও তাৎক্ষণিক ঝুঁকি এখনই কেটে যাচ্ছে না। ` : ' ') +
                (upCity.rain > 3
                    ? `উজানে এখনো বৃষ্টি চলছে (${upCity.rain}mm) — পরিস্থিতি বদলাতে পারে, নজর রাখা ভালো।`
                    : `উজানেও এই মুহূর্তে বৃষ্টি নেই।`);
        } else {
            trendColor = isElevated ? '#c0392b' : '#607d8b';
            trendMsg = isElevated
                ? `<i class="fa-solid fa-triangle-exclamation" style="color:${trendColor}" aria-hidden="true"></i> <strong>${data.river} নদীর প্রবাহ আপাতত বাড়ছে-কমছে না (স্থিতিশীল), কিন্তু নদী এখনও <span style="color:${trendColor}">${localLevel}</span> অবস্থায় আছে</strong> — স্থিতিশীল মানে বিপদ কেটে গেছে তা না, শুধু আর বাড়ছে না। ` +
                  (upCity.rain > 3
                      ? `উজানে (${actualUpstreamCity}) বৃষ্টি চলছে (${upCity.rain}mm) — পরিস্থিতি বদলাতে পারে।`
                      : `উজানেও কোনো উল্লেখযোগ্য বৃষ্টি নেই, তাই শীঘ্রই বড় পরিবর্তনের সম্ভাবনা কম।`)
                : `<i class="fa-solid fa-arrow-right-arrow-left" style="color:${trendColor}" aria-hidden="true"></i> <strong>${data.river} নদীর প্রবাহ আপাতত মোটামুটি স্থিতিশীল থাকার সম্ভাবনা।</strong> ` +
                  (upCity.rain > 3
                      ? `উজানে (${actualUpstreamCity}) বৃষ্টি চলছে (${upCity.rain}mm) — এখনই বড় প্রভাব দেখা না গেলেও নজরে রাখা উচিত।`
                      : `উজানেও কোনো উল্লেখযোগ্য বৃষ্টি নেই।`);
        }

        if(upstreamCards) {
            upstreamCards.innerHTML = `
                <div style="grid-column: 1 / -1; width:100%; overflow-x:auto; margin-bottom:1rem;">
                    <table class="river-table" style="width:100%">
                        <thead style="background: var(--bg);">
                            <tr>
                                <th>স্থান</th>
                                <th>বৃষ্টি (mm)</th>
                                <th>আর্দ্রতা (%)</th>
                                <th>তাপমাত্রা (°C)</th>
                                <th>সার্বিক অবস্থা</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="font-weight:600; color:var(--text);"><i class="fa-solid fa-city" style="color:var(--blue); margin-right:4px;"></i> ${actualUpstreamCity} (ভারত)</td>
                                <td style="color:var(--blue); font-weight:600;">${upCity.rain || 0}</td>
                                <td>${upCity.humidity || '—'}</td>
                                <td>${upCity.temp || '—'}</td>
                                <td>
                                    <span style="color:var(--muted);font-weight:600">
                                        ${upCity.rain > 10 ? '<i class="fa-solid fa-cloud-showers-heavy" aria-hidden="true"></i> ভারী বৃষ্টি হচ্ছে' : upCity.rain > 3 ? '<i class="fa-solid fa-cloud-rain" aria-hidden="true"></i> মাঝারি বৃষ্টি হচ্ছে' : '<i class="fa-solid fa-sun" aria-hidden="true"></i> বৃষ্টি নেই'}
                                    </span>
                                </td>
                            </tr>
                            <tr style="background: rgba(39, 174, 96, 0.05);">
                                <td style="font-weight:600; color:var(--text);"><i class="fa-solid fa-location-dot" style="color:#27ae60; margin-right:4px;"></i> ${data.district || name} (নিজ এলাকা)</td>
                                <td style="color:var(--blue); font-weight:600;">${data.weather ? data.weather.rain : 0}</td>
                                <td>${data.weather ? data.weather.humidity : '—'}</td>
                                <td>${data.weather ? data.weather.temp : '—'}</td>
                                <td>
                                    <span style="font-weight:600; color:${localLevelColor};">
                                        ${levelIcon(localLevel)} ${data.river} নদী: ${localLevel}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div style="grid-column: 1 / -1; padding:12px 16px;border-radius:8px;font-size:13px;
                     background:${trendColor}14;
                     border-left:3px solid ${trendColor};
                     color:${trendColor}; margin-bottom: 1rem; line-height: 1.6;">
                    ${trendMsg}
                </div>

                <div class="metric-card">
                    <div class="metric-label">Soil Moisture</div>
                    <div class="metric-value" style="font-size:1.2rem">${data.soil_moisture}</div>
                    <div class="metric-sub">${data.soil_moisture > 0.7 ? '<i class="fa-solid fa-circle-exclamation" style="color:#c0392b"></i> Saturated' : data.soil_moisture > 0.5 ? '<i class="fa-solid fa-triangle-exclamation" style="color:#e67e22"></i> Wet' : '<i class="fa-solid fa-circle-check" style="color:#27ae60"></i> Normal'}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Lag Time</div>
                    <div class="metric-value" style="font-size:1.2rem">${data.lag_time}</div>
                    <div class="metric-sub">ঘণ্টা</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Runoff</div>
                    <div class="metric-value" style="font-size:1.2rem">${data.runoff_mm || 0}</div>
                    <div class="metric-sub">mm</div>
                </div>`;
        }

        const grid = document.getElementById('forecastGrid');
        if(grid && data.forecast) {
            const days = ['আজ','কাল','৩য়','৪র্থ','৫ম','৬ষ্ঠ','৭ম'];
            grid.innerHTML = '';
            data.forecast.slice(0, 7).forEach((d, i) => {
                const val = Math.round(d);
                const fRatio = predLocalRef ? val / predLocalRef : null;
                let label = 'স্বাভাবিক';
                if (fRatio !== null) {
                    if (fRatio > 1) { label = 'বিপদ'; }
                    else if (fRatio > 0.7) { label = 'সতর্ক'; }
                } else {
                    label = val > 15000 ? 'বিপদ' : val > 8000 ? 'সতর্ক' : 'স্বাভাবিক';
                }
                const fStyle = levelStyleFor(label);
                grid.innerHTML += `
                    <div class="forecast-day">
                        <div class="forecast-date">${days[i]}</div>
                        <div class="forecast-icon" style="color:${fStyle.border}">${levelIcon(label)}</div>
                        <div class="forecast-rain">${val.toLocaleString()}</div>
                        <div class="forecast-label" style="color:${fStyle.text}">${label}</div>
                    </div>`;
            });
        }

        if (predLocal && Object.keys(predLocal).length > 0) {
            const riskPercent = document.getElementById('riskPercent');
            const fill = document.getElementById('riskFill');

            if(riskPercent) riskPercent.textContent = predLocal.probability || 0;
            if(fill) {
                fill.style.width = (predLocal.probability || 0) + '%';
                fill.style.background = (predLocal.probability || 0) >= 70 ? '#c0392b' :
                                        (predLocal.probability || 0) >= 50 ? '#e67e22' :
                                        (predLocal.probability || 0) >= 30 ? '#f39c12' : '#27ae60';
            }

            const badge = document.getElementById('warningBadge');
            if(badge) {
                badge.innerHTML = predLocal.level === 'বিপদ' ? `${levelIcon('বিপদ')} বিপদ!` :
                                   predLocal.level === 'সতর্ক' ? `${levelIcon('সতর্ক')} সতর্ক` :
                                   predLocal.level === 'সাবধান' ? `${levelIcon('সাবধান')} সাবধান` : `${levelIcon('নিরাপদ')} নিরাপদ`;
                badge.className = predLocal.level === 'বিপদ' ? 'badge-danger' :
                                 predLocal.level === 'সতর্ক' || predLocal.level === 'সাবধান' ?
                                 'badge-warn' : 'badge-safe';
            }

            const text = document.getElementById('warningText');
            if(text) text.textContent = predLocal.message || data.upstream_warning;

            const oldAction = document.getElementById('actionList');
            if (oldAction) oldAction.remove();

            if(predLocal.action && warningCard) {
                const actionHtml = `
                    <div id="actionList" style="margin-top:1rem">
                        <div style="font-size:12px;font-weight:600;
                             color:var(--text);margin-bottom:8px">
                            📋 এখন যা করবেন:
                        </div>
                        ${predLocal.action.map(a => `
                            <div style="display:flex;gap:8px;margin-bottom:6px;
                                 font-size:13px;color:var(--muted)">
                                <span>→</span><span>${a}</span>
                            </div>
                        `).join('')}
                    </div>`;
                warningCard.insertAdjacentHTML('beforeend', actionHtml);
            }
        }

        loadUnionData(name);
        loadUpstreamForecast(name);

        const lat = data.lat || 23.8103;
        const lon = data.lon || 90.4125;
        loadWeatherForecast(lat, lon);

    } catch(e) {
        console.error("Flood API load error:", e);
        const warningText = document.getElementById('warningText');
        const warningCard = document.getElementById('warningCard');
        if(warningText) warningText.textContent = '❌ Backend চালু নেই বা এরর হয়েছে: py backend/app.py চেক করুন';
        if(warningCard) warningCard.style.display = 'block';
    }
}

// ── CHARTS ──
function initCharts() {
    const fhChart = document.getElementById('floodHistoryChart');
    if(fhChart) {
        new Chart(fhChart, {
            type: 'bar',
            data: {
                labels: ['২০১৫','২০১৬','২০১৭','২০১৮','২০১৯','২০২০','২০২১','২০২২','২০২৩','২০২৪'],
                datasets: [{
                    label: 'ক্ষতিগ্রস্ত মানুষ (লক্ষ)',
                    data: [12, 8, 31, 7, 15, 42, 18, 25, 20, 35],
                    backgroundColor: (ctx) => {
                        const v = ctx.raw;
                        return v >= 30 ? 'rgba(192,57,43,0.7)' :
                               v >= 15 ? 'rgba(230,126,34,0.7)' :
                               'rgba(26,95,168,0.7)';
                    },
                    borderRadius: 6,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {labels: {color: '#4a6080'}},
                    tooltip: { callbacks: { label: (c) => ` ${c.raw} লক্ষ মানুষ` } }
                },
                scales: {
                    x: {ticks: {color: '#4a6080'}, grid: {color: 'rgba(13,31,60,0.06)'}},
                    y: {
                        ticks: {color: '#4a6080'},
                        grid: {color: 'rgba(13,31,60,0.06)'},
                        title: {display: true, text: 'লক্ষ মানুষ', color: '#4a6080'}
                    },
                }
            }
        });
    }

    const rpChart = document.getElementById('riskPieChart');
    if(rpChart) {
        new Chart(rpChart, {
            type: 'doughnut',
            data: {
                labels: ['অতি উচ্চ', 'উচ্চ', 'মাঝারি', 'কম'],
                datasets: [{
                    data: [8, 22, 28, 6],
                    backgroundColor: [
                        'rgba(192,57,43,0.8)',
                        'rgba(230,126,34,0.8)',
                        'rgba(243,156,18,0.8)',
                        'rgba(39,174,96,0.8)',
                    ],
                    borderWidth: 2,
                    borderColor: '#fff',
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom', labels: {color: '#4a6080', padding: 12, font: {size: 11}} },
                    tooltip: { callbacks: { label: (c) => ` ${c.label}: ${c.raw} জেলা` } }
                }
            }
        });
    }

    const mChart = document.getElementById('monthlyChart');
    if(mChart) {
        new Chart(mChart, {
            type: 'line',
            data: {
                labels: ['জান','ফেব','মার','এপ্র','মে','জুন','জুল','আগ','সেপ','অক্ট','নভ','ডিস'],
                datasets: [{
                    label: 'বন্যার ঘটনা',
                    data: [0, 0, 0, 1, 3, 8, 15, 18, 12, 5, 1, 0],
                    borderColor: '#1a5fa8',
                    backgroundColor: 'rgba(26,95,168,0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#1a5fa8',
                    pointRadius: 4,
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: {labels: {color: '#4a6080'}} },
                scales: {
                    x: {ticks: {color: '#4a6080'}, grid: {color: 'rgba(13,31,60,0.06)'}},
                    y: {ticks: {color: '#4a6080'}, grid: {color: 'rgba(13,31,60,0.06)'}},
                }
            }
        });
    }
}

// ── ON WINDOW LOAD ──
window.addEventListener('load', () => {
    initMap();
    initCharts();
    loadAllDistricts();
});

// ── LOAD ALL DISTRICTS TO DROPDOWN ──
async function loadAllDistricts() {
    try {
        const res = await fetch(`${BACKEND}/api/districts`);
        if (!res.ok) throw new Error("API Connection Failed");
        const districts = await res.json();

        const mainSelect = document.getElementById('districtSelect');
        const shelterSelect = document.getElementById('shelterDistrict');
        const reportDistrict = document.getElementById('reportDistrict');
        const signupDistrict = document.getElementById('signupDistrict');

        districts.forEach(d => {
            if(mainSelect) {
                const opt = document.createElement('option');
                opt.value = d; opt.textContent = d;
                mainSelect.appendChild(opt);
            }
            if(shelterSelect) {
                const opt = document.createElement('option');
                opt.value = d; opt.textContent = d;
                shelterSelect.appendChild(opt);
            }
            if(reportDistrict) {
                const opt = document.createElement('option');
                opt.value = d; opt.textContent = d;
                reportDistrict.appendChild(opt);
            }
            if(signupDistrict) {
                const opt = document.createElement('option');
                opt.value = d; opt.textContent = d;
                signupDistrict.appendChild(opt);
            }
        });
    } catch(e) {
        console.error("Districts load error (Backend not running?):", e);
    }
}

// ── SHELTER DATA ──
const shelterData = {
    "রংপুর": [
        {name: "রংপুর সরকারি কলেজ", capacity: 500, address: "রংপুর সদর", phone: "0521-62234"},
        {name: "কারমাইকেল কলেজ", capacity: 800, address: "রংপুর", phone: "0521-63456"},
        {name: "রংপুর জিলা স্কুল", capacity: 300, address: "রংপুর সদর", phone: "0521-64567"},
    ],
    "কুড়িগ্রাম": [
        {name: "কুড়িগ্রাম সরকারি কলেজ", capacity: 400, address: "কুড়িগ্রাম সদর", phone: "0581-61234"},
        {name: "কুড়িগ্রাম উচ্চ বিদ্যালয়", capacity: 250, address: "কুড়িগ্রাম", phone: "0581-62345"},
    ],
    "সিলেট": [
        {name: "এমসি কলেজ", capacity: 600, address: "সিলেট সদর", phone: "0821-71234"},
        {name: "সিলেট সরকারি পাইলট উচ্চ বিদ্যালয়", capacity: 350, address: "সিলেট", phone: "0821-72345"},
        {name: "মদনমোহন কলেজ", capacity: 450, address: "সিলেট", phone: "0821-73456"},
    ],
    "সুনামগঞ্জ": [
        {name: "সুনামগঞ্জ সরকারি কলেজ", capacity: 400, address: "সুনামগঞ্জ সদর", phone: "0871-52234"},
        {name: "সুনামগঞ্জ উচ্চ বিদ্যালয়", capacity: 300, address: "সুনামগঞ্জ", phone: "0871-53456"},
    ],
    "ঢাকা": [
        {name: "ঢাকা কলেজ", capacity: 1000, address: "নিউ মার্কেট, ঢাকা", phone: "02-9667222"},
        {name: "ইডেন মহিলা কলেজ", capacity: 800, address: "আজিমপুর, ঢাকা", phone: "02-9664383"},
    ],
    "গাইবান্ধা": [
        {name: "গাইবান্ধা সরকারি কলেজ", capacity: 500, address: "গাইবান্ধা সদর", phone: "0541-62234"},
        {name: "গাইবান্ধা জিলা স্কুল", capacity: 300, address: "গাইবান্ধা", phone: "0541-63456"},
    ],
};

function loadShelters(district) {
    const container = document.getElementById('shelterList');
    if (!container) return;

    if (!district) {
        container.innerHTML = '';
        return;
    }

    const shelters = shelterData[district] || [];

    if (shelters.length === 0) {
        container.innerHTML = `
            <div style="text-align:center;padding:2rem;color:var(--muted);font-size:14px">
                এই জেলার shelter তথ্য যোগ করা হচ্ছে...<br>
                <small>DDMC থেকে তথ্য সংগ্রহ করা হচ্ছে</small>
            </div>`;
        return;
    }

    container.innerHTML = shelters.map((s, i) => `
        <div style="display:flex;align-items:center;gap:14px;
             padding:14px 0;border-bottom:1px solid var(--border)">
            <div style="width:36px;height:36px;border-radius:8px;
                 background:rgba(26,95,168,0.1);display:flex;
                 align-items:center;justify-content:center;
                 font-size:16px;flex-shrink:0"><i class="fa-solid fa-house-chimney"></i></div>
            <div style="flex:1">
                <div style="font-size:14px;font-weight:600;
                     color:var(--text);margin-bottom:3px">${escapeHtml(s.name)}</div>
                <div style="font-size:12px;color:var(--muted)">
                    📍 ${s.address} &nbsp;|&nbsp;
                    👥 ধারণক্ষমতা: ${s.capacity} জন
                </div>
            </div>
            <a href="tel:${s.phone}"
               style="padding:6px 14px;background:var(--blue);
               color:#fff;border-radius:6px;text-decoration:none;
               font-size:12px;font-weight:600;white-space:nowrap">
                📞 ${s.phone}
            </a>
        </div>
    `).join('');
}

// ── CHATBOT ──
function appendChatMessage(container, type, text) {
    const message = document.createElement('div');
    message.className = `msg ${type}`;
    message.textContent = text;
    container.appendChild(message);
}

function appendTypingIndicator(container) {
    const typing = document.createElement('div');
    typing.className = 'msg bot';
    typing.id = 'typing';
    typing.innerHTML = `
        <span class="typing-dots">
            <span>.</span><span>.</span><span>.</span>
        </span>`;
    container.appendChild(typing);
}

async function sendChat() {
    const input = document.getElementById('chatInput');
    if(!input) return;
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    const msgs = document.getElementById('chatMessages');
    if(!msgs) return;

    appendChatMessage(msgs, 'user', msg);
    appendTypingIndicator(msgs);
    msgs.scrollTop = msgs.scrollHeight;

    try {
        const res = await fetch(`${BACKEND}/api/chat`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        });
        const data = await res.json();

        const typing = document.getElementById('typing');
        if(typing) typing.remove();

        if (data.reply) {
            appendChatMessage(msgs, 'bot', data.reply);
        } else {
            appendChatMessage(msgs, 'bot', '❌ উত্তর পাওয়া যায়নি।');
        }
    } catch(e) {
        const typing = document.getElementById('typing');
        if(typing) typing.remove();
        appendChatMessage(msgs, 'bot', '❌ Backend চালু আছে? python backend/app.py');
    }
    msgs.scrollTop = msgs.scrollHeight;
}

function askQuick(q) {
    const input = document.getElementById('chatInput');
    if(input) {
        input.value = q;
        sendChat();
    }
}

// ── DOWNLOAD PDF ──
function downloadPDF() {
    const districtSelect = document.getElementById('districtSelect');
    if(!districtSelect) return;
    const district = districtSelect.value;
    if (!district) {
        alert('আগে জেলা select করুন!');
        return;
    }
    window.open(`${BACKEND}/api/report/pdf/${encodeURIComponent(district)}`, '_blank');
}

// ── UPSTREAM 7 DAY FORECAST (Light Theme Table Layout) ──
async function loadUpstreamForecast(district) {
    try {
        const res = await fetch(
            `${BACKEND}/api/upstream/forecast/${encodeURIComponent(district)}`
        );
        const data = await res.json();

        if (data.error) return;

        const container = document.getElementById('upstreamCards');
        if(!container) return;

        const oldTable = document.getElementById('upstreamTableWrapper');
        if (oldTable) oldTable.remove();

        let tableHtml = `
            <div id="upstreamTableWrapper" style="grid-column: 1 / -1; width: 100%; margin-top: 1rem;">
                <h3 style="font-size:14px; font-weight:600; color:var(--text); margin-bottom:1rem;">
                    <i class="fa-solid fa-table-list" style="color:var(--blue); margin-right:6px;"></i> উজানের শহরগুলোর আগামী ৭ দিনের অবস্থা:
                </h3>
                <div class="card" style="padding:0; overflow:hidden;">
                    <table class="river-table">
                        <thead style="background: var(--bg);">
                            <tr>
                                <th>তারিখ</th>
                                <th>বৃষ্টি (mm)</th>
                                <th>আর্দ্রতা (%)</th>
                                <th>তাপমাত্রা (°C)</th>
                                <th>অবস্থা</th>
                            </tr>
                        </thead>
                        <tbody>
        `;

        data.forecast.forEach(f => {
            let level = f.impact.includes('🚨') ? 'বিপদ' : f.impact.includes('⚠️') ? 'সতর্ক' : 'স্বাভাবিক';
            let cleanImpact = f.impact.replace('🚨', '').replace('⚠️', '').replace('✅', '').trim();

            tableHtml += `
                <tr>
                    <td style="font-weight:600;">${f.date}</td>
                    <td style="color:var(--blue); font-weight:600;">${f.rain}</td>
                    <td>${f.humidity}</td>
                    <td>${f.temp}</td>
                    <td>${levelBadge(level, cleanImpact)}</td>
                </tr>
            `;
        });

        tableHtml += `</tbody></table></div>`;

        if (data.warnings && data.warnings.length > 0) {
            const warningHtml = data.warnings.map(w => `
                <div style="padding:8px 12px; background:rgba(192,57,43,0.08);
                     border-left:3px solid #c0392b; border-radius:4px;
                     font-size:13px; color:#c0392b; margin-bottom:6px;">
                    <i class="fa-solid fa-triangle-exclamation"></i> ${w.replace('🚨', '')}
                </div>`).join('');

            tableHtml += `
                <div style="margin-top:1rem">
                    <div style="font-size:12px; font-weight:600; color:var(--text); margin-bottom:8px;">
                        <i class="fa-solid fa-circle-exclamation" style="color:#c0392b;"></i> আগামী ৭ দিনের সতর্কতা:
                    </div>
                    ${warningHtml}
                </div>`;
        }

        tableHtml += `</div>`;

        container.insertAdjacentHTML('beforeend', tableHtml);

    } catch(e) {
        console.error('Upstream forecast error:', e);
    }
}

// ── LOAD UNION DATA ──
async function loadUnionData(district) {
    try {
        const res = await fetch(`${BACKEND}/api/unions/${encodeURIComponent(district)}`);
        if(!res.ok) return;
        const data = await res.json();

        if (!data.unions || data.unions.length === 0) return;

        const container = document.getElementById('upstreamCards');
        if(!container) return;

        const oldUnion = document.getElementById('unionDataWrapper');
        if (oldUnion) oldUnion.remove();

        const unionHtml = `
            <div id="unionDataWrapper" style="grid-column:1/-1;margin-top:1.5rem">
                <h3 style="font-size:14px;font-weight:600;
                     color:var(--text);margin-bottom:1rem">
                    <i class="fa-solid fa-house-flood-water" style="color:var(--blue)"></i> ${district} জেলার উচ্চ ঝুঁকিপ্রবণ এলাকা
                </h3>
                ${data.unions.map(u => `
                    <div style="display:flex;gap:12px;padding:10px 0;
                         border-bottom:1px solid var(--border);
                         align-items:flex-start">
                        <div style="width:36px;height:36px;border-radius:8px;
                             background:${u.risk === 'অতি উচ্চ' ?
                             'rgba(192,57,43,0.1)' : 'rgba(230,126,34,0.1)'};
                             display:flex;align-items:center;
                             justify-content:center;font-size:16px;
                             flex-shrink:0"><i class="fa-solid fa-house-flood-water" style="color:${u.risk === 'অতি উচ্চ' ? '#c0392b' : '#e67e22'}"></i></div>
                        <div style="flex:1">
                            <div style="font-size:13px;font-weight:600;
                                 color:var(--text)">
                                ${u.upazila} উপজেলা — ${u.union} ইউনিয়ন
                            </div>
                            <div style="font-size:11px;color:var(--muted);
                                 margin-top:3px">
                                নদী: ${u.river} |
                                উচ্চতা: ${u.elevation}m |
                                জনসংখ্যা: ${u.population.toLocaleString()}
                            </div>
                            <div style="font-size:11px;color:var(--muted)">
                                ${u.notes}
                            </div>
                        </div>
                        <span style="font-size:11px;font-weight:600;
                              padding:3px 8px;border-radius:4px;
                              background:${u.risk === 'অতি উচ্চ' ?
                              'rgba(192,57,43,0.1)' : 'rgba(230,126,34,0.1)'};
                              color:${u.risk === 'অতি উচ্চ' ?
                              '#c0392b' : '#e67e22'};
                              white-space:nowrap">
                            ${u.risk}
                        </span>
                    </div>
                `).join('')}
            </div>`;

        container.insertAdjacentHTML('beforeend', unionHtml);

    } catch(e) {
        console.log('Union API error or not ready yet, skipping...');
    }
}

// ── SATELLITE CARD সরিয়ে ফেলা হয়েছে ──
// আগে এখানে loadSatelliteData() ছিল, যেটা "Satellite Soil Moisture" ও
// "NDWI Index" নামে একটা card দেখাত। কিন্তু এই মান real satellite imagery
// থেকে আসত না — discharge/danger_level অনুপাত থেকে estimate করা হতো
// (backend/satellite.py দেখো)। "NDWI" একটা নির্দিষ্ট, well-defined
// remote-sensing metric, তাই estimated মানকে সেই নামে দেখানো misleading
// ছিল, এবং সাধারণ ইউজারের কাছে soil moisture/AMC-এর মতো টেকনিক্যাল সংখ্যা
// actionable কিছু বলে না। তাই card পুরোপুরি সরানো হলো।
//
// backend/satellite.py ও /api/satellite/<district> endpoint ইচ্ছাকৃতভাবে
// রাখা হয়েছে — ভবিষ্যতে real Sentinel-1 SAR ভিত্তিক satellite integration
// করার সময় এই ফাইলের function-এর কাঠামো reuse করা যাবে।

// ==========================================
// 👉 ৭ দিনের রিয়েল-টাইম আবহাওয়া পূর্বাভাস ফাংশন
// ==========================================
async function loadWeatherForecast(lat, lon) {
    const tableBody = document.getElementById('weatherTableBody');

    if(tableBody) tableBody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding:20px; color:var(--muted);">ডেটা লোড হচ্ছে...</td></tr>`;

    try {
        const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=precipitation_sum&timezone=auto`);
        const data = await response.json();

        const rainData = data.daily.precipitation_sum;
        const dayNames = ["আজ", "কাল", "৩য় দিন", "৪র্থ দিন", "৫ম দিন", "৬ষ্ঠ দিন", "৭ম দিন"];

        if(tableBody) tableBody.innerHTML = "";

        for (let i = 0; i < 7; i++) {
            let rain = rainData[i] || 0;

            let weatherIcon = 'fa-sun';
            let weatherLabel = 'রৌদ্রোজ্জ্বল';
            let level = 'নিরাপদ';

            if (rain > 50) {
                weatherIcon = 'fa-cloud-bolt';
                weatherLabel = 'ভারী বৃষ্টি';
                level = 'বিপদ';
            } else if (rain > 20) {
                weatherIcon = 'fa-cloud-showers-heavy';
                weatherLabel = 'মাঝারি বৃষ্টি';
                level = 'সতর্ক';
            } else if (rain > 0) {
                weatherIcon = 'fa-cloud-rain';
                weatherLabel = 'হালকা বৃষ্টি';
                level = 'স্বাভাবিক';
            } else {
                weatherIcon = 'fa-cloud-sun';
                weatherLabel = 'মেঘলা/রৌদ্রোজ্জ্বল';
                level = 'নিরাপদ';
            }

            const style = levelStyleFor(level);
            const icon = `<i class="fa-solid ${weatherIcon}" style="color:${style.border}" aria-hidden="true"></i> ${weatherLabel}`;
            const rainColor = style.border;
            const riskBadge = levelBadge(level);

            const row = `
                <tr style="border-bottom:1px solid rgba(13,31,60,0.06);">
                    <td style="font-weight:600; padding:11px 12px;">${dayNames[i]}</td>
                    <td style="padding:11px 12px;">${icon}</td>
                    <td style="color:${rainColor}; font-weight:bold; padding:11px 12px;">${rain.toFixed(1)} মিমি</td>
                    <td style="padding:11px 12px;">${riskBadge}</td>
                </tr>
            `;
            if(tableBody) tableBody.innerHTML += row;
        }

    } catch (error) {
        console.error("Weather forecast fetch error:", error);
        if(tableBody) tableBody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:#c0392b;">ডেটা লোড করতে সমস্যা হয়েছে। ইন্টারনেট কানেকশন চেক করুন।</td></tr>`;
    }
}