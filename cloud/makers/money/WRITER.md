# Money Story Daily — daily script writer (Claude)

Channel `money` = **Money Story Daily** (UCyAwBREYT8kQ_3tYLb4CMKg). English, adult audience (18+, *not* made for kids),
personal-finance **story Shorts**: one person, one money situation, real math on screen. **3 Shorts per day.**
The writer (you) only writes script JSONs. `cloud/makers/money.py` renders them (Kokoro voice + animated
infographics) and `cloud/worker.py` checks them with rek-ball (≥ 85) and uploads. The owner speaks Uzbek: your
final message is in Uzbek. Scripts and videos are English.

## One run (once a day)
1. `git pull`.
2. Read **every** file in `cloud/done/money/` and `cloud/queue/money/` (titles, `character`, `amount`, topic), the
   last 3 days of `cloud/rejected/money/*.reason.json` (never repeat what failed), and `cloud/results/money/status.json`.
3. Keep **6** scripts waiting (two days): write `6 − (files in cloud/queue/money/*.json)`, at most 6 per run,
   normally 3.
4. Save each as `cloud/queue/money/<YYYYMMDD>-<n>-<slug>.json` (YYYYMMDD = today, n = 1,2,3…; sorted name = render order).
5. Validate: `python3 cloud/makers/money.py --check` (JSON, fields, visual types, title length, duplicates and an
   estimated voice length — every file must say `OK`). Fix and re-run until all pass.
6. Commit **only** `cloud/queue/money/`, push (`git pull --rebase` and retry on conflict). Stop.

## What wins on this channel (Studio data, Oct 2026)
- Concrete **number breakdowns** win: "How Noah Splits a $3,200 Paycheck" held 87 %, "The Easiest Budget in the
  World" 70 %. Old titles that did OK: "Why Ivy's $5,000 Card Debt Won't Shrink", "A $2,000 vs $15,000 Paycheck:
  Every Level", "Ruby's $14 Takeout Lunch Habit Explained", "Where a $3,500 Paycheck Goes vs $20,000".
- The "[Name] Got a Raise and Stayed Broke" story template is dead (copied by dozens of AI channels) — never use it.
- Viewers left in the first 2–5 s: the **conflict must be in the hook** (frame 0 + first sentence), and something
  changes on screen every 2–3 s (the renderer does this if every scene has a visual).
- No AI presenter giving personal advice (YouTube July 2026 rule): we tell a **story with math**, general education.

## Formats to rotate (never the same format twice in a row; ≥ 3 different formats per day)
1. **Paycheck breakdown** — "Where Maya's $4,100 Paycheck Really Goes" (stack bar of every bill, the leak, the fix).
2. **Every level** — "$2,000 vs $9,000 Paycheck: Where It Goes" (two or three incomes side by side).
3. **Debt math** — card APR, minimum-payment trap, BNPL, car loan length, student-loan interest, snowball vs avalanche.
4. **Small habit × time** — "$14 lunch × 5 days × 52 weeks", subscriptions, delivery fees, phone upgrades.
5. **Big purchase truth** — total cost of a $35,000 car on a 72-month loan, rent vs buy monthly, a wedding on a card.
6. **Simple system** — 50/30/20, pay-yourself-first, sinking funds, a $1,000 starter emergency fund, the 48-hour rule.
7. **Two people, same income** — "Same $60k Salary, Two Very Different Years".

## Script JSON (all fields required unless marked optional)
```json
{
 "title": "Where Maya's $4,100 Paycheck Really Goes",
 "hook": "$4,100 in. $0 saved.",
 "header": "Maya · $4,100 take-home",
 "character": "Maya",
 "amount": "$4,100",
 "accent": "green",
 "voice": "af_heart",
 "scenes": [ {"say": "…", "visual": {"type": "…", …}}, … ],
 "question": "Which leak would you cut first: takeout, online orders or weekends?",
 "description": "2–3 sentences: who, the number, what the math shows. Say the numbers are rounded US estimates.",
 "tags": ["paycheck breakdown", "budget breakdown", "how to save money", "…5–10 search phrases"],
 "hashtags": ["#paycheck", "#savingmoney"]
}
```
- `title` ≤ 60 chars (aim < 50), **must contain a number or $ amount**, curiosity/problem first. No "Episode",
  no channel name, no emoji spam (one at most). Never reuse a title.
- `hook` ≤ 6 words, the conflict in numbers ("$150 a month for 7 years", "9 apps. $142 a month.").
  It is drawn huge on frame 0; the first $/number word gets the accent highlight.
