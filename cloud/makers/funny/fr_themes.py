"""Funny Rank Daily — themes, titles, reactions.

Only mild slapstick: no injuries, blood, crashes, cruelty, scaring animals or pranks on people.
Each theme: (display name, search query, keywords — at least one must be in a source clip's title).
"""
import datetime as dt
import json
import os
import random
import re

THEMES = [
    ("Puppy Fails", "funny puppy fails", ["puppy", "puppies", "pup"]),
    ("Kitten Fails", "funny kitten fails", ["kitten", "kitty", "kittens"]),
    ("Cat Jump Fails", "cat jump fail funny", ["cat", "cats"]),
    ("Dog Zoomies", "dog zoomies funny", ["zoomies", "dog", "dogs"]),
    ("Trampoline Fails", "trampoline fails funny", ["trampoline"]),
    ("Skateboard Fails", "skateboard fail funny", ["skate", "skateboard", "skater"]),
    ("Gym Fails", "funny gym fails", ["gym", "workout", "exercise"]),
    ("Wedding Fails", "funny wedding fails", ["wedding", "bride", "groom"]),
    ("Snow Fails", "funny snow fails", ["snow", "snowy"]),
    ("Ice Slip Fails", "slipping on ice funny", ["ice", "icy", "slip", "slipping"]),
    ("Goat Moments", "funny goats", ["goat", "goats"]),
    ("Parrot Moments", "funny parrot talking", ["parrot", "parrots", "cockatoo", "macaw"]),
    ("Baby Laughs", "baby laughing funny", ["baby", "babies", "laugh"]),
    ("Pool Fails", "funny pool fails", ["pool", "swimming"]),
    ("Treadmill Fails", "treadmill fail funny", ["treadmill"]),
    ("Bike Fails", "funny bike fails", ["bike", "bicycle", "cycling"]),
    ("Scooter Fails", "scooter fail funny", ["scooter"]),
    ("Roller Skate Fails", "roller skating fail funny", ["roller", "skating", "skates"]),
    ("Ice Skating Fails", "ice skating fails funny", ["skating", "ice rink", "skater"]),
    ("Ski Fails", "funny ski fails", ["ski", "skiing", "skier"]),
    ("Sledding Fails", "sledding fail funny", ["sled", "sledding", "sledge"]),
    ("Surfing Fails", "funny surfing fails", ["surf", "surfing", "surfer"]),
    ("Paddle Board Fails", "paddle board fail funny", ["paddle", "sup", "paddleboard"]),
    ("Kayak Fails", "kayak fail funny", ["kayak", "canoe"]),
    ("Fishing Fails", "funny fishing fails", ["fishing", "fish"]),
    ("Golf Fails", "funny golf fails", ["golf"]),
    ("Basketball Fails", "funny basketball fails", ["basketball", "hoop", "dunk"]),
    ("Soccer Fails", "funny soccer fails", ["soccer", "football", "goal"]),
    ("Bowling Fails", "funny bowling fails", ["bowling"]),
    ("Baseball Bloopers", "funny baseball bloopers", ["baseball"]),
    ("Volleyball Fails", "funny volleyball fails", ["volleyball"]),
    ("Dance Fails", "funny dance fails", ["dance", "dancing"]),
    ("Cooking Fails", "funny cooking fails", ["cooking", "kitchen", "cook"]),
    ("Cake Fails", "cake fail funny", ["cake", "baking"]),
    ("DIY Fails", "funny diy fails", ["diy", "home", "repair"]),
    ("Rope Swing Fails", "rope swing fail funny", ["rope", "swing"]),
    ("Hammock Fails", "hammock fail funny", ["hammock"]),
    ("Water Slide Fails", "water slide fail funny", ["slide", "waterslide"]),
    ("Bounce House Fails", "bounce house funny", ["bounce", "bouncy", "inflatable"]),
    ("Swing Fails", "funny swing fails", ["swing", "swings"]),
    ("Slip N Slide Fails", "slip and slide fail funny", ["slip", "slide"]),
    ("Diving Board Fails", "diving board fail funny", ["diving", "dive", "board"]),
    ("Duck Moments", "funny ducks", ["duck", "ducks", "duckling"]),
    ("Chicken Moments", "funny chickens", ["chicken", "chickens", "hen", "rooster"]),
    ("Cow Moments", "funny cows", ["cow", "cows", "calf"]),
    ("Pig Moments", "funny pigs", ["pig", "pigs", "piglet"]),
    ("Sheep Moments", "funny sheep", ["sheep", "lamb"]),
    ("Hamster Moments", "funny hamster", ["hamster", "hamsters"]),
    ("Bunny Moments", "funny bunny rabbit", ["bunny", "rabbit", "bunnies"]),
    ("Squirrel Moments", "funny squirrel", ["squirrel", "squirrels"]),
    ("Raccoon Moments", "funny raccoon", ["raccoon", "raccoons"]),
    ("Penguin Moments", "funny penguins", ["penguin", "penguins"]),
    ("Husky Moments", "funny husky talking", ["husky", "huskies"]),
    ("Dog Mirror Moments", "dog mirror funny", ["mirror", "dog"]),
    ("Cats In Boxes", "cat box funny", ["box", "cat"]),
    ("Dog Bath Fails", "funny dog bath", ["bath", "dog", "puppy"]),
    ("Robot Vacuum Pets", "cat robot vacuum funny", ["vacuum", "roomba"]),
    ("Selfie Fails", "funny selfie fails", ["selfie"]),
    ("Hoverboard Fails", "hoverboard fail funny", ["hoverboard"]),
    ("Unicycle Fails", "unicycle fail funny", ["unicycle"]),
    ("Pogo Stick Fails", "pogo stick fail funny", ["pogo"]),
    ("Jump Rope Fails", "jump rope fail funny", ["jump rope", "skipping"]),
    ("Yoga Fails", "funny yoga fails", ["yoga"]),
    ("Snowboard Fails", "funny snowboard fails", ["snowboard", "snowboarding"]),
    ("Hockey Bloopers", "funny hockey bloopers", ["hockey"]),
    ("Frisbee Dog Fails", "dog frisbee fail funny", ["frisbee", "disc"]),
    ("Fetch Fails", "dog fetch fail funny", ["fetch", "ball", "dog"]),
    ("Lazy Dog Moments", "lazy dog funny", ["lazy", "dog", "dogs"]),
    ("Sleepy Cat Moments", "sleepy cat funny", ["sleepy", "sleeping", "cat"]),
    ("Dog Sneeze Moments", "dog sneeze funny", ["sneeze", "sneezing"]),
    ("Llama Moments", "funny llama alpaca", ["llama", "alpaca"]),
    ("Owl Moments", "funny owl", ["owl", "owls"]),
    ("Seagull Snack Thefts", "seagull steals food funny", ["seagull", "gull"]),
    ("Dog Costume Moments", "dog costume funny", ["costume", "dog"]),
    ("Mini Horse Moments", "funny mini horse pony", ["horse", "pony"]),
    ("Puppy Stairs Fails", "puppy stairs funny", ["stairs", "puppy", "steps"]),
    ("Pet Door Fails", "pet door fail funny", ["door", "pet", "flap"]),
    ("Mud Fails", "mud fail funny", ["mud", "muddy"]),
    ("Windy Day Fails", "windy day fail funny", ["wind", "windy"]),
    ("Umbrella Fails", "umbrella fail funny", ["umbrella"]),
    ("Balloon Fails", "balloon fail funny", ["balloon", "balloons"]),
    ("Gift Wrapping Fails", "funny christmas present fail", ["gift", "present", "wrapping"]),
    ("Christmas Tree Cats", "cat christmas tree funny", ["christmas", "tree", "cat"]),
    ("Pumpkin Carving Fails", "pumpkin carving fail funny", ["pumpkin"]),
    ("Snowman Fails", "snowman fail funny", ["snowman"]),
    ("Car Wash Pets", "dog car wash funny", ["car wash", "dog"]),
    ("Beach Fails", "funny beach fails", ["beach", "sand", "waves"]),
    ("Camping Fails", "funny camping fails", ["camping", "tent"]),
    ("Boat Fails", "funny boat fails", ["boat", "dock"]),
    ("Horse Moments", "funny horse", ["horse", "horses"]),
    ("Toddler Dance Moments", "toddler dancing funny", ["toddler", "dance", "dancing", "kid"]),
    ("Magic Trick Fails", "magic trick fail funny", ["magic", "trick"]),
    ("Talking Dog Moments", "talking dog funny", ["talking", "dog", "howl"]),
    ("Cat Vs Dog Moments", "cat vs dog funny", ["cat", "dog"]),
    ("Zipline Fails", "zipline fail funny", ["zipline", "zip line"]),
    ("Bowling Ball Bloopers", "bowling blooper funny", ["bowling"]),
    ("Piano Cat Moments", "cat playing piano funny", ["piano", "cat"]),
]

