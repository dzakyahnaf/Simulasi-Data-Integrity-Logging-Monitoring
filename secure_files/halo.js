const crypto = require('crypto');

// /d:/AITIES/Semester_5/KWA/Simulasi-Data-Integrity-Logging-Monitoring/secure_files/halo.js
// Random JS utility: generates "halo" records with HMAC signatures and verifies them.


function randomId(len = 8) {
    return crypto.randomBytes(Math.ceil(len / 2)).toString('hex').slice(0, len);
}

function nowIso() {
    return new Date().toISOString();
}

function generateHalo(overrides = {}) {
    const halo = {
        id: randomId(10),
        createdAt: nowIso(),
        radius: (Math.random() * 10 + 1).toFixed(2),
        color: ['cyan', 'magenta', 'gold', 'emerald'][Math.floor(Math.random() * 4)],
        metadata: {
            origin: ['satellite', 'drone', 'sensor'][Math.floor(Math.random() * 3)],
            confidence: +(Math.random()).toFixed(3)
        },
        ...overrides
    };
    return halo;
}

function signObject(obj, key) {
    const payload = JSON.stringify(obj);
    const h = crypto.createHmac('sha256', key).update(payload).digest('hex');
    return { payload: obj, signature: h };
}

function verifySigned(signed, key) {
    const expected = crypto.createHmac('sha256', key).update(JSON.stringify(signed.payload)).digest('hex');
    return expected === signed.signature;
}

// Simple CLI demo when run directly
if (require.main === module) {
    const key = process.env.HALO_KEY || crypto.randomBytes(16).toString('hex');
    console.log('HALO KEY:', key);
    const items = [];
    for (let i = 0; i < 5; i++) {
        const h = generateHalo();
        const s = signObject(h, key);
        items.push(s);
        console.log(`Generated halo ${h.id} signed: ${s.signature.slice(0, 12)}...`);
    }

    console.log('\nVerifying items...');
    items.forEach((it, idx) => {
        const ok = verifySigned(it, key);
        console.log(`#${idx + 1} id=${it.payload.id} valid=${ok}`);
    });

    // Tamper test
    const tampered = JSON.parse(JSON.stringify(items[0]));
    tampered.payload.radius = (parseFloat(tampered.payload.radius) + 5).toFixed(2);
    console.log('\nTamper test (should be false):', verifySigned(tampered, key));
}

module.exports = {
    generateHalo,
    signObject,
    verifySigned
};