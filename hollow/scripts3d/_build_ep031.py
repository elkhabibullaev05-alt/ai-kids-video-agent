# Builds scripts3d/ep031.json (run from hollow/)
import json
src=json.load(open('scripts3d/ep030.json'))
chars={k:src['chars'][k] for k in ('odo','moth','narr','shepherd')}
chars['shepherd']['home']=[30,30]
chars['collie']={"name":"Norman Collie","voice":"bm_lewis","speed":0.95,"pitch":-1,"color":[0.55,0.42,0.28],"kind":"human","size":0.85,"home":[1.5,12.0]}
chars['welsh']={"name":"Hugh Welsh","voice":"am_michael","speed":1.0,"pitch":0,"color":[0.2,0.3,0.4],"kind":"human","size":0.8,"home":[-30,30]}
chars['brother']={"name":"His brother","voice":"am_puck","speed":1.05,"pitch":1,"color":[0.4,0.22,0.15],"kind":"human","size":0.75,"home":[-30,32]}
chars['frere']={"name":"Richard Frere","voice":"am_eric","speed":1.0,"pitch":0,"color":[0.25,0.25,0.3],"kind":"human","size":0.85,"home":[-30,34]}
chars['grey']={"name":"The Grey Man","voice":"bm_daniel","speed":0.8,"pitch":-3,"color":[0.42,0.44,0.46],"kind":"greyman","size":1.5,"home":[7.0,24.0]}
props=[
 {"type":"box","id":"cairn","color":[0.4,0.4,0.42],"visible":True,"scale":1.2,"at":[7.0,15.0,0.6]},
 {"type":"ball","id":"mark","color":[0,0,0],"visible":False,"scale":0.1,"at":[3.0,14.0,1.5]},
 {"type":"ball","id":"glory","color":[0.7,0.75,0.9],"glow":0.9,"visible":False,"scale":4.0,"at":[-5.0,24.0,6.0]},
 {"type":"ball","id":"moon","color":[0.95,0.9,0.75],"glow":12,"visible":False,"scale":1.4,"at":[14,40,16]},
]
B=[]
def b(who,say,cam,do=(),sfx=None,text=None):
    x={"who":who,"say":say,"cam":cam,"do":[list(d) for d in do]}
    if sfx:x["sfx"]=sfx
    if text:x["text"]=text
    B.append(x)