FUNNY_WORDS = ["fail", "fails", "funny", "funniest", "lol", "oops", "epic", "hilarious", "laugh", "laughing",
               "comedy", "blooper", "bloopers", "silly", "derp", "clumsy", "goofy", "cute", "crazy", "moment",
               "moments", "try not to", "compilation", "zoomies", "talking", "dramatic"]

# words that make a clip unusable (harm, cruelty, scary, not a funny clip)
BAD_WORDS = ["injur", "hurt", "blood", "hospital", "accident", "crash", "died", "death", "dead", "kill", "fight",
             "abuse", "cruel", "attack", "bite", "bitten", "broken", "ambulance", "war", "gun", "shoot", "scary",
             "horror", "nsfw", "sexy", "bikini", "tutorial", "how to", "review", "unboxing", "asmr", "podcast",
             "news", "reaction", "reacts", "prank", "pranks", "scare", "scared", "vomit", "puke", "drunk", "weed", "fire",
             "burn", "knife", "police", "cop", "arrest", "explosion", "explode", "tragic", "rip", "funeral",
             "cucumber", "1 hour", "livestream", "live stream", "trailer", "music video", "lyrics", "slaughter",
             "hunting", "rescue", "sick", "vet", "surgery", "storm", "flood", "tornado", "earthquake"]

