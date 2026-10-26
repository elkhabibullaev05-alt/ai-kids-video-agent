# Builds scripts3d/ep032.json (run from hollow/)
# True story: Gef the "talking mongoose", Cashen's Gap farmhouse near Dalby, Isle of Man (from 1931).
# Sources: en.wikipedia.org/wiki/Gef ; mentalfloss.com/article/71816 ; encyclopedia.com "Cashen's Gap"
import json
src=json.load(open('scripts3d/ep031.json'))
chars={k:src['chars'][k] for k in ('odo','moth','narr','shepherd')}
chars['shepherd']['home']=[30,30]
chars['jim']={"name":"James Irving","voice":"bm_lewis","speed":0.95,"pitch":-1,"color":[0.35,0.28,0.2],"kind":"human","size":0.85,"home":[3.5,9.5]}
chars['maggie']={"name":"Margaret Irving","voice":"bf_emma","speed":0.95,"pitch":0,"color":[0.3,0.18,0.25],"kind":"human","size":0.8,"home":[-30,30]}
chars['voirrey']={"name":"Voirrey","voice":"bf_isabella","speed":1.0,"pitch":2,"color":[0.45,0.2,0.18],"kind":"human","size":0.65,"home":[-30,32]}
chars['price']={"name":"Harry Price","voice":"bm_george","speed":0.95,"pitch":-2,"color":[0.15,0.15,0.18],"kind":"human","size":0.85,"home":[-30,34]}
chars['mona']={"name":"Mona the sheepdog","voice":"am_onyx","speed":1.0,"pitch":0,"color":[0.75,0.7,0.62],"kind":"gloamhound","size":0.5,"home":[-30,36]}
chars['gef']={"name":"Gef","voice":"af_sky","speed":1.1,"pitch":4}   # never seen: only a voice and two yellow eyes
props=[
 {"type":"box","id":"wall1","color":[0.22,0.15,0.09],"visible":True,"scale":3.4,"at":[-4.2,13.5,0]},
 {"type":"box","id":"wall2","color":[0.2,0.13,0.08],"visible":True,"scale":3.4,"at":[0.0,13.5,0]},
 {"type":"box","id":"wall3","color":[0.22,0.15,0.09],"visible":True,"scale":3.4,"at":[4.2,13.5,0]},
 {"type":"ball","id":"eyes","color":[1.0,0.7,0.0],"glow":5,"visible":True,"scale":0.14,"at":[-0.35,11.3,1.6]},
 {"type":"ball","id":"eyes2","color":[1.0,0.7,0.0],"glow":5,"visible":True,"scale":0.14,"at":[0.35,11.3,1.6]},
 {"type":"ball","id":"saucer","color":[0.85,0.85,0.8],"visible":False,"scale":0.35,"at":[2.0,11.0,3.0]},
 {"type":"box","id":"clay","color":[0.6,0.45,0.3],"visible":False,"scale":0.5,"at":[1.0,8.0,0]},
 {"type":"ball","id":"lamp","color":[1.0,0.7,0.3],"glow":10,"visible":False,"scale":0.4,"at":[-3.0,11.0,2.5]},
]
B=[]
def b(who,say,cam,do=(),sfx=None,text=None):
    x={"who":who,"say":say,"cam":cam,"do":[list(d) for d in do]}
    if sfx:x["sfx"]=sfx
    if text:x["text"]=text
    B.append(x)