b("narr","Something was walking behind them in the fog. And every step it took was far too long.","wide",[("odo","shake"),("moth","jump"),("grey","to:6,21,0")],"crunch","DON'T LOOK BACK")
b("moth","Odo! Every time we take a step, something takes one after us!","close:moth",[("moth","shake"),("odo","turn:moth")],"crunch","SOMETHING IS FOLLOWING")
b("odo","Keep walking, Mothwick. Whatever you do, don't turn around.","close:odo",[("odo","eyes_big"),("moth","to:-4.5,7.5,0")],"suspicious","KEEP WALKING")
b("narr","New episode every day. Subscribe so you don't miss what happens next.","two:odo,moth",[("odo","turn:front"),("moth","turn:front")],None,"SUBSCRIBE")
b("narr","They had run from the Oak Island pit, up and up, into the mountains of Scotland.","wide",[("odo","to:-6,8,0"),("moth","to:-4,8,0"),("grey","to:30,40,0")],"whoosh","RUNNING FROM THE PIT")
b("narr","This is a true story, from the records of a famous mountain climber.","wide",[("moon","show"),("collie","jump")],None,"A TRUE STORY")
b("narr","Ben Macdui. The highest mountain in the Cairngorms, and the second highest in Britain.","prop:cairn",[("cairn","bounce")],"horn","BEN MACDUI, SCOTLAND")
b("narr","The year is eighteen ninety-one. A professor named Norman Collie is climbing alone.","close:collie",[("collie","turn:front")],None,"1891: ALONE")
b("collie","Thick mist all around me. I can hardly see the stones at my feet.","close:collie",[("collie","shake")],"suspicious","THICK MIST")
b("odo","He's alone up there? In this fog? That's the worst idea I've ever heard.","close:odo",[("odo","turn:collie")],None,"ALONE IN THE FOG")
b("narr","Near the top, Collie turned and started back down the mountain.","wide",[("collie","to:-1,10,0"),("grey","to:8,26,0")],"crunch","GOING DOWN")
b("collie","Then I began to hear something else. Not just my own footsteps.","close:collie",[("collie","eyes_big")],"crunch","SOMETHING ELSE")
b("narr","He later said: for every few steps he took, he heard a crunch.","close:grey",[("grey","to:7,23,0"),("grey","turn:front")],"crunch","CRUNCH")
b("narr","Then another crunch, as if someone was walking after him.","wide",[("grey","to:6,22,0"),("collie","shake")],"crunch","SOMEONE BEHIND HIM")
b("collie","But the steps were three or four times longer than my own!","close:collie",[("collie","jump")],"alarm","STEPS 4 TIMES LONGER")
b("moth","Four times longer? Odo, how big are the legs on that thing?","close:moth",[("moth","eyes_big")],None,"HOW BIG?")
b("narr","Collie saw nothing in the mist. But he was seized with terror.","close:grey",[("grey","turn:front")],"suspicious","HE SAW NOTHING")
b("narr","He ran, and he did not stop for four or five miles.","wide",[("collie","exit"),("grey","to:2,20,0")],"whoosh","HE RAN 5 MILES")
b("odo","The rule, Mothwick: if footsteps follow you in the fog, don't look back.","close:odo",[("odo","shake")],"suspicious","DON'T LOOK BACK")
b("moth","Don't stop. Don't look. Got it. My wings are already running.","close:moth",[("moth","jump")])
b("narr","Collie kept this secret for thirty-four years.","wide",[("grey","to:30,40,0"),("collie","to:1.5,12,0")],"horn","34 YEARS OF SILENCE")
b("narr","Then, in December nineteen twenty-five, he told the Cairngorm Club in Aberdeen.","close:collie",[("collie","turn:front")],None,"1925: HE TOLD THEM")
b("collie","There is something very queer about the top of Ben Macdui. I will not go back there alone.","close:collie",[("collie","shake")],"alarm","I WILL NOT GO BACK")
b("narr","The newspapers printed his words. And other climbers began to speak.","wide",[("collie","exit"),("welsh","to:0,12,0"),("brother","to:3.5,12.5,0")],"horn","OTHERS SPOKE UP")
b("narr","In nineteen oh four, Hugh Welsh and his brother camped near the top.","two:welsh,brother",[("welsh","turn:front"),("brother","turn:welsh")],None,"1904: TWO BROTHERS")
b("welsh","Listen! Slow, slurring footsteps. Like someone walking through wet gravel.","close:welsh",[("welsh","eyes_big")],"crunch","SLURRING FOOTSTEPS")
b("brother","But nobody is out there. I can see the whole ridge!","close:brother",[("brother","shake")],"suspicious","NOBODY IS THERE")
b("narr","In nineteen forty-eight, a climber named Richard Frere felt a Presence on the summit.","close:frere",[("welsh","exit"),("brother","exit"),("frere","to:1,12,0"),("frere","turn:front")],"alarm","1948: A PRESENCE")
b("frere","Something I could not see. And a high, singing note in the air.","close:frere",[("frere","shake")],"suspicious","A SINGING NOTE")
b("narr","People started calling it Am Fear Liath Mor. The Big Grey Man.","close:grey",[("grey","to:6,21,0"),("grey","turn:front")],"rumble","THE BIG GREY MAN")
b("moth","Odo. The fog in front of us. It's moving.","close:moth",[("moth","shake"),("frere","exit")],"crunch","IT'S MOVING")
b("narr","Through the mist rose a giant grey shape, as tall as a house.","wide",[("glory","show"),("all","shake")],"alarm","AS TALL AS A HOUSE")
b("odo","Wait, Mothwick. Lift your wing. Now drop it.","close:odo",[("odo","turn:moth"),("moth","jump")],"suspicious","LIFT YOUR WING")
b("narr","The giant lifted its wing too. It was Mothwick's own shadow, thrown onto the cloud.","wide",[("glory","bounce"),("moth","spin")],"whoosh","IT WAS A SHADOW")
b("narr","Scientists call it a Brocken spectre. Your shadow on the mist can look like a giant.","wide",[("glory","bounce")],None,"A BROCKEN SPECTRE")
b("narr","Others blame tired minds, wind noise, or the lonely dark.","two:odo,moth",[("odo","happy")],None,"SHADOWS AND WIND?")
b("moth","So it was just me! Phew. I scared myself.","close:moth",[("moth","happy"),("moth","jump")],"pop","JUST A SHADOW")
b("narr","But a shadow makes no sound. And nobody has explained the footsteps.","close:odo",[("glory","vanish"),("odo","eyes_big")],"crunch","BUT THE FOOTSTEPS...")
b("narr","They stood perfectly still. And behind them, something took one long step.","wide",[("odo","shake"),("moth","shake")],"crunch","THEY STOPPED. IT DIDN'T.")
b("shepherd","Such long steps, lantern-bearer. I have walked behind you all night.","close:shepherd",[("shepherd","to:-2,11,0"),("shepherd","turn:front")],"alarm","IT WAS BEHIND THEM")
b("narr","What do you think happens in the next part? Tell me in the comments.","close:odo",[("odo","shake"),("moth","eyes_big")],"horn","WHAT HAPPENS NEXT?")
d={"title":"Ep 31 · Who Walked Behind Him in the Fog?",
 "description":"What do you think happens in the next part? Tell me in the comments.",
 "lead_in":0.05,"set":{"place":"hill","fog":0.04,"eyes":2,"moonlight":14},
 "chars":chars,"props":props,"beats":B}
json.dump(d,open('scripts3d/ep031.json','w'),indent=1,ensure_ascii=False)
w=sum(len(x['say'].split()) for x in B); print('beats',len(B),'words',w, 'maxline',max(len(x['say'].split()) for x in B))