BAD_PREFIX = {"injur", "explo", "crash", "burn", "kill", "attack", "bit", "scar"}

TITLE_PATTERNS = [
    "Ranking {n} (Wait for #1) 💀",
    "Ranking {n} (Wait for #1) 😂",
    "Ranking The FUNNIEST {n} 😂",
    "Ranking Best {n} (#1 is Wild) 💀",
    "Ranking Crazy {n} 😂",
    "Ranking {n} From Bad to WORST 💀",
    "Ranking Top 5 {n} 😂",
    "Ranking The Silliest {n} 🤯",
]

# (on-screen tag for the 1-5 list, spoken + caption reaction)
REACTIONS = {
    5: [("WARM UP", "Okay, a gentle start."), ("ROUGH START", "That's a rough start."),
        ("CLASSIC", "A classic, but we're just warming up."), ("NOT BAD", "Not bad for number five."),
        ("SO CLOSE", "So close, and yet so far.")],
    4: [("BIG OOPS", "Oops, that did not go to plan."), ("NOPE", "Nope. Not today."),
        ("WOBBLY", "Look at that wobble!"), ("PLOT TWIST", "Did not see that coming."),
        ("CONFIDENT", "So confident. So wrong.")],
    3: [("NO WAY", "No way that just happened."), ("CHAOS", "Pure chaos."),
        ("THE FACE", "Look at the face after!"), ("BAD IDEA", "Somebody knew it was a bad idea."),
        ("TIMING", "The timing is perfect.")],
    2: [("TOTAL CHAOS", "This one almost took the top spot."), ("UNREAL", "How is this only number two?"),
        ("LEGEND", "Absolute legend behavior."), ("WAIT WHAT", "Wait, what just happened?"),
        ("REPLAY IT", "I had to watch this five times.")],
    1: [("LEGENDARY", "Absolutely legendary."), ("CHAMPION", "And the champion is..."),
        ("THE KING", "Nothing beats this one."), ("GOLD", "Pure gold. Number one."),
        ("UNBEATABLE", "Unbeatable. Watch it again.")],
}
NUM_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
# 2026-11-14 owner (Ask Studio): frame 1 = the shock moment + a QUESTION, no "Top 5" countdown screen
HOOKS = ["Can you spot the mistake before it happens?", "Wait for number one!", "Guess what goes wrong!",
         "This was a terrible idea."]