b("narr","Something lived inside the walls of this farmhouse. And it could talk.","prop:eyes",[("eyes","bounce"),("eyes2","bounce"),("odo","shake")],"alarm","THE WALL TALKED")
b("gef","Who's there? I can see you! I see everything from in here!","prop:eyes",[("eyes","shake"),("eyes2","shake")],"suspicious","WHO'S THERE?")
b("moth","Odo! The wall has eyes! Yellow eyes!","close:moth",[("moth","jump"),("odo","turn:moth")],"crunch","THE WALL HAS EYES")
b("narr","New episode every day. Subscribe so you don't miss what happens next.","two:odo,moth",[("odo","turn:front"),("moth","turn:front")],None,"SUBSCRIBE")
b("narr","They had run from the Pale Shepherd all night, down the mountain, across the sea.","wide",[("odo","to:-5,7,0"),("moth","to:-3.5,7,0")],"whoosh","RUNNING FROM THE SHEPHERD")
b("odo","A farmhouse. A light in the window. Maybe we can hide here.","close:odo",[("lamp","show"),("odo","turn:front")],None,"A PLACE TO HIDE?")
b("narr","This is a true story, from the records of the Isle of Man.","wide",[("lamp","bounce")],"horn","A TRUE STORY")
b("narr","A lonely farm called Cashen's Gap, near the village of Dalby.","wide",[("jim","to:3.5,9.5,0"),("jim","turn:front")],None,"CASHEN'S GAP, 1931")
b("narr","In nineteen thirty-one, the Irving family lived here. James, Margaret and their daughter Voirrey.","two:jim,maggie",[("maggie","to:5.5,9.8,0"),("voirrey","to:1.8,9.2,0")],None,"THE IRVING FAMILY")
b("jim","At night we hear scratching behind the wooden panels. Then rustling.","close:jim",[("jim","shake")],"crunch","SCRATCHING")
b("maggie","And then... a voice. Coming out of the wall.","close:maggie",[("maggie","eyes_big")],"suspicious","A VOICE")
b("narr","The voice said it was a mongoose. Its name was Gef.","prop:eyes",[("eyes","bounce"),("eyes2","bounce")],"pop","MY NAME IS GEF")
b("gef","I am an extra, extra clever mongoose!","prop:eyes",[("eyes","spin"),("eyes2","spin")],"pop","EXTRA EXTRA CLEVER")
b("narr","Gef said he came from India, and was born in eighteen fifty-two.","prop:eyes",[("eyes","shake"),("eyes2","shake")],None,"BORN IN 1852?")
b("moth","Eighteen fifty-two? Odo, that mongoose is older than my grandma's grandma!","close:moth",[("moth","eyes_big")],None,"80 YEARS OLD?")
b("narr","The family left food for him in a saucer, hanging from the ceiling.","prop:saucer",[("saucer","show"),("saucer","bounce")],"pop","FOOD FOR THE WALL")
b("voirrey","He talks to me most of all. He sleeps in my room, he says.","close:voirrey",[("voirrey","turn:front")],None,"HE TALKS TO HER")
b("narr","Gef said he guarded the house, and warned them of visitors and strange dogs.","wide",[("eyes","bounce"),("eyes2","bounce"),("jim","turn:front")],"suspicious","HE GUARDS THE HOUSE")
b("narr","Many people said they heard the voice. Almost nobody ever saw him.","prop:eyes",[("eyes","vanish"),("eyes2","vanish")],"alarm","NOBODY SAW HIM")
b("odo","The rule, Mothwick: if the wall talks back, don't answer it.","close:odo",[("odo","shake")],"suspicious","DON'T ANSWER THE WALL")
b("moth","Don't answer. Got it. My mouth is already closed. Mostly.","close:moth",[("moth","jump")])
b("narr","Newspapers all over Britain printed the story of the talking mongoose.","wide",[("jim","exit"),("maggie","exit"),("voirrey","exit")],"horn","IT WAS IN THE PAPERS")
b("narr","In July nineteen thirty-five, the famous ghost hunter Harry Price came to see for himself.","close:price",[("price","to:2,9.5,0"),("price","turn:front")],"whoosh","1935: THE GHOST HUNTER")
b("price","I listened for days. Gef did not say one single word.","close:price",[("price","shake")],None,"NOT ONE WORD")
b("narr","Price found that the wooden panels could carry a voice through the whole house.","wide",[("wall1","bounce"),("wall2","bounce"),("wall3","bounce")],"crunch","THE WALLS CARRY SOUND")
b("narr","Hair said to be Gef's was sent to a scientist. It was dog hair.","close:mona",[("mona","to:-1,8.5,0"),("mona","turn:front")],"pop","IT WAS DOG HAIR")
b("price","I believe it came from Mona, the family's sheepdog.","close:price",[("price","turn:mona"),("mona","jump")],None,"THE SHEEPDOG?")
b("narr","Paw prints pressed in clay matched no known animal. And they were not a mongoose.","prop:clay",[("clay","show"),("clay","bounce")],"suspicious","NO KNOWN ANIMAL")
b("odo","So was it a trick? A voice thrown through the wall?","close:odo",[("odo","turn:moth"),("price","exit")],None,"A TRICK?")
b("narr","Some said so. But Voirrey said, until the end of her life, that Gef was real.","close:voirrey",[("voirrey","to:1.5,9,0"),("voirrey","turn:front"),("mona","exit")],"horn","SHE NEVER CHANGED HER STORY")
b("narr","In nineteen forty-five the family left the farm. Nobody has solved the mystery.","wide",[("voirrey","exit"),("lamp","vanish"),("clay","vanish"),("saucer","vanish")],"rumble","NEVER SOLVED")
b("moth","Okay. The family is gone. The house is empty. So why is the wall still scratching?","close:moth",[("moth","shake")],"crunch","STILL SCRATCHING")
b("narr","Two yellow eyes opened in the dark wood again.","prop:eyes",[("eyes","show"),("eyes2","show"),("odo","eyes_big")],"alarm","THE EYES ARE BACK")
b("gef","Psst. Lantern-bearer. Someone tall is standing outside. He asked me where you are.","prop:eyes",[("eyes","shake"),("eyes2","shake")],"suspicious","SOMEONE IS OUTSIDE")
b("odo","Don't answer it, Mothwick. Whatever it says, don't answer.","close:odo",[("odo","shake"),("moth","jump")],None,"DON'T ANSWER")
b("narr","Then the voice changed. It was no longer small, and no longer squeaky.","prop:eyes",[("eyes","bounce"),("eyes2","bounce")],"rumble","THE VOICE CHANGED")
b("shepherd","I told the little one to keep you talking, lantern-bearer. And you did.","close:shepherd",[("shepherd","to:-2,10,0"),("shepherd","turn:front")],"alarm","HE WAS INSIDE")
b("narr","What do you think happens in the next part? Tell me in the comments.","close:odo",[("odo","shake"),("moth","eyes_big")],"horn","WHAT HAPPENS NEXT?")
d={"title":"Ep 32 · 1931: What Was Talking Behind the Wall?",
 "description":"What do you think happens in the next part? Tell me in the comments.",
 "lead_in":0.05,"set":{"place":"village","fog":0.04,"eyes":2,"moonlight":10},
 "chars":chars,"props":props,"beats":B}
json.dump(d,open('scripts3d/ep032.json','w'),indent=1,ensure_ascii=False)
w=sum(len(x['say'].split()) for x in B); print('beats',len(B),'words',w, 'maxline',max(len(x['say'].split()) for x in B))
