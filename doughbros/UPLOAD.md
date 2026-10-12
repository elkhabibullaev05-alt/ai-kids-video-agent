# Uploading the day's videos to YouTube (Dough Bros channel)

Channel: **Dough Bros** — @DoughBrosTV — Studio id `UCsQ8TVoioR_IIJpU_1RE_IA` (Google account habibullaeveldorbek57@gmail.com).
Uploads go through the **Claude app's built-in browser** on the user's computer (tools `mcp__remote-devices__Claude_Browser__*`), where the user is already signed in. Never type passwords; if Google asks to sign in, stop and tell the user.

## Schedule (Bishkek time = New York + 10 h; Nov–mid-March New York + 11 h)
Each episode goes to ONE New York day — the day chosen in AGENT.md step 0 (the earliest day with nothing scheduled yet).
| video | New York (that day) | Bishkek (summer time) |
|---|---|---|
| short1 (character moment) | 09:00 | 19:00 same date |
| short2 (question) | 12:00 | 22:00 same date |
| long   | 15:00 | 01:00 next date |
| short3 (teaser) | 18:00 | 04:00 next date |
Studio's schedule picker shows **Bishkek time** on this computer, so pass the Bishkek date/time to `__sched` (e.g. NY 13 Oct 15:00 → Bishkek 14 Oct 01:00). Never pick a slot less than 30 min in the future.

## 1. Host the files temporarily
The browser can't read the cloud workspace, so push the day's files to the orphan branch `uploads` (force-push replaces the previous day):
```bash
rm -rf /tmp/upl && mkdir /tmp/upl && cd /tmp/upl && git init -q && git checkout -q --orphan uploads
O=<repo>/doughbros/out; N=epNNN
for s in long short1 short2 short3; do cp $O/${N}_$s/${N}_$s.mp4 .; done
cp $O/${N}_long/thumbnail.png ${N}_long_thumb.png
git add . && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "upload $N"
git push -q -f https://github.com/elkhabibullaev05-alt/ai-kids-video-agent uploads
```
Files are then at `https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/uploads/<file>`.

## 2. Open Studio and download the files into the page
`preview_start` → `https://studio.youtube.com/channel/UCsQ8TVoioR_IIJpU_1RE_IA/videos/upload?d=ud`, wait 5 s, check the page shows "Dough Bros" (not another channel). Then (javascript_tool; returns immediately, poll after ~60 s):
```js
window.__dl={}; const go=async n=>{const r=await fetch('https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/uploads/'+n); window.__dl[n]=await r.blob();};
Promise.all(['epNNN_long.mp4','epNNN_short1.mp4','epNNN_short2.mp4','epNNN_short3.mp4','epNNN_long_thumb.png'].map(go)); 'started'
```
Poll: `Object.fromEntries(Object.entries(window.__dl).map(([k,v])=>[k,v.size]))` until all 5 are present. **Don't reload the page after this** (the blobs live in the page).

## 3. Helper functions (define once)
```js
window.__open = async (file) => { const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 [...document.querySelectorAll('ytcp-video-share-dialog ytcp-button, ytcp-video-share-dialog button')].find(b=>b.innerText.trim()==='Закрыть')?.click(); await sleep(1500);
 if(!document.querySelector('ytcp-uploads-file-picker input[type=file]')){ document.querySelector('#create-icon')?.click(); await sleep(1000);
  [...document.querySelectorAll('tp-yt-paper-item')].find(e=>e.innerText.includes('Добавить видео'))?.click(); await sleep(2000);}
 const inp=document.querySelector('ytcp-uploads-file-picker input[type=file]'); if(!inp) return 'no picker';
 const dt=new DataTransfer(); dt.items.add(new File([window.__dl[file]], file, {type:'video/mp4'})); inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true})); return 'uploading '+file; };
window.__fill = async (title, desc, tags) => { const sleep=ms=>new Promise(r=>setTimeout(r,ms)); await sleep(3000);
 const dlg=document.querySelector('ytcp-uploads-dialog');
 const setTb=(el,txt)=>{el.focus(); document.execCommand('selectAll',false,null); document.execCommand('insertText',false,txt); el.dispatchEvent(new Event('input',{bubbles:true}));};
 const tbs=[...dlg.querySelectorAll('#textbox')]; setTb(tbs[0], title); await sleep(500); setTb(tbs[1], desc); await sleep(500);
 const mfk=dlg.querySelector('tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]'); mfk.click(); await sleep(800);
 dlg.querySelector('#toggle-button')?.click(); await sleep(1200);
 const tag=dlg.querySelector('input[aria-label="Теги"]'); tag.focus(); document.execCommand('insertText',false,tags+',');
 tag.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true})); await sleep(800);
 return [tbs[0].innerText, mfk.getAttribute('aria-checked'), dlg.querySelectorAll('ytcp-chip').length]; };
window.__thumb = (file) => { const t=document.querySelector('ytcp-uploads-dialog #file-loader');
 const dt=new DataTransfer(); dt.items.add(new File([window.__dl[file]],'thumb.png',{type:'image/png'})); t.files=dt.files; t.dispatchEvent(new Event('change',{bubbles:true})); return 'thumb set'; };
window.__sched = async (day, time) => { const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const dlg=document.querySelector('ytcp-uploads-dialog');
 for (let i=0;i<3;i++){ dlg.querySelector('#next-button').click(); await sleep(1800);} dlg.querySelector('#second-container-expand-button').click(); await sleep(1200);
 const c=dlg.querySelector('#second-container');
 if (!c.querySelector('#datepicker-trigger').innerText.trim().startsWith(day+' ')) { c.querySelector('#datepicker-trigger').click(); await sleep(1200);
  [...document.querySelectorAll('ytcp-date-picker [class*=day]')].find(e=>e.innerText.trim()===String(day) && e.offsetParent)?.click(); await sleep(800); }
 const t=c.querySelector('input'); t.focus(); t.select(); document.execCommand('insertText',false,time); t.dispatchEvent(new Event('input',{bubbles:true})); t.dispatchEvent(new Event('change',{bubbles:true})); t.blur(); await sleep(1000);
 return [c.querySelector('#datepicker-trigger').innerText.trim(), t.value]; };
window.__done = async () => { document.querySelector('ytcp-uploads-dialog #done-button').click(); await new Promise(r=>setTimeout(r,5000));
 return document.querySelector('ytcp-video-share-dialog')?.innerText?.slice(0,140); };
'ok'
```
(The Studio UI is in Russian on this account. Keep each javascript_tool call short — they time out after 45 s.)

## 4. For each video (separate calls, check every result)
1. `await window.__open('epNNN_short1.mp4')` → "uploading …"
2. `await window.__fill(title, description, tags)` → title echoed, `"true"`, chip count > 0 (title/description/tags from that video's `upload.txt`; asking viewers to comment is fine — the channel is not made for kids)
3. long video only: `window.__thumb('epNNN_long_thumb.png')`
4. `await window.__sched(DAY, 'HH:MM')` → returns the date and time you asked for. If the date is wrong, take a screenshot and click the right day in the calendar.
5. `await window.__done()` → must say "Публикация видео запланирована" with the right date/time.
Order: short1, short2, long, short3.

## 5. Clean up
`git push https://github.com/elkhabibullaev05-alt/ai-kids-video-agent --delete uploads` after all four are scheduled.

If anything fails (not signed in, wrong channel, computer not reachable): skip uploading, still deliver the files to the user, and explain in the final message.