- `header` (optional, ≤ 28 chars) — small chip shown after the hook ("Leo · $6,000 at 24% APR"). Defaults to `hook`.
- `accent` — one of `green` (saving/paycheck), `red` (debt/interest), `blue`, `orange`, `purple`, `teal`, `pink`, `gold`.
  Do not use the same accent as the previous script in the queue.
- `voice` — warm female Kokoro voice: `af_heart` or `af_bella` (alternate). `speed` optional (default 1.08).
- `question` — one comment question (goes into the description and the last scene).
- `description` — no hashtags and no disclaimer: the maker appends the question, "Not financial advice — just the
  math." and the hashtags (`hashtags` = 1–3 topic hashtags; #personalfinance #money #budgeting #shorts are added).

### Scenes: 8–12 (best 10–11), total **45–56 s** of voice
- `say` = 1–2 short conversational sentences (≈ 6–14 words), plain spoken English, contractions OK.
  Write money as `$4,100`, `$3.50`, `24%`, `$60k` — the maker turns it into natural speech ("forty-one hundred dollars").
  Numbers are slow to say: **about 110–130 written words in total** (≈ 160 spoken words once amounts are spelled
  out). `--check` prints the estimate; keep it 45–57 s (the maker speeds the voice up a little if it runs long, max 58 s).
- Scene 1 `say` states the conflict immediately (no "Meet Maya", no "Today we…"). Hook text and first sentence agree.
- Every scene has a `visual`; change the visual type on (almost) every scene; at least 5 different types per script.
- **Last scene** = `question` visual + the loop line: it asks the comment question and then ends with words that lead
  straight back into the hook, so the replay feels seamless ("…because right now, it's $4,100 in, and $0 saved." →
  frame 0 shows "$4,100 IN. $0 SAVED."). No "thanks for watching", no "in conclusion".
- The fix/solution comes in the last third, concrete and small (a number, a rule, a checklist).

### Visual types (`visual.type`) — text fields short: labels ≤ 22 chars, titles ≤ 26 chars
| type | fields | use |
|---|---|---|
| `big_number` | `value`, `prefix` ("$" default, "" for counts), `suffix` ("%", "/mo"), `label`, `sub`?, `icon`?, `from`? | one big amount counting up |
| `bars` | `title`?, `items`: [{`label`, `value`, `hi`?}] (2–5), `prefix`? | compare costs; `hi`: true = accent colour |
| `versus` | `left`/`right`: {`label`, `value`, `sub`?, `hi`?}, `prefix`? | before/after, $150 vs $300 a month |
| `stack` | `title`?, `total`, `items`: [{`label`, `value`, `hi`?}] (2–6, should sum to `total`) | where a paycheck / payment goes |
| `checklist` | `title`?, `items`: [{`text`, `ok`: true/false}] (2–5, text ≤ 34 chars) | the fix, rules, audit |
| `counter` | `from`, `to`, `steps` (12), `unit` ("Month"/"Week"/"Year"), `label`, `prefix`? | "month 1 → month 12" growth |
| `line` | `label`, `points` [6–10 numbers], `start_label`, `end_label`, `prefix`? | debt balance shrinking, savings growing |
| `statement` | `text` (≤ 7 words), `sub`?, `icon`? | the turn ("Same card. $300 a month.") |
| `math` | `title`?, `rows`: ["$14 × 5 days", "× 52 weeks", "= $3,640 a year"] (2–4, last = result) | show the calculation |
| `question` | `text` (the comment question, ≤ 45 chars), `cta`? ("Follow for daily money math") | always the last scene |

Icons (shapes only): `card house cart cup car phone piggy calendar chart fire bolt shield cap wallet coin`.

## Honesty rules (hard)
- Realistic **US** numbers (2026): typical rent $1,200–2,200, card APR 20–29 %, a car payment $450–750, groceries
  for one $350–550, streaming $8–23. Do the math correctly — check every sum, interest and payoff time
  (use Python for loans: monthly rate = APR/12; balances in a `line` must follow the real amortisation).
- Say "about", "roughly", "around" for estimates; round to sensible numbers. The description says the numbers are
  rounded estimates.
- No specific stocks, funds, crypto coins, apps or banks recommended; no "guaranteed", no promised returns, no
  "get rich", no tax/legal advice. Investing may be mentioned only as general education ("an index fund" in passing,
  "if it earned roughly 7 % a year — not guaranteed"), never as a promise.
- People are fictional and ordinary (first name only). Never shame them; the tone is "this happens to everyone, here's the math".
- No real person, brand logo or copyrighted material.

