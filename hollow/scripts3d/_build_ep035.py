# builds scripts3d/ep035.json (run from hollow/)
import json
src=json.load(open('scripts3d/ep034.json'))
ch={k:src['chars'][k] for k in ('odo','moth','narr','shepherd','dog','wren')}
def H(name,voice,pitch,col,home,size=0.85):
    return {"name":name,"voice":voice,"speed":0.95,"pitch":pitch,"color":col,"kind":"human","size":size,"home":home}
ch['guest']=H("Victorian guest","bf_alice",0,[0.3,0.25,0.4],[-30,30],0.8)
ch['earl']=H("Earl Beardie","bm_fable",-2,[0.35,0.06,0.05],[30,32])
ch['stranger']=H("The Stranger","am_fenrir",-4,[0.03,0.03,0.04],[30,36],1.0)
ch['servant']=H("The servant","am_liam",0,[0.3,0.28,0.2],[-30,34],0.8)
P=lambda t,i,c,at,sc,vis=False,glow=0:{"type":t,"id":i,"color":c,"glow":glow,"visible":vis,"scale":sc,"at":at}
props=[P("cake","drum",[0.55,0.1,0.08],[-4.8,7.6,0.3],0.45,True,3),
 P("ball","lamp",[1,0.75,0.35],[-1.5,10.5,1.8],0.15,True,10),
 P("ball","lamp2",[1,0.75,0.35],[5.5,10.5,1.8],0.15,True,10),
 P("box","towel1",[0.95,0.95,0.92],[-4.1,19.2,4.2],0.6,False,2),
 P("box","towel2",[0.95,0.95,0.92],[-1.3,19.2,4.2],0.6,False,2),
 P("box","towel3",[0.95,0.95,0.92],[0.1,19.2,4.2],0.6,False,2),
 P("box","towel4",[0.95,0.95,0.92],[-5.5,19.2,4.2],0.6,False,2),
 P("box","nowin",[0.12,0.14,0.2],[-2.7,19.2,4.2],0.6,True,0.6),
 P("ball","pdark",[0.9,0.1,0.05],[-2.7,18.7,4.2],0.12,False,6),
 P("box","table",[0.25,0.15,0.08],[3.8,10.6,0],0.9,False,0),
 P("box","cards",[0.95,0.92,0.85],[3.8,10.6,1.15],0.3,False,1.5),
 P("key","key",[1.0,0.72,0.15],[-1.0,9.0,1.3],0.6,False,1),
 P("box","paper",[0.92,0.88,0.75],[-1.0,8.5,1.2],0.35,False,1)]
B=[]
def b(who,say,cam,do=(),sfx=None,text=None):
    x={"who":who,"say":say,"cam":cam,"do":[list(d) for d in do]}
    if sfx:x["sfx"]=sfx
    if text:x["text"]=text
    B.append(x)
