/**
 * Like counter for Mami's Musings — a Google Apps Script web app.
 *
 * Setup (one time, ~3 minutes):
 *  1. Go to https://script.google.com → New project. Name it "Mami's Musings likes".
 *  2. Delete everything in Code.gs and paste this whole file. Save.
 *  3. Deploy → New deployment → gear icon → Web app.
 *       Execute as: Me        Who has access: Anyone
 *     Click Deploy, authorise with your Google account (Advanced → Go to … (unsafe) is normal
 *     for your own scripts), and copy the Web app URL (ends in /exec).
 *  4. Paste that URL into _config.yml →  likes_endpoint: "https://script.google.com/macros/s/…/exec"
 *  5. tools/publish.sh "Enable likes"
 *
 * Counts live in this script's Project Settings → Script properties (like:012 = 7, …).
 * If you edit this code later, use Deploy → Manage deployments → Edit → New version,
 * so the URL stays the same.
 */
const PROPS = PropertiesService.getScriptProperties();

function doGet(e) {
  const p = (e && e.parameter) || {};
  const id = String(p.id || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 40);
  let out;

  if ((p.action === 'like' || p.action === 'unlike') && id) {
    const lock = LockService.getScriptLock();
    lock.waitLock(5000);
    try {
      const key = 'like:' + id;
      let n = Number(PROPS.getProperty(key) || 0);
      n = p.action === 'like' ? n + 1 : Math.max(0, n - 1);
      PROPS.setProperty(key, String(n));
      out = { id: id, count: n };
    } finally {
      lock.releaseLock();
    }
  } else {
    const all = PROPS.getProperties();
    const counts = {};
    Object.keys(all).forEach(function (k) {
      if (k.indexOf('like:') === 0) counts[k.slice(5)] = Number(all[k]) || 0;
    });
    out = { counts: counts };
  }

  return ContentService.createTextOutput(JSON.stringify(out))
    .setMimeType(ContentService.MimeType.JSON);
}