HOOK_TEXT = {"Can you spot the mistake before it happens?": "SPOT THE MISTAKE?", "Wait for number one!": "WAIT FOR #1",
             "Guess what goes wrong!": "WHAT GOES WRONG?", "This was a terrible idea.": "TERRIBLE IDEA..."}
PHYSICS_HOOKS = ["Why did this fail? Physics explains.", "Can you guess the physics before it fails?",
                 "Which law of physics wins here?"]
PHYSICS_HOOK_TEXT = {"Why did this fail? Physics explains.": "WHY DID IT FAIL?",
                     "Can you guess the physics before it fails?": "GUESS THE PHYSICS",
                     "Which law of physics wins here?": "WHICH LAW WINS?"}
PHYSICS_END = [("WHICH LAW?", "Which law won? Comment!"), ("YOUR #1?", "What's your number one? Comment!")]

# 2026-11-14 owner: every clip gets our OWN spoken commentary (predict what happens + funny reaction + the cause),
# not just "Number five!" — clips without original commentary count as reused content. Short lines (<= ~7 words)
# keep the Short at 15-22 s.
COMMENT_PREDICT = ["Watch the back foot.", "Way too confident.", "Look at that speed.", "Wait for the landing.",
                   "This will not end well.", "Spot the mistake?", "Here it comes.", "He has no plan.",
                   "Nobody checked the ground.", "Too much speed. Watch."]
COMMENT_REACT = ["Gravity always wins.", "Zero grip, full send.", "The landing had other plans.",
                 "Momentum said no.", "Instant regret.", "That face says everything.", "Physics did not agree.",
                 "Full speed, no brakes.", "He trusted that? Brave."]
PHYSICS_PREDICT = ["Watch the center of gravity.", "Speed in, zero friction.", "Look where the weight is.",
                   "Watch the pivot point.", "Too much speed. Watch.", "Wet surface. Here it goes."]
PHYSICS_CAUSE = ["Inertia: the body keeps going.", "Weight past the base. Over.", "Low friction. Feet gone.",
                 "Momentum beats balance.", "Equal and opposite reaction.", "Gravity pulls, nothing pushes back.",
                 "Torque wins. Down it goes.", "Speed doubled, impact quadrupled.", "No grip, no stop."]
END_LINES = [("#1 OR #2?", "Number one or two? Comment!"), ("AGREE?", "Do you agree? Comment!"),
             ("YOUR #1?", "What's your number one? Comment!")]


# 2026-11-14 owner (Ask Studio): animal clips (parrot, goat, horse) kept only 19-29 % of viewers, dynamic risky
# action (trampoline, water slide, boat/car, extreme sport, DIY) kept 58-60 % -> no animal themes from now on.
ANIMAL_WORDS = ["puppy", "kitten", "cat", "dog", "goat", "parrot", "duck", "chicken", "cow", "pig", "sheep",
                "hamster", "bunny", "squirrel", "raccoon", "penguin", "husky", "llama", "owl", "seagull", "horse",
                "pet", "baby", "toddler"]