b("narr","One window had no room behind it. So who was inside?","close:odo",[("nowin","bounce"),("odo","shake"),("drum","bounce")],"alarm","THE ROOM WITH NO DOOR")
b("moth","Odo, run! The drum is still beating, and that tall thing is outside!","close:moth",[("moth","jump"),("drum","spin")],"crunch","RUN!")
b("narr","New episode every day. Subscribe so you don't miss what happens next.","two:odo,moth",[("odo","turn:front"),("moth","turn:front"),("dog","to:-1,8,0")],None,"SUBSCRIBE")
b("narr","Last night the drum played by itself. And the Pale Shepherd stepped back.","close:shepherd",[("shepherd","to:-8,16,0"),("shepherd","turn:odo")],"whoosh","HE STEPPED BACK")
b("shepherd","Keep your little drum. I will wait where you are going.","close:shepherd",[("shepherd","shake")],"rumble","I'LL WAIT FOR YOU")
b("odo","Where we're going? The dog knows the way. Come on, Mothwick.","close:odo",[("odo","to:-3,9,0"),("dog","to:0,10,0"),("drum","to:odo")],None,"FOLLOW THE DOG")
b("narr","The black dog led them through the fog, to a castle full of windows.","wide",[("dog","to:2,12,0"),("odo","to:0,11,0"),("moth","to:1,11,0"),("shepherd","exit")],"whoosh","A CASTLE OF WINDOWS")
b("narr","This castle is real. Glamis Castle, in Angus, Scotland.","wide",[("lamp","bounce"),("lamp2","bounce")],"horn","GLAMIS CASTLE, SCOTLAND")
b("narr","The Lyon family has held it since the thirteen hundreds. And they kept a secret.","prop:key",[("key","show"),("key","spin")],"pop","A FAMILY SECRET")
b("narr","The legend says the secret was told to each heir at twenty-one. And to no one else.","prop:key",[("key","bounce")],"suspicious","TOLD ONLY AT 21")
#b("moth","A secret only one person knows? That is the worst kind of secret.","close:moth",[("moth","eyes_big"),("odo","turn:moth")],None,"ONLY ONE KNOWS")
b("narr","Visitors whispered about a hidden room. A room with no door.","prop:nowin",[("nowin","bounce")],"alarm","A ROOM WITH NO DOOR")
b("narr","One day in Queen Victoria's time, the Earl went out shooting.","wide",[("guest","to:3,10,0"),("servant","to:5.5,10,0")],"pop","WHILE THE EARL WAS OUT")
b("guest","Quick, while he's gone! A towel in every window. Every single one!","close:guest",[("guest","turn:front"),("guest","jump")],"whoosh","A TOWEL IN EVERY WINDOW")
b("narr","The guests ran from room to room, hanging towels out of the windows.","prop:towel2",[("towel1","show"),("towel2","show"),("guest","to:5,11,0")],"whoosh","ROOM TO ROOM")
b("narr","Then they ran outside, looked up at the castle, and counted.","wide",[("towel3","show"),("towel4","show"),("guest","to:2,9,0"),("servant","to:3.5,9,0")],"suspicious","THEN THEY COUNTED")
b("guest","There! That window has no towel. Which room is that?","close:guest",[("guest","eyes_big"),("guest","turn:front")],"alarm","NO TOWEL!")
b("narr","The legend says one window had no towel. Some versions say four.","prop:nowin",[("nowin","bounce")],"crunch","ONE WINDOW. NO TOWEL.")
#b("narr","A window you could see from outside, but never reach from inside.","prop:nowin",[("nowin","spin"),("guest","shake")],"rumble","NO WAY IN")
b("odo","Mothwick. Look up. Count the windows with me.","close:odo",[("odo","turn:front"),("guest","exit"),("servant","exit")],"suspicious","COUNT THEM")
b("moth","One, two, three, four. Odo, there's a light in the dark one.","close:moth",[("moth","to:2,10,0"),("pdark","show")],"suspicious","A LIGHT INSIDE")
b("narr","So who is in that room? The oldest story is about Earl Beardie.","close:earl",[("earl","to:3,10,0"),("earl","turn:front")],"rumble","EARL BEARDIE")
b("narr","A fierce lord of the fourteen hundreds, known for his temper.","close:earl",[("earl","shake"),("table","show")],"crunch","A FIERCE LORD")
b("narr","One Sunday night, the legend says, nobody would play cards with him.","prop:cards",[("cards","show"),("cards","bounce")],"pop","SUNDAY NIGHT")
b("earl","Then I'll play with the Devil himself, if no one else will!","close:earl",[("earl","jump")],"alarm","I'LL PLAY ANYONE")
b("narr","A knock at the door. A tall, dark stranger walked in.","close:stranger",[("stranger","to:6,11,0"),("stranger","turn:earl")],"crunch","A KNOCK AT THE DOOR")
b("stranger","You wanted a game, my lord. I will play. For a price.","close:stranger",[("stranger","shake"),("earl","turn:stranger")],"rumble","FOR A PRICE")
b("narr","They played behind a locked door. Shouting. Swearing. Dice rattling.","prop:cards",[("cards","spin"),("earl","shake")],"suspicious","BEHIND A LOCKED DOOR")
b("narr","A servant crept up to the keyhole, to see who the stranger was.","close:servant",[("servant","to:4.5,8.8,0"),("servant","turn:stranger")],"whoosh","THE KEYHOLE")
b("narr","The legend says a blinding light shot out through the keyhole.","close:servant",[("servant","shake"),("servant","eyes_big"),("lamp","bounce")],"alarm","A BLINDING LIGHT")
b("narr","Would you look through that keyhole? Yes or no? Tell me in the comments.","prop:key",[("key","spin"),("key","bounce")],"suspicious","WOULD YOU LOOK?")
b("narr","The stranger vanished. The legend says he won the game, and the Earl's soul.","two:earl,stranger",[("stranger","exit"),("earl","sad")],"crunch","HE WON THE GAME")
b("narr","And they say the Earl still plays on, in a room that was walled up.","prop:nowin",[("earl","exit"),("servant","exit"),("nowin","bounce")],"rumble","WALLED UP FOREVER")
b("odo","The rule here, Mothwick. Never play a game with a stranger.","close:odo",[("odo","shake")],"suspicious","NEVER PLAY WITH A STRANGER")
b("moth","I wasn't going to! I'm terrible at cards anyway.","close:moth",[("moth","jump")],None,"TERRIBLE AT CARDS")
b("narr","Is it true? An account from eighteen eighty tells of loud hammering at night.","wide",[("lamp2","bounce"),("odo","turn:front")],"crunch","HAMMERING AT NIGHT")
b("narr","But there had been no workmen at the castle for months.","close:guest",[("guest","to:3,9.5,0"),("guest","eyes_big")],"rumble","NO WORKMEN")
b("narr","In eighteen eighty-two, a New York newspaper printed the window story.","prop:paper",[("paper","show"),("paper","spin")],"pop","1882: IN THE NEWSPAPER")
b("narr","A guest in nineteen-oh-five wrote that the family loved inventing stories.","close:guest",[("guest","turn:front"),("paper","bounce")],"suspicious","JUST STORIES?")
b("narr","No one has ever shown the room. And no one has proved it isn't there.","prop:nowin",[("guest","exit"),("paper","hide")],"rumble","NO ONE KNOWS")
b("moth","So it's just a story. Stories don't have lights in them. Right, Odo?","close:moth",[("moth","to:1,10.5,0"),("moth","turn:odo")],None,"JUST A STORY?")
b("narr","From behind the stone wall came a sound. Cards. Being shuffled.","prop:cards",[("cards","spin"),("cards","bounce")],"suspicious","SHUFFLE...")
b("wren","Odo! I'm in the room with no door. He's making me play!","prop:pdark",[("pdark","bounce"),("odo","jump")],"alarm","WREN!")
b("odo","Wren! Hold on! Where's the door? There has to be a door!","close:odo",[("odo","to:1,12,0"),("moth","jump")],None,"WHERE'S THE DOOR?")
b("shepherd","There is no door, lantern-bearer. Only an empty chair. Deal him in.","close:shepherd",[("shepherd","to:-4,14,0"),("shepherd","turn:front"),("dog","shake")],"rumble","DEAL HIM IN")
b("narr","What do you think happens in the next part? Tell me in the comments.","close:odo",[("odo","shake"),("moth","eyes_big")],"horn","WHAT HAPPENS NEXT?")
s={"title":"Glamis Castle: Who's Behind the Window? (Ep 35)","description":"What do you think happens in the next part? Tell me in the comments.",
 "lead_in":0.05,"set":{"place":"chapel","fog":0.06,"eyes":4,"moonlight":10},"chars":ch,"props":props,"beats":B}
json.dump(s,open('scripts3d/ep035.json','w'),indent=1,ensure_ascii=False)
print(len(B),sum(len(x['say'].split()) for x in B),len(s['title']))
