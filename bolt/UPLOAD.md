# Uploading a video to YouTube (Inspector Bolt channel)

Channel: **Inspector Bolt** — id `UCv2hAyDv5m8Rm-0L63a93XQ`, account halilovelbek558@gmail.com, Studio `authuser=4` (`story/log.json → channel`). **Always check the page shows "Inspector Bolt" before uploading.** Every video is **Made for Kids = YES** (COPPA).
Uploads go through the **Claude app's built-in browser** on the user's computer (`mcp__remote-devices__Claude_Browser__*`). Never type passwords; if Google asks to sign in, stop and tell the user. Open your **own tab** and pass its `tabId` to every call (Doodle Desk / Dough Bros / Hollowmere tasks may use the browser at the same time).
Switching accounts: open `https://studio.youtube.com/?authuser=N` (N = 0…5) and read `location.href` after ~3 s to find which index lands on the channel; for a second channel of the same account use `https://www.youtube.com/channel_switcher?authuser=N`.
Studio's schedule picker shows **Bishkek time (UTC+6)**: convert the UTC slot from AGENT.md.

## 1. Host the files (orphan branch `uploads-bolt-epNNN`, one per episode)
```bash
N=epNNN; rm -rf /tmp/upld && mkdir /tmp/upld && cd /tmp/upld && git init -q && git checkout -q --orphan uploads-bolt-$N
O=<repo>/bolt/out
cp $O/$N.mp4 bolt_$N.mp4; cp $O/${N}_thumb.jpg bolt_${N}_thumb.jpg
for f in $O/${N}_s?.mp4 $O/${N}_s?_d.mp4; do [ -f "$f" ] && cp "$f" bolt_$(basename "$f"); done   # only the files that passed rek-ball
git add . && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "upload $N" && git push -q -f https://github.com/elkhabibullaev05-alt/ai-kids-video-agent uploads-bolt-$N
```
Every file must be < 100 MB. Files: `https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/uploads-bolt-epNNN/<file>`.

## 2. Open Studio and download the files into the page
Open `https://studio.youtube.com/channel/<CHANNEL_ID>/videos/upload?d=ud`, wait 5 s, check the channel name. Then:
```js
window.__dl={}; const go=async n=>{const r=await fetch('https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/uploads-bolt-epNNN/'+n); window.__dl[n]=await r.blob();};
Promise.all(['bolt_epNNN.mp4','bolt_epNNN_thumb.jpg','bolt_epNNN_s1.mp4','bolt_epNNN_s2.mp4'].map(go)); 'started'
```
Poll `Object.fromEntries(Object.entries(window.__dl).map(([k,v])=>[k,v.size]))` until both are there. Don't reload the page afterwards.