THEMES = [t for t in THEMES if not any(re.search(r"\b" + a + r"s?\b", t[0].lower()) for a in ANIMAL_WORDS)]
THEMES += [
    ("Jet Ski Fails", "jet ski fail funny", ["jet ski", "jetski", "waverunner"]),
    ("Boat Launch Fails", "boat ramp launch fail funny", ["boat", "ramp", "launch", "trailer"]),
    ("Wakeboard Fails", "wakeboard fail funny", ["wakeboard", "wakeboarding"]),
    ("BMX Fails", "bmx fail funny", ["bmx"]),
    ("Parkour Fails", "parkour fail funny", ["parkour", "freerunning"]),
    ("Dirt Bike Fails", "dirt bike fail funny", ["dirt bike", "dirtbike", "motocross"]),
    ("Car Stuck Fails", "car stuck mud snow fail funny", ["car", "truck", "stuck"]),
    ("Ladder Fails", "ladder fail funny diy", ["ladder"]),
    ("Tubing Fails", "tubing fail funny", ["tubing", "tube"]),
    ("Cliff Jump Fails", "cliff jumping fail funny", ["cliff", "jump", "jumping"]),
]

# 2026-11-13 owner: the "Money Story" channel becomes a ranked funny-PHYSICS channel (same engine, own theme list)
PHYSICS_THEMES = [
    ("Physics Fails", "physics fail funny", ["physics", "fail"]),
    ("Gravity Fails", "gravity fail funny", ["gravity", "fall", "drop"]),
    ("Balance Fails", "balance fail funny", ["balance", "balancing"]),
    ("Slingshot Fails", "slingshot fail funny", ["slingshot"]),
    ("Catapult Fails", "catapult fail funny", ["catapult", "trebuchet"]),
    ("Seesaw Fails", "seesaw fail funny", ["seesaw", "see-saw"]),
    ("Ramp Jump Fails", "ramp jump fail funny", ["ramp", "jump"]),
    ("Science Experiment Fails", "science experiment fail funny", ["experiment", "science"]),
    # 2026-11-14 owner: dynamic topics only (falls, jumps, cars, water); calm experiments (magnets, pendulum,
    # dominoes, egg drop) dropped
    ("Slip And Fall Physics", "slip and fall fail funny", ["slip", "slipping", "fall"]),
    ("Water Splash Fails", "water splash fail funny", ["water", "splash", "lake", "river"]),
    ("Bike Jump Fails", "bike jump fail funny", ["bike", "jump"]),
    ("RC Car Jump Fails", "rc car jump fail", ["rc", "car", "jump"]),
    ("Car Mud Fails", "car stuck in mud fail", ["car", "truck", "mud"]),
    ("Rope Swing Physics", "rope swing fail funny", ["rope", "swing"]),
    ("Dock Jump Fails", "dock jump fail funny", ["dock", "jump", "lake"]),
    ("Ski Jump Fails", "ski jump fail funny", ["ski", "jump"]),
]
if os.environ.get("FR_THEMES") == "physics":
    THEMES = PHYSICS_THEMES

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^\w#\s]", " ", (t or "").lower())).strip()


def load_hist(home):
    p = os.path.join(home, "funny_themes.json")
    try:
        return json.load(open(p))
    except Exception:
        return {}


def save_hist(home, hist):
    p = os.path.join(home, "funny_themes.json")
    json.dump(hist, open(p + ".tmp", "w"), indent=1)
    os.replace(p + ".tmp", p)


def pick_themes(titles, home, n, rng=random, skip=()):
    """Themes not in the last ~30 titles and not used in the last 12 days (oldest-used first)."""
    recent = " | ".join(_norm(t) for t in titles[:30] + titles[-30:])
    hist = load_hist(home)
    cut = (dt.date.today() - dt.timedelta(days=12)).isoformat()
    ok = [t for t in THEMES if _norm(t[0]) not in recent and hist.get(t[0], "") < cut and t[0] not in skip]
    rng.shuffle(ok)
    ok.sort(key=lambda t: hist.get(t[0], ""))  # never-used first, shuffle within ties
    if len(ok) < n:  # almost everything used lately → add least recently used themes not in recent titles first
        rest = [t for t in THEMES if t not in ok and t[0] not in skip]
        rest.sort(key=lambda t: (_norm(t[0]) in recent, hist.get(t[0], "")))
        ok += rest
    return ok


