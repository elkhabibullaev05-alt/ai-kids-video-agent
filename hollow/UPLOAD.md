# Uploading the day's videos to YouTube (Hollowmere Tales channel)

Channel: **Hollowmere Tales** — @HollowmereTalesTV — Studio id `UCiOfdnuWUlHj5bPi6H5scgA` (Google account habibullaeveldorbek57@gmail.com, same account as Dough Bros — **always check the page shows "Hollowmere Tales" before uploading**).
Uploads go through the **Claude app's built-in browser** on the user's computer (`mcp__remote-devices__Claude_Browser__*`). Never type passwords; if Google asks to sign in, stop and tell the user. Open your **own tab** with `preview_start` and pass its `tabId` to every call (the Dough Bros task may use the browser at the same time).

## Schedule (Bishkek = New York + 10 h; Nov–mid-March + 11 h)
Each episode goes to ONE New York day (AGENT.md step 0).
| video | New York (that day) | Bishkek (summer time) |
|---|---|---|
| short1 (the rule) | 11:00 | 21:00 same date |
| short2 (would you) | 16:00 | 02:00 next date |
| long | 20:00 | 06:00 next date |
| short3 (scariest moment) | 22:00 | 08:00 next date |
Studio's schedule picker shows **Bishkek time**: pass the Bishkek day number and time to `__sched`. Never pick a slot less than 30 min ahead.

## 1. Host the files temporarily (orphan branch `uploads-hollow`)
```bash
rm -rf /tmp/uplh && mkdir /tmp/uplh && cd /tmp/uplh && git init -q && git checkout -q --orphan uploads-hollow
O=<repo>/hollow/out; N=epNNN
for s in long short1 short2 short3; do cp $O/${N}_$s/${N}_$s.mp4 hollow_${N}_$s.mp4; done
cp $O/${N}_long/thumbnail.png hollow_${N}_long_thumb.png
git add . && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "upload $N" && git push -q -f https://github.com/elkhabibullaev05-alt/ai-kids-video-agent uploads-hollow
```
Files: `https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/uploads-hollow/<file>`.

## 2. Open Studio and download the files into the page
`preview_start` → `https://studio.youtube.com/channel/UCiOfdnuWUlHj5bPi6H5scgA/videos/upload?d=ud`, wait 5 s, check the page shows "Hollowmere Tales". Then:
```js
window.__dl={}; const go=async n=>{const r=await fetch('https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/uploads-hollow/'+n); window.__dl[n]=await r.blob();};
Promise.all(['hollow_epNNN_short1.mp4','hollow_epNNN_short2.mp4','hollow_epNNN_short3.mp4','hollow_epNNN_long_thumb.png','hollow_epNNN_long.mp4'].map(go)); 'started'
```
Poll `Object.fromEntries(Object.entries(window.__dl).map(([k,v])=>[k,v.size]))` until all 5 are there. Don't reload the page afterwards.

