# Builds scripts3d/ep033.json (run from hollow/)
# True legend: the Moddey Dhoo (Manx "black dog") of Peel Castle, St Patrick's Isle, Isle of Man.
# Written down by George Waldron (A Description of the Isle of Man, published 1731); Waldron dates the keys night to about 1650.
# Sources: en.wikipedia.org/wiki/Moddey_Dhoo ; isle-of-man.com/manxnotebook/fulltext/ma1863/ch04.htm ; isle-of-man.com/manxnotebook/fulltext/sm1911/p129.htm
# The soldier's death in the record is left out: we only say he never spoke of it.
import json
src=json.load(open('scripts3d/ep032.json'))
chars={k:src['chars'][k] for k in ('odo','moth','narr','shepherd')}
chars['shepherd']['home']=[30,30]
chars['dog']={"name":"Moddey Dhoo","voice":"am_onyx","speed":0.8,"pitch":-5,"color":[0.02,0.02,0.02],"kind":"gloamhound","size":0.8,"home":[3.0,10.0]}
chars['guard1']={"name":"Old Guard","voice":"bm_lewis","speed":0.95,"pitch":-1,"color":[0.3,0.12,0.1],"kind":"human","size":0.85,"home":[-30,30]}
chars['guard2']={"name":"Young Guard","voice":"am_michael","speed":1.0,"pitch":1,"color":[0.15,0.2,0.32],"kind":"human","size":0.8,"home":[-30,32]}
chars['boaster']={"name":"The Boasting Soldier","voice":"am_adam","speed":1.05,"pitch":0,"color":[0.4,0.3,0.1],"kind":"human","size":0.85,"home":[-30,34]}
chars['wren']={"name":"Wren","voice":"af_sky","speed":0.95,"pitch":3}   # voice only, never seen
props=[
 {"type":"ball","id":"fire","color":[1.0,0.45,0.1],"glow":12,"visible":True,"scale":0.6,"at":[1.5,9.0,0.4]},
 {"type":"ball","id":"candle1","color":[1.0,0.8,0.4],"glow":8,"visible":False,"scale":0.12,"at":[-1.2,10.5,1.6]},
 {"type":"ball","id":"candle2","color":[1.0,0.8,0.4],"glow":8,"visible":False,"scale":0.12,"at":[4.0,10.5,1.6]},
 {"type":"box","id":"wallL","color":[0.2,0.2,0.22],"visible":True,"scale":3.2,"at":[-5.0,14.0,0]},
 {"type":"box","id":"wallR","color":[0.2,0.2,0.22],"visible":True,"scale":3.2,"at":[5.5,14.0,0]},
 {"type":"box","id":"seal","color":[0.3,0.3,0.32],"visible":False,"scale":2.2,"at":[0.3,14.5,0]},
 {"type":"ball","id":"keys","color":[0.95,0.8,0.3],"glow":3,"visible":False,"scale":0.18,"at":[-1.0,8.0,1.2]},
 {"type":"ball","id":"pdark","color":[0.9,0.1,0.05],"glow":6,"visible":False,"scale":0.1,"at":[0.3,13.0,1.2]},
]
B=[]
def b(who,say,cam,do=(),sfx=None,text=None):
    x={"who":who,"say":say,"cam":cam,"do":[list(d) for d in do]}
    if sfx:x["sfx"]=sfx
    if text:x["text"]=text
    B.append(x)
