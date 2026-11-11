# Video skilllari (2026-11-11)

Har bir videoni yuklashdan oldin quyidagi tartibda tekshiring:

| # | Skill | Nima qiladi |
|---|---|---|
| 1 | `video-watch/` | Videoni odam ko'zi bilan "ko'radi": vaqt belgili kadrlar, birinchi kadr, montaj kesimlari, takroriy kadrlar, sukut va ovoz balandligi. Keyin tomoshabin va muharrir sifatida baho beradi. |
| 2 | `video-retention/` | Necha foiz ko'rilishini bashorat qiladi: soniyama-soniya egri chiziq, o'rtacha % ko'rish, Shorts "stayed to watch". Recommend chiqadimi yoki yo'qmi, hukm chiqaradi va qayerni qanday sozlash kerakligini aytadi. |
| 3 | `video-polish/` | Full HD/1440p/4K, aniqroq tasvir, rang (natural/vivid/warm/cinematic), ovozni −14 LUFS ga keltiradi, sukut va takrorlarni kesadi, subtitr qo'shadi, YouTube uchun yuqori bitrate eksport qiladi. |

Repoda oldindan bor skill va asboblar (ular bilan birga ishlatiladi):
- `cloud/ink/tomoshabin-bahosi/SKILL.md`: ssenariyni tomoshabin ko'zi bilan 100 ballik baholaydi (85 dan o'tishi kerak).
- `tools/rek_ball.py`: render qilingan MP4 ni mexanik 100 ballik baholaydi (yuklash darvozasi).
- `tools/make_short.py`: uzun videodan Shorts kesadi.
- `cloud/growth/studio-maslahat/SKILL.md`: Ask Studio maslahati.

Ishlash tartibi:
```
video-watch → video-retention → (muammo bo'lsa) video-polish --cut/--trim-silence → video-retention qayta → yuklash
```

Kerakli dasturlar: `ffmpeg`, `ffprobe`, Python 3, `numpy`, `Pillow` (`matplotlib` ixtiyoriy).
Ovozni matnga o'girish uchun ixtiyoriy: `pip install faster-whisper`. Bulutda model
yuklanmaydi, noutbukda esa ishlaydi.

## Noutbukda (Claude ilovasi) skill sifatida o'rnatish
Claude ilovasida: Sozlamalar → Capabilities/Skills → "Upload skill", keyin
`video-watch.skill`, `video-retention.skill`, `video-polish.skill` fayllarini yuklang.
Bu fayllarni Claude chatda yuborgan. Bu bandni faqat egasi o'zi bajara oladi, agent
uni avtomatik qila olmaydi. Repodagi nusxani noutbuk worker'i 20 daqiqa ichida o'zi
tortib oladi, agentlar skriptlarni `skills/<nom>/scripts/` dan to'g'ridan-to'g'ri ishlatadi.

## GitHub'da topilgan ommaviy video skilllar (tekshirilmagan, faqat ma'lumot uchun)
Bular boshqa mualliflarning kodi. O'rnatishdan oldin kodini o'qib chiqish kerak.
- OpenMontageInc/OpenMontage: agentli video ishlab chiqarish tizimi, 12 ta pipeline
- nateherkai/herk-edit-kit: reels/Shorts montaji, Claude Code/Codex uchun
- Agentchengfeng/chengfeng-videocut-skills: Claude Code video kesish skilllari
- pycodebr/heditor: vertikal video montaj skilli
- 6missedcalls/video-editing-skill: trim, jump cut, subtitr
- artemisln/edit-reel: karaoke subtitr, takrorlarni olib tashlash
- Vincentwei1021/anything2explainer: mavzudan izohli video
- haidrrrry/claude-remotion-skill: Remotion bilan video yasash