## 3. Helper functions (define once)
```js
window.__new = async () => { const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 [...document.querySelectorAll('ytcp-video-share-dialog ytcp-button, ytcp-video-share-dialog button')].find(b=>b.innerText.trim()==='Закрыть')?.click(); await sleep(1500);
 if(!document.querySelector('ytcp-uploads-file-picker input[type=file]')){ document.querySelector('#create-icon, [aria-label="Создать"]')?.click(); await sleep(1200); document.querySelector('#text-item-0')?.click(); await sleep(2500);}
 return !!document.querySelector('ytcp-uploads-file-picker input[type=file]'); };
window.__open = async (file) => { await window.__new(); const inp=document.querySelector('ytcp-uploads-file-picker input[type=file]'); if(!inp) return 'no picker';
 const dt=new DataTransfer(); dt.items.add(new File([window.__dl[file]], file, {type:'video/mp4'})); inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true})); return 'uploading '+file; };
window.__fill = async (title, desc, tags) => { const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 let dlg; for (let i=0;i<20;i++){ dlg=document.querySelector('ytcp-uploads-dialog'); if (dlg && dlg.querySelectorAll('#textbox').length>=2 && dlg.querySelector('#textbox').innerText.trim()) break; await sleep(1000);} await sleep(1500);
 const setTb=async (el,txt)=>{ el.click(); el.focus(); await sleep(300); const sel=window.getSelection(); const rg=document.createRange(); rg.selectNodeContents(el); sel.removeAllRanges(); sel.addRange(rg); document.execCommand('insertText',false,txt); el.dispatchEvent(new Event('input',{bubbles:true}));};
 const tbs=[...dlg.querySelectorAll('#textbox')]; await setTb(tbs[0], title); await sleep(500); await setTb(tbs[1], desc); await sleep(500);
 const mfk=dlg.querySelector('tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]'); mfk.click(); await sleep(800);
 if(!dlg.querySelector('input[aria-label="Теги"]')){ dlg.querySelector('#toggle-button')?.click(); await sleep(1500);}
 const tag=dlg.querySelector('input[aria-label="Теги"]'); tag.focus(); document.execCommand('insertText',false,tags+',');
 tag.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true})); await sleep(800);
 return [tbs[0].innerText, mfk.getAttribute('aria-checked'), dlg.querySelectorAll('ytcp-chip').length]; };
window.__thumb = (file) => { const t=document.querySelector('ytcp-uploads-dialog #file-loader');
 const dt=new DataTransfer(); dt.items.add(new File([window.__dl[file]],'thumb.png',{type:'image/png'})); t.files=dt.files; t.dispatchEvent(new Event('change',{bubbles:true})); return 'thumb set'; };
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
(The Studio UI is in Russian. Keep each javascript_tool call short — they time out after 45 s.)

## 4. For each video (separate calls, check every result)
1. `await window.__open('hollow_epNNN_short1.mp4')` → "uploading …"
2. `await window.__fill(title, description, tags)` (from that video's `upload.txt`) → title echoed (if it echoes the file name, wait 8 s and call again), `"true"` (= NOT made for kids), chips > 0
3. long only: `window.__thumb('hollow_epNNN_long_thumb.png')`
4. `await window.__sched(DAY, 'HH:MM')` → returns the date and time you asked for (twice).
5. `await window.__done()` → "Публикация видео запланирована" with the right date/time. For the long video a "Обработка видео" dialog appears instead: read the date in it, then close it (button "Закрыть" in `ytcp-uploads-still-processing-dialog`).
   Wrong time? Open `studio.youtube.com/video/<id>/edit` → Параметры доступа → pick the time from the list → ОК → Сохранить.
   Stuck on "Сохранение…" for minutes → reload the upload page, download the blobs again, upload again.
Order: short1, short2, long, short3.

If anything fails (not signed in, wrong channel, computer unreachable): skip uploading, still deliver the files and explain in the final message.

## Known pitfalls (2026-10-16)
- YouTube may first show a **"Choose a channel"** picker (Hollowmere Tales / Dough Bros) — click Hollowmere Tales.
- The channel has old **upload defaults** (title "#FunnyVideos…", description "Funny pranks…", tags prank/funny/viral/prankpop/comedy/joke/fun). `__fill` must replace them, and the default tag chips must be removed (click each chip's `#delete-icon`). Check the echo: if the title still shows "#FunnyVideos…", `execCommand` had no focus — do one real `left_click` into the title box with the computer tool, then call `__fill` again.
- `__pickDay`/`__pickTime` can miss while the pane is hidden: retry with a loop over `ytcp-scrollable-calendar span.calendar-day` and visible `tp-yt-paper-item`. The time list has 15-minute steps → use minutes :15 or :45.
- On the video edit page, the Save button (`#save`) often ignores a JS `.click()` — click it with the computer tool and reload to verify.
- The browser downloads at ~150 KB/s; an 80 MB long takes ~8–10 min — use a streaming reader with a progress counter and never start the same download twice.
- The cloud container can restart mid-run and kill background renders: check `uptime`/`pgrep -f render.py` when polling and restart the loop (it skips finished videos).
