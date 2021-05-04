from azure.cognitiveservices.personalizer import PersonalizerClient
from azure.cognitiveservices.personalizer.models import RankableAction, RewardRequest, RankRequest
from msrest.authentication import CognitiveServicesCredentials

import datetime, json, os, time, uuid, ast

key = "3c06cba4080f40baabe8090f79c2f0bd"
endpoint = "https://musicrec.cognitiveservices.azure.com/"


names = ['MONTERO (Call Me By Your Name)','Save Your Tears (with Ariana Grande) (Remix)','Heartbreak Anniversary','Kiss Me More (feat. SZA)',
'RAPSTAR','Levitating (feat. DaBaby)','Peaches (feat. Daniel Caesar & Giveon)','Leave The Door Open','Astronaut In The Ocean',
'Goosebumps - Remix','deja vu','Beautiful Mistakes (feat. Megan Thee Stallion)','Hold On','Up','Best Friend (feat. Doja Cat)','WITHOUT YOU','Heat Waves',
'Friday (feat. Mufasa & Hypeman) - Dopamine Re-Edit','Arcade','telepatía','The Business','Fiel','My Head & My Heart','GIRL LIKE ME','Met Him Last Night (feat. Ariana Grande)',
'Streets','Your Love (9PM)','You','Runaway','Cover Me In Sunshine','BED','Good Without','Girls Like Us','Otra Noche Sin Ti','On The Ground','Shy Away',
'As I Am (feat. Khalid)','Good Days','Wasted Love (feat. Lagique)','Paradise (feat. Dermot Kennedy)','34+35','drivers license','Follow You','Mood (feat. iann dior)',
'DÁKITI','Therefore I Am','Baila Conmigo (with Rauw Alejandro)','Calling My Phone','What’s Next']



client = PersonalizerClient(endpoint, CognitiveServicesCredentials(key))


songs = []

with open('data.json', 'r', encoding='UTF-8') as f:
    new_streamings = ast.literal_eval(f.read())
    songs += [streaming for streaming 
                    in new_streamings]

def get_actions():
    actions = []
    for i in range(49):
        characteristics = []
        characteristics.append(songs[i])
        action = RankableAction(id=names[i], features=characteristics)
        actions.append(action)

    return actions


def get_user_timeofday():
    res={}
    time_features = ["morning", "afternoon", "evening", "night"]
    time = input("What time of day is it (enter number)? 1. morning 2. afternoon 3. evening 4. night\n")
    try:
        ptime = int(time)
        if(ptime<=0 or ptime>len(time_features)):
            raise IndexError
        res['time_of_day'] = time_features[ptime-1]
    except (ValueError, IndexError):
        print("Entered value is invalid. Setting feature value to", time_features[0] + ".")
        res['time_of_day'] = time_features[0]
    return res



def get_user_mood():
    res = {}
    mood_features = ['happy','energetic','nostalgic','sleepy']
    pref = input("In what type of mood are you? Enter number 1.happy 2.energetic 3.nostalgic 4.sleepy\n")
    
    try:
        ppref = int(pref)
        if(ppref<=0 or ppref>len(mood_features)):
            raise IndexError
        res['mood_preference'] = mood_features[ppref-1]
    except (ValueError, IndexError):
        print("Entered value is invalid. Setting feature value to", mood_features[0]+ ".")
        res['mood_preference'] = mood_features[0]
    return res


keep_going = True
while keep_going:

    eventid = str(uuid.uuid4())

    context = [get_user_mood(), get_user_timeofday()]
    actions = get_actions()

    rank_request = RankRequest( actions=actions, context_features=context, excluded_actions=[], event_id=eventid)
    response = client.rank(rank_request=rank_request)
    
    print("Personalizer service ranked the actions with the probabilities listed below:")
    
    rankedList = response.ranking
    for ranked in rankedList:
        print(ranked.id, ':',ranked.probability)

    print("Personalizer thinks you would like to have", response.reward_action_id+".")
    answer = input("Is this correct?(y/n)\n")[0]

    reward_val = "0.0"
    if(answer.lower()=='y'):
        reward_val = "1.0"
    elif(answer.lower()=='n'):
        reward_val = "0.0"
    else:
        print("Entered choice is invalid. Service assumes that you didn't like the recommended food choice.")

    client.events.reward(event_id=eventid, value=reward_val)

    br = input("Press Q to exit, any other key to continue: ")
    if(br.lower()=='q'):
        keep_going = False



