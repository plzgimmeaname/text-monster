# Names: Sreekar Karra, Zayan Sikder, John Steele
# Period: 2
# Date Last Edited: 10/20/26

import random
import names

names.get_full_name()

def random_name():
    return names.get_first_name()

def npc():
    return names.get_full_name()

backstories = [

#npc name and random name is place holders i couldnt figure it out
#player name works i think
"""
Night creeps over the Union of random name. Land in ruin after the event's in random place's Grotto,
making many left in poverty and in hunger, moving in a vegetative state. You walk over countless bodies making
your way to the local tavern after a rough encounter with thugs that lent you money. Desperate for some food,
you beg the tavern owner, npc name, for leftovers. NPC: ('If you could beg, you could work' )
player name: 'Please anything is enough, after I get some food ill work, I need to pay back my debt.'. 
NPC: 'Theres a dungeon out west, maybe you could sell the materials you get from the monsters, 
or even better, find some treasure. anyways youd be doing a service to this country after all, 
nobody wants to be near those monsters after what they did to the grotto'. 
player name: 'Really? I'll head there now. I would do anything for a quick buck.'
You soon regret your words after you see the dungeon stairs covered in corpses, all died with the same motivation as you. 
'What could go wrong' you thought as you decend into the Labyrinth of Zayan.""",

    """
Many believed the forest of random name was flourished with monsters of all kinds, from slimes 
to skeletons. You awake under a treestump, vaguely remebering the name that was given to you by 
your parents, player name. You start to wander around looking for civilization and stumble across
some ruins, marked with some sort of geoglyphs of an ancient tribe. You decend into the temple
with a staircase covered by the effects of nature. Along the walls is torches that are surprisingly
lit even though the area took a toll. Taking a closer look at the geoglyphs, you see a faint figure
depicted mostly thoughout all of them. As you walk up, you see a name, npc name, explaining
they were once the ruler in this forest. Wanting to find out more, you go further down the stairs, 
wondering what happened to this area that once was inhabited.
""",

    """
You are an average citizen that makes barely enough to scrape by. Countless interviews for
jobs that you dont even have the experience for hoping the name, player name, catches someones 
attention. Wasting away, you make one last ditch effort into one more interview. 'Hello, I will'
'be interviewing you today my name is random name.' 'Hello thank you so much...' Your words are cut
off from the commotion coming from outside. A gate to another world was opened right then and there.
All common sense was thrown out the window after this event. Every event was called off, from sports
events to world conflicts. The government needs volunteers to explore this phenomena and is willing 
to put cash on the table. You immediately sign up and get to be the chosen few to explore this place.
However, as soon as you step in, you are seperated from your squad and stripped of your equipment,
 leaving only your uniform they gave you. You are forced to explore this Labyrinth on your own.
""",

    """
In the eyes of the random name people, if you cannot provide the tribe tax, you get sent to the 
Labyrinth where you are forced to survive for as long as you can. Your friend, who was recently
sent there, left you a letter before he was dragged out from his house by the guards. 'Dear player name,'
'I hope you will not miss me when I'm taken. Don't expect me to come back, you know what happens down there.'
Anyways, I just wanted you to know that out time together was the best I ever had. But I'm scared,'
'my one favor that I want you to fufill for me, come save me, please...' Mortified, you seek out the guards 
to help your friend. They let you in without any hesitation because they know you won't come back. 
"They better have a huge IOU for me after this" you say after you decend to the unknown.
""",
    """
"Wake up!" your little sibling, random name yells. Annoyed, you throw a pebble at them. 
"Hey! Stop that player name!" The country of random place collapsed onto itself after the widepsread
practice of putting data centers on ever inch of land. As a result, residents are forced to reside 
underground now, mining away for new hope. You get up and make your way into the mining shaft. 
You feel a bit hyper and decide to stray away from your group to go explore. You make your way to 
to an abandoned minecart track that has the big bold letters, "DO NOT ENTER". You don't care and 
decide to go anyways having the time of your life. As you are riding, the minecart jolts and you 
stumble off of it, gravity pulling you toward the cold hard ground. Every wall is blank,
 no sign of an exit anywhere. However, some parts started to erode so you ram your body to budge it.
After a few tries and some aching pain in your shoulder, you crumble the wall. It leads to an 
area further underground, your only option is to go down. Not like anyone will help you anyways.
""",
    """
The kingdom of random name was once in fear of the Great Evil Zayan. The government 
summoned you from earth hoping you would defeat this wretched monster. After tough encounters
with demons of all kinds, you best the Great Evil so the civilains of the kingdom can sleep soundly
tonight. "You have bested me fair and square, drop you weapon and hear my final words player name." 
You do not oppose to this request for some strange reason, their words had this allure to them.
 You walk up to them, waiting for his final words. "Thank you for granting my request. However,"
 "you should know to never trust a demon." The floor under you shatters, revealing
a whole new dungeon below it. You begin to plunge down into the abyss, waiting to face your next
challenge to make your way back up and report back to the kingdom.
""",

    """
You grew up in an abusive household. Parents always bickering, shouting, and complaining. 
You were sick of it. Sick of being here. Sick of being called player name by them.
The basement was the only safe space to you. You would reside there when they would argue.
One day you found an entrance while staying there after they fought about your performance in school.
It looked bottomless, you picked up a stone and threw it to see how far it went down. "1, 2, 3..."
you count. An echo came back after 10 seconds. In awe, you lean off the edge to try and see further.
You stumble into the hole, but it wasn't on acccident. You try to face up while you are falling.
You see two shadowy figures hovering over the entrance, it was your parents. A bittersweet feeling
washes over you. Relief that you are gone from their pointless hatred, but sad since your own parents abandoned you.
You swear that no matter what, you will survive. 
""",

"""
You are an adventurer. You make an honest living killing moneters and looting dungeons. 
The guild you work for treats you well. Your party however, the random names, treats you like a lackey. Carrying everyones
 items, loot, and materials. You make your way to a new dungeon for a rank-up assignemnt, finally becoming
S-rank like you have always dreamed of. Your party beats the dungeon boss and starts collecting the loot.
They find a double-dungeon however, a phenomena that has a dungeon inside a dungeon. They realized that 
they do not need you anymore so they lock you into the dungeon to get rid of dead weight. 
Wanting revenge, you vow to yourself you will climb out of this situation and make them regret 
making an enemy of player name.
""",

    """
You are riding a bus with the nametag, player name, when you are suddenly skydiving through the air. Around 100 people are also
skydiving to a huge island in the middle. You see chests scattered everywhere. This seems like 
a big battle royale where everyone has to duke it out and be the last one standing. Time seems to be 
accelerated here so day and night cycles happen in 10 minutes. For the night, you build a house in the
middle of a forest called the Weeping random name's'. You see a bunker however and make your way to there.
After you swing with your pickaxe that was given to you for some reason, you eventually open the
sealed entrance, breaking your pickaxe in the process. You dive in to the secret bunker, hoping to find 
a way out of this loop.
""",

    """
Mazes have always been your forte. Solving puzzles that stumped even the most experienced 
adventurers couldn't solve. This led to you developing quite an ego. You never respected anyone anymore.
You only dined at the finest restaurants, but you were still rude to the employee's. Your ego made your own name
become a saying people told. "You player name!" You didn't mind, you were making so much money you didn't care.
Few months pass by and you are still getting your ego inflated. You seem so sure that you are doing everything right, 
that you forget to check stuff off. It works the first few times, but you push your luck way too far.
You make a simple mistake, but it leaves you hopelessly trapped in the Labyrinth of Zayan.
Maybe this is a reality check for all the times you have been rude to people. Maybe once you get out of here,
 you will start to change for the better.
""",

]

#Generates random backstory for the game using the names library to randomly generate a random name for the placeholders 
def get_story(name: str):
    selected_backstory = random.choice(backstories)
    selected_backstory = selected_backstory.replace("player name", name)
    selected_backstory = selected_backstory.replace("random name", random_name())
    selected_backstory = selected_backstory.replace("random place", random_name())
    selected_backstory = selected_backstory.replace("npc name", random_name())
    return selected_backstory
