# Bulut serverlar — har bir kanal o'z serverida (Claude'siz render va yuklash)

**Kim nima qiladi:**
- **Claude:** har kuni hikoyalarni yozadi (`cloud/WRITER.md`) va kechqurun natijani tekshiradi (`cloud/REVIEW.md`). Videolar bir xil bo'lmasligini ham Claude nazorat qiladi.
- **Server:** qolgan hamma ishni o'zi qiladi. Ovoz, 3D render, musiqa, montaj, rek-ball (≥ 85), Shorts, 7 tilda sarlavha va jadval bo'yicha YouTube'ga yuklash.
- **Server qo'shimcha himoyasi:**
  - Eski videoga o'xshash hikoyani o'zi rad etadi.
  - Token boshqa kanalniki bo'lsa, ishni to'xtatadi. Shu tufayli video hech qachon noto'g'ri kanalga tushmaydi.

| kanal | server nomi | kuniga |
|---|---|---|
| Inspector Bolt | `bolt` | 2 long + 5 Shorts |
| Dough Bros | `doughbros` | 3 long + 4 Shorts |
| Hollowmere Tales | `hollow` | 3 long + 4 Shorts |
| Max the Curious Cat | `maxcat` | 3 long + 4 Shorts |

## Siz qiladigan ishlar (bir marta)

### 1. 4 ta server oching
- Har kanalga bitta server: Ubuntu 24.04, kamida **8 vCPU, 16 GB RAM, 80 GB disk**.
- Mos keladiganlar: Hetzner, DigitalOcean, Vultr va boshqalar.
- 8 yadroda bitta long ~1.5–2 soatda tayyor bo'ladi. Shunda kuniga 3 ta long bemalol sig'adi.

### 2. Har bir serverda bitta buyruq ishga tushiring
Root bo'lib, kanal nomini o'zgartirib:
```
curl -sSL https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/main/cloud/install.sh | bash -s doughbros
```
Oxirida ekranga `ssh-ed25519 ...` bilan boshlanadigan kalit chiqadi.

### 3. Kalitni GitHub'ga qo'shing
GitHub → repo → **Settings → Deploy keys → Add deploy key**:
- Kalitni joylang.
- **Allow write access** belgisini qo'ying.

Har bir server uchun alohida qiling. Bu kalit faqat shu bitta repoga ishlaydi.

### 4. YouTube ruxsatini oling (kompyuteringizda, har kanalga bir marta)

**4a. Google loyiha yarating**
- Google Cloud Console'da **har kanal uchun alohida loyiha** oching. YouTube API limiti loyihaga bog'liq: bitta loyiha kuniga ~6 ta video yuklay oladi.
- Loyihada **YouTube Data API v3** ni yoqing.
- **OAuth client (Desktop app)** yarating va `client_secret.json` ni yuklab oling.

**4b. Tokenni oling**
```
pip install google-auth-oauthlib google-api-python-client
python auth.py client_secret.json token_doughbros.json
```
- Brauzer ochiladi. Kerakli Google akkaunt va **kerakli kanalni** tanlang.
- Oxirida `OK: Dough Bros (UC...)` chiqishi kerak.

### 5. Tokenni serverga ko'chiring
```
scp token_doughbros.json root@SERVER_IP:/root/kanal/doughbros/token.json
```

### 6. Tekshiring
Tayyor. Server har 20 daqiqada o'zi ishga tushadi. Ishlayotganini ko'rish:
```
tail -f /root/kanal/doughbros/worker.log
```

**Muhim:** parol yoki tokenni hech kimga, Claude'ga ham bermang. Tokenni faqat o'zingiz serverga qo'yasiz.

## Bilib qo'ying
- YouTube API limiti: kuniga 7 ta yuklash (3 long + 4 Shorts) bitta loyihaning standart limitidan biroz oshadi. Shunday bo'lsa, server qolganini ertasi kuni yuklaydi. Doimiy hal qilish uchun Google Cloud'da limitni oshirishni so'rang (bepul so'rov).
- Server o'chib qolsa yoki tokenning muddati o'tsa (`invalid_grant`), kechki tekshiruvda Claude sizga aytadi.