## 3. Helper functions (define once)
```js
window.__new = async () => { const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 [...document.querySelectorAll('ytcp-video-share-dialog ytcp-button, ytcp-video-share-dialog button')].find(b=>['Закрыть','Yopish','Close'].includes(b.innerText.trim()))?.click(); await sleep(1500);
 if(!document.querySelector('ytcp-uploads-file-picker input[type=file]')){ document.querySelector('#create-icon, [aria-label="Создать"], [aria-label="Yaratish"], [aria-label="Create"]')?.click(); await sleep(1200); document.querySelector('#text-item-0')?.click(); await sleep(2500);}
 return !!document.querySelector('ytcp-uploads-file-picker input[type=file]'); };
window.__open = async (file) => { await window.__new(); const inp=document.querySelector('ytcp-uploads-file-picker input[type=file]'); if(!inp) return 'no picker';
 const dt=new DataTransfer(); dt.items.add(new File([window.__dl[file]], file, {type:'video/mp4'})); inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true})); return 'uploading '+file; };
window.__fill = async (title, desc, tags) => { const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 let dlg; for (let i=0;i<20;i++){ dlg=document.querySelector('ytcp-uploads-dialog'); if (dlg && dlg.querySelectorAll('#textbox').length>=2 && dlg.querySelector('#textbox').innerText.trim()) break; await sleep(1000);} await sleep(1500);
 const setTb=async (el,txt)=>{ el.click(); el.focus(); await sleep(300); const sel=window.getSelection(); const rg=document.createRange(); rg.selectNodeContents(el); sel.removeAllRanges(); sel.addRange(rg); document.execCommand('insertText',false,txt); el.dispatchEvent(new Event('input',{bubbles:true}));};
 const tbs=[...dlg.querySelectorAll('#textbox')]; await setTb(tbs[0], title); await sleep(500); await setTb(tbs[1], desc); await sleep(500);
 const mfk=dlg.querySelector('tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_MFK]'); mfk.click(); await sleep(800);
 if(!dlg.querySelector('input[aria-label="Теги"], input[aria-label="Teglar"], input[aria-label="Tags"]')){ dlg.querySelector('#toggle-button')?.click(); await sleep(1500);}
 const tag=dlg.querySelector('input[aria-label="Теги"], input[aria-label="Teglar"], input[aria-label="Tags"]'); tag.focus(); document.execCommand('insertText',false,tags+',');
 tag.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true})); await sleep(800);
 return [tbs[0].innerText, mfk.getAttribute('aria-checked'), dlg.querySelectorAll('ytcp-chip').length]; };
window.__thumb = (file) => { const t=document.querySelector('ytcp-uploads-dialog #file-loader');
 const dt=new DataTransfer(); dt.items.add(new File([window.__dl[file]],'thumb.jpg',{type:'image/jpeg'})); t.files=dt.files; t.dispatchEvent(new Event('change',{bubbles:true})); return 'thumb set'; };
window.__pickDay = async (day) => { const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const c=document.querySelector('ytcp-uploads-dialog #second-container');
 if (c.querySelector('#datepicker-trigger').innerText.trim().startsWith(day+' ')) return 'already';
 c.querySelector('#datepicker-trigger').click();
 for (let i=0;i<10;i++){ await sleep(500); const cand=[...document.querySelectorAll('ytcp-scrollable-calendar *, ytcp-date-picker *')].filter(e=>e.children.length===0 && e.textContent.trim()===String(day) && e.getClientRects().length && !/disabled/.test(e.className+e.parentElement.className));
  if (cand.length){ (cand[0].closest('[class*=calendar-day]')||cand[0]).click(); await sleep(1000); return c.querySelector('#datepicker-trigger').innerText.trim(); } }
 return 'day not found'; };
window.__pickTime = async (time) => { const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const c=document.querySelector('ytcp-uploads-dialog #second-container'); const t=c.querySelector('input'); t.click();
 for (let i=0;i<10;i++){ await sleep(500); const it=[...document.querySelectorAll('tp-yt-paper-item')].find(e=>e.getClientRects().length && e.innerText.trim()===time); if (it){ it.scrollIntoView(); it.click(); await sleep(1000); return t.value; } }
 return 'time not found'; };
// time can't be typed — it must be picked from the 15-minute list (typing silently keeps 00:00)
window.__sched = async (day, time) => { const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const dlg=document.querySelector('ytcp-uploads-dialog');
 for (let i=0;i<3;i++){ dlg.querySelector('#next-button').click(); await sleep(1800);} dlg.querySelector('#second-container-expand-button').click(); await sleep(1500);
 const a=await window.__pickDay(day); await sleep(600); const b=await window.__pickTime(time); const c=dlg.querySelector('#second-container'); return [a,b,c.querySelector('#datepicker-trigger').innerText.trim(), c.querySelector('input').value]; };
window.__done = async () => { const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 for(let i=0;i<40;i++){ const b=document.querySelector('ytcp-uploads-dialog #done-button'); if(b.getAttribute('aria-disabled')!=='true') break; await sleep(1000);}
 document.querySelector('ytcp-uploads-dialog #done-button').click(); await sleep(5000);
 return document.querySelector('ytcp-video-share-dialog')?.innerText?.slice(0,140) || 'no share dialog yet — wait and check'; };
'ok'
```
(Studio UI is in **Uzbek** (tags field "Teglar", publish button "Chop etish"). Keep each javascript_tool call short — they time out after 45 s; never chain __open + __fill + __sched in one call. Page navigation wipes `window.__*` — define the helpers again after any reload. Screenshots of the built-in browser can be stale: read state with JS (`document.querySelector('ytcp-uploads-dialog').innerText`). If the dialog gets stuck with Next/Done disabled, close it (the video is kept as a private draft), open `studio.youtube.com/video/<id>/edit`, and set the schedule there; then check the Shorts/Videos list shows "Rejalashtirilgan" + the date.)

## 4. Upload (separate calls, check every result)
1. `await window.__open('bolt_epNNN.mp4')` → "uploading …"
2. `await window.__fill(title, description, tags)` (from that video's `upload.txt`) → title echoed (if it echoes the file name, wait 8 s and call again), `"true"` (= made for kids — required on this channel), chips > 0
3. `window.__thumb('bolt_epNNN_thumb.jpg','bolt_epNNN_s1.mp4','bolt_epNNN_s2.mp4')`
4. `await window.__sched(DAY, 'HH:MM')` → returns the date and time you asked for (twice).
5. `await window.__done()` → "Публикация видео запланирована" with the right date/time. For the long video a "Обработка видео" dialog appears instead: read the date in it, then close it (button "Закрыть" in `ytcp-uploads-still-processing-dialog`).
   Wrong time? Open `studio.youtube.com/video/<id>/edit` → Параметры доступа → pick the time from the list → ОК → Сохранить.
   Stuck on "Сохранение…" for minutes → reload the upload page, download the blobs again, upload again.
Also upload `subs_en.srt` later if Studio offers it (optional).

If anything fails (not signed in, wrong channel, computer unreachable): skip uploading, still deliver the files and explain in the final message.