# 2026-11-07 competitors (fail channels at 250k-1M views/week): the title names the OUTCOME/feeling, not "Ranking …".
# Only for "… Fails" themes (the video is a ranked top 5 of fails, so these deliver). Tried before TITLE_PATTERNS.
FAIL_PATTERNS = [
    "{n} That Went Horribly Wrong 💀",
    "Instant Regret: Top 5 {n} 😂",
    "{n} Ranked From Bad to WORST 💀",
    "Top 5 {n}… #1 Hurts 💀",
    # 2026-11-08 competitors: situation/feeling titles ("HE THOUGHT NO ONE WAS WATCHING 😭" 268k/2 d)
    "{n} Nobody Saw Coming 😭",
    "Worst Day Ever? {n} 💀",
]


def make_title(name, titles, rng=random):
    used = {_norm(t) for t in titles}
    pats = TITLE_PATTERNS[:]
    rng.shuffle(pats)
    if name.lower().endswith(" fails"):
        fp = FAIL_PATTERNS[:]
        rng.shuffle(fp)
        pats = fp[:2] + pats
    # 2026-11-13 review: "X Fails That Went Horribly Wrong 💀" 4x in two days → least-used template among recent titles first
    recent = [_norm(t) for t in titles[:12] + titles[-12:]]

    def _uses(p):
        a, _, b = p.partition("{n}")
        a, b = _norm(a), _norm(b)
        return sum(1 for t in recent if (not a or t.startswith(a)) and (not b or t.endswith(b)))
    pats.sort(key=_uses)
    for p in pats:
        t = p.format(n=name)
        if len(t) <= 50 and _norm(t) not in used:
            return t
    for p in pats:  # all patterns used for this name (rare) → add "Part N"
        for k in range(2, 30):
            t = p.format(n=f"{name} {k}")
            if len(t) <= 55 and _norm(t) not in used:
                return t
    return f"Ranking {name} #{rng.randint(100, 999)} 😂"


def script(rng=random):
    physics = os.environ.get("FR_THEMES") == "physics"
    hook = rng.choice(PHYSICS_HOOKS if physics else HOOKS)
    hook_text = (PHYSICS_HOOK_TEXT if physics else HOOK_TEXT)[hook]
    end = rng.choice(PHYSICS_END if physics else END_LINES)
    pred = rng.sample(PHYSICS_PREDICT if physics else COMMENT_PREDICT, 3)
    cause = rng.sample(PHYSICS_CAUSE if physics else COMMENT_REACT, 2)
    ranks = {}
    for r in range(5, 0, -1):
        tag, _ = rng.choice(REACTIONS[r])
        # 2026-11-14 owner: own commentary on every clip — #5-#3 predict what is coming, #2/#1 react + say why
        line = pred[5 - r] if r >= 3 else cause[2 - r]
        num = NUM_WORDS[r].capitalize() if r > 1 else "Number one"
        ranks[r] = {"tag": tag, "line": line, "say": f"{num}. {line}"}
    return {"hook": hook, "hook_text": hook_text, "end_text": end[0], "end_say": end[1], "ranks": ranks}


def clip_ok(title, desc, kws):
    t = " " + (title or "").lower() + " "
    if any(re.search(r"\b" + re.escape(b) + ("" if b in BAD_PREFIX else r"s?\b"), t) for b in BAD_WORDS):
        return False
    if not any(k in t for k in kws):
        return False
    return any(w in t or w in (desc or "").lower()[:300] for w in FUNNY_WORDS)
