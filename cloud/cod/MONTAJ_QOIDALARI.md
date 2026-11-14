# MW4 / CoD Shorts montaj qoidalari (egasi, 2026-11-14)
Sabab: Ask Studio — 67% tomoshabin darrov o'tkazib yuboradi. To'liq: C:\Users\1\Documents\YouTube-kanallar\MW4-million-strategiya.md

1. Birinchi kadr = harakat (otishma, portlash yoki qahramon yuzi). Yugurib kelish, qurol ko'rsatish, menyu kesiladi.
2. 0-soniyadan tepada katta matn: savol yoki va'da (masalan "Price buni kechirmadi").
3. 0-soniyada ovoz (qahramon gapi, portlash yoki musiqa urg'usi) — jim boshlanmaydi.
4. Uzunlik 9–15 s; oxirgi kadr boshiga ulanadigan loop (qora fade yo'q).
5. Grafika/cinematic Shorts musiqa beat'iga kesiladi.
6. Nom aniq qiziqish bilan, hech qachon takrorlanmaydi; heshteg faqat `#mw4 #callofduty`.
7. Kuniga 2–3 ta, 4–6 soat oraliq bilan; bir soatda bir nechta yuklanmaydi.
8. Bitta kesma boshqa nom bilan qayta yuklanmaydi.

Kodda: short4.py (1,3,4 — oyna otishmadan boshlanadi, 9–15 s, fade yo'q), auto_gameplay.py (9–15 s, nom heshteglari),
cod_upload.py (6,7,8 — kuniga 3 ta, UTC 4/9/14 = Osh 09/14/19; takror nom/kesma o'tkaziladi).
Claude job.json'ga yt_title/hook yozganda va v4_ok.json'ni tasdiqlaganda 1, 2, 5, 6 ni ko'z bilan tekshiradi.