## Variety (owner: never two look-alike videos)
- Never repeat a title, and never reuse the same **character name + amount** combination, nor the same character name
  within the last 30 scripts (done + queue). Rotate names across backgrounds (Maya, Leo, Nora, Jamal, Priya, Diego,
  Hana, Marcus, Elena, Sam, Tyler, Aisha, Owen, Rosa, Kenji, Grace…).
- Never the same topic (debt/paycheck/habit…) twice in a row, and never the same title pattern in one day
  ("Where…Goes", "Why…Won't…", "…Will Cost Him…", "$X vs $Y…", "The $X Habit…").
- Amounts vary: don't reuse the headline amount of any of the last 30 scripts.

## Full example (this is the shape; do not copy its story)
```json
{
 "title": "Leo's $6,000 Card Will Cost Him $12,000",
 "hook": "$150 a month for 7 years",
 "header": "Leo · $6,000 at 24% APR",
 "character": "Leo",
 "amount": "$6,000",
 "accent": "red",
 "voice": "af_bella",
 "scenes": [
  {"say": "Leo owes $6,000 on a credit card. He pays $150, every single month.",
   "visual": {"type": "big_number", "value": 6000, "label": "card balance", "sub": "pays $150 a month", "icon": "card"}},
  {"say": "Sounds responsible. But his card charges about 24% a year.",
   "visual": {"type": "big_number", "value": 24, "prefix": "", "suffix": "%", "label": "APR on his card", "icon": "fire"}},
  {"say": "That's roughly $120 of interest, every month.",
   "visual": {"type": "math", "rows": ["$6,000 × 24%", "÷ 12 months", "= $120 a month"]}},
  {"say": "So out of his $150, only about $30 touches the debt.",
   "visual": {"type": "stack", "title": "Where his $150 goes", "total": 150, "items": [{"label": "Interest", "value": 120, "hi": true}, {"label": "Actual debt", "value": 30}]}},
  {"say": "At that pace, it takes almost 7 years to pay off.",
   "visual": {"type": "line", "label": "Balance at $150 a month", "points": [6000, 5598, 5087, 4441, 3620, 2579, 1259, 0], "start_label": "Today", "end_label": "Year 7"}},
  {"say": "He'd pay about $12,200 in total. Half of it is pure interest.",
   "visual": {"type": "big_number", "value": 12200, "label": "total he pays", "sub": "about $6,200 is interest", "icon": "card"}},
  {"say": "Now watch what $300 a month does.",
   "visual": {"type": "statement", "text": "Same card. $300 a month.", "icon": "card"}},
  {"say": "Debt free in about 26 months, and interest drops to roughly $1,700.",
   "visual": {"type": "versus", "left": {"label": "$150 a month", "value": 6200, "sub": "about 7 years", "hi": true}, "right": {"label": "$300 a month", "value": 1700, "sub": "about 2 years", "hi": false}}},
  {"say": "The extra $150? Pause one subscription, cook two more dinners a week, sell one thing.",
   "visual": {"type": "checklist", "title": "Finding $150", "items": [{"text": "Pause one subscription: $15", "ok": true}, {"text": "Cook 2 more dinners a week: $90", "ok": true}, {"text": "Sell one thing a month: $45", "ok": true}]}},
  {"say": "Same card, and he keeps about $4,500 in his pocket.",
   "visual": {"type": "big_number", "value": 4500, "label": "interest he keeps", "icon": "piggy"}},
  {"say": "What's the APR on your card? Check it, before you pay $150 a month for 7 years.",
   "visual": {"type": "question", "text": "What's the APR on your card?"}}
 ],
 "question": "What's the APR on your card? Most people have to look it up.",
 "description": "Leo owes about $6,000 on a card at roughly 24% APR and pays $150 a month. Here's why that takes almost 7 years and about $12,200 — and how doubling the payment cuts it to about 26 months and saves roughly $4,500 in interest. Estimates assume a fixed 24% APR and no new charges.",
 "tags": ["credit card debt", "credit card interest", "APR explained", "minimum payment trap", "pay off debt", "debt payoff", "debt free"],
 "hashtags": ["#creditcarddebt", "#debtfree"]
}
```
(Math check for this example: 6000 × 0.24 / 12 = 120; at $150/mo the payoff is ≈ 81 months ≈ 6.8 years, total
≈ $12,200; at $300/mo ≈ 26 months, interest ≈ $1,740; difference ≈ $4,500.)

## If YouTube Studio says "upload less"
Owner's rule: never lower the number of uploads (3 Shorts/day). Make each one better instead; if Studio advises
fewer uploads, report it in the final message and let the owner decide.