# 0 s: in motion, hook text, the question
b("narr","A black dog lies by the fire. Nobody dares pass it alone.","close:dog",[("dog","to:1,8.5,0"),("dog","turn:front"),("odo","shake")],"alarm","DON'T GO ALONE")
b("moth","Odo, stop! Its eyes are open. It's watching us!","close:moth",[("moth","jump"),("odo","to:-4,7,0")],"crunch","IT'S WATCHING")
b("narr","New episode every day. Subscribe so you don't miss what happens next.","two:odo,moth",[("odo","turn:front"),("moth","turn:front")],None,"SUBSCRIBE")
# consequence of Ep 32
b("narr","Last night the Pale Shepherd found them at the farmhouse.","wide",[("odo","to:-6,7,0"),("moth","to:-4.5,7,0")],"whoosh","HE FOUND THEM")
b("odo","We ran all the way to the sea. He didn't even hurry.","close:odo",[("odo","shake")],None,"HE NEVER HURRIES")
b("moth","A castle on a rock in the water! Stone walls. Odo, stone walls!","wide",[("moth","jump"),("candle1","show"),("candle2","show")],"pop","A CASTLE ON A ROCK")
b("narr","A real legend, written down in seventeen thirty-one, on the Isle of Man.","wide",[("candle1","bounce"),("candle2","bounce")],"horn","A REAL LEGEND")
b("narr","Peel Castle stands on a little island called Saint Patrick's Isle.","wide",[("guard1","to:3.5,9.5,0"),("guard1","turn:front")],None,"PEEL CASTLE")
b("narr","George Waldron wrote down what the soldiers who guarded it believed.","two:guard1,guard2",[("guard2","to:5.5,9.8,0"),("guard2","turn:front")],None,"WHAT THE SOLDIERS SAID")
b("guard1","Every evening, when we light the candles, it comes in.","close:guard1",[("candle1","bounce"),("candle2","bounce")],"suspicious","WHEN THE CANDLES ARE LIT")
b("narr","A big black dog, like a spaniel, with curly, shaggy hair.","close:dog",[("dog","turn:front"),("dog","bounce")],"rumble","THE BLACK DOG")
b("guard2","It walks into the guard room and lies down in front of the fire.","close:guard2",[("dog","to:1.5,8.0,0"),("fire","bounce")],None,"IT LIES BY THE FIRE")
b("narr","In Manx they called it the Moddey Dhoo. The black dog.","close:dog",[("dog","shake")],"pop","MODDEY DHOO")
b("moth","It's lying in our spot. By our fire. Should I ask it to move?","close:moth",[("moth","eyes_big"),("odo","turn:moth")],None,"OUR FIRE")
b("narr","It came out of a dark passage at dusk. At dawn, it went back.","prop:pdark",[("pdark","show"),("pdark","bounce")],"suspicious","FROM THE PASSAGE")
b("narr","At first the soldiers were terrified. Slowly, they got used to it.","two:guard1,guard2",[("guard1","turn:guard2"),("guard2","turn:guard1")],None,"THEY GOT USED TO IT")
b("guard1","But we never swear when it's here. And we are never alone with it.","close:guard1",[("guard1","shake")],"alarm","NEVER ALONE")
b("odo","Mothwick. The rule here: never walk the dark passage alone.","close:odo",[("odo","shake")],"suspicious","NEVER WALK IT ALONE")
b("moth","Alone? I'm not even walking it with you!","close:moth",[("moth","jump")],None)
b("narr","Each night the gates were locked, and the keys carried to the captain.","prop:keys",[("keys","show"),("keys","spin")],"pop","THE KEYS")
b("narr","The way went through the old church. Through that passage.","prop:pdark",[("keys","bounce"),("pdark","bounce")],"whoosh","THROUGH THE PASSAGE")
b("guard2","So we always carried the keys in twos. Never one man alone.","close:guard2",[("guard2","turn:front")],None,"ALWAYS IN TWOS")
b("narr","Then, Waldron says around sixteen fifty, one soldier had too much to drink.","close:boaster",[("boaster","to:-1,8.5,0"),("boaster","turn:front")],"horn","ONE NIGHT")
b("boaster","Give me the keys! I'll go alone. I'll see if it's a dog or a devil!","close:boaster",[("boaster","jump"),("keys","bounce")],"alarm","I'LL GO ALONE")
b("guard1","Don't do it, lad. Not alone. Nobody goes alone.","close:guard1",[("guard1","shake")],None,"DON'T DO IT")
b("narr","He took the keys into the passage. The dog got up and followed.","prop:pdark",[("boaster","to:0.3,13,0"),("dog","to:0.5,12,0"),("keys","vanish")],"rumble","IT FOLLOWED HIM")
b("narr","Soon the guards heard a terrible noise. Nobody dared look.","two:guard1,guard2",[("guard1","eyes_big"),("guard2","shake"),("fire","bounce")],"crunch","A TERRIBLE NOISE")
b("narr","Then he came back. Sober now. Silent. He never told anyone what he saw.","close:boaster",[("boaster","to:-1,8.5,0"),("boaster","turn:front"),("boaster","shake")],"alarm","HE NEVER SPOKE OF IT")
b("odo","What did he see in there? What could make a man go silent?","close:odo",[("odo","eyes_big"),("boaster","exit")],None,"WHAT DID HE SEE?")
b("narr","After that night, the passage was closed up for good.","prop:seal",[("seal","show"),("pdark","vanish")],"crunch","THE PASSAGE WAS SEALED")
b("narr","And the black dog was never seen in Peel Castle again.","wide",[("dog","exit"),("guard1","exit"),("guard2","exit")],"rumble","NEVER SEEN AGAIN")
b("narr","In eighteen twenty-three, Walter Scott put the dog in a novel.","wide",[("candle1","bounce"),("candle2","bounce")],"horn","1823: WALTER SCOTT")
b("moth","So the dog is gone. Good. Lovely. Can we sleep now?","close:moth",[("moth","jump"),("odo","turn:moth")],None,"CAN WE SLEEP?")
# twist ~70%
b("narr","Then the candles flickered. Someone tall stood at the gate.","close:shepherd",[("shepherd","to:-7,12,0"),("shepherd","turn:front"),("candle1","vanish")],"alarm","HE'S AT THE GATE")
b("shepherd","Lantern-bearer. Open the gate. You cannot run from me forever.","close:shepherd",[("shepherd","shake")],"rumble","OPEN THE GATE")
b("narr","But out of the dark, the black dog came back. It stood in the gateway.","close:dog",[("dog","to:-5,10,0"),("dog","turn:shepherd")],"whoosh","THE DOG CAME BACK")
b("odo","It's not hunting us, Mothwick. It's guarding us.","close:odo",[("odo","eyes_big")],None,"IT'S GUARDING US")
b("narr","The Shepherd stared at the dog. Then he stepped back into the fog.","wide",[("shepherd","exit"),("dog","turn:front")],"rumble","HE STEPPED BACK")
# cliffhanger
b("narr","Then, from behind the sealed stones, keys began to jingle.","prop:seal",[("seal","shake"),("pdark","show")],"suspicious","KEYS IN THE WALL")
b("wren","Odo? Is that you? Come and get me. But don't come alone.","prop:seal",[("seal","bounce"),("odo","jump")],"alarm","ODO... IS THAT YOU?")
b("odo","Wren? That's my sister's voice. That's Wren!","close:odo",[("odo","to:-0.5,12,0"),("moth","jump")],"crunch","MY SISTER?")
b("narr","The black dog walked to the sealed passage. And looked back, waiting.","close:dog",[("dog","to:1.5,13,0"),("dog","turn:odo")],"rumble","IT'S WAITING")
b("narr","What do you think happens in the next part? Tell me in the comments.","close:odo",[("odo","shake"),("moth","eyes_big")],"horn","WHAT HAPPENS NEXT?")
d={"title":"Ep 33 · A Black Dog Guards This Castle. Dare?",
 "description":"What do you think happens in the next part? Tell me in the comments.",
 "lead_in":0.05,"set":{"place":"chapel","fog":0.04,"eyes":2,"moonlight":10},
 "chars":chars,"props":props,"beats":B}
json.dump(d,open('scripts3d/ep033.json','w'),indent=1,ensure_ascii=False)
w=sum(len(x['say'].split()) for x in B); print('beats',len(B),'words',w,'maxline',max(len(x['say'].split()) for x in B),'title',len(d['title']))
