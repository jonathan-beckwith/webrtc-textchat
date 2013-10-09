from random import choice
import json

import cherrypy

adjectives = ['adorable','adventurous','aggressive','agreeable','alert','alive','amused','angry','annoyed','annoying','anxious','arrogant','ashamed','attractive','average','awful','bad','beautiful','better','bewildered','black','bloody','blue','blue-eyed','blushing','bored','brainy','brave','breakable','bright','busy','calm','careful','cautious','charming','cheerful','clean','clear','clever','cloudy','clumsy','colorful','combative','comfortable','concerned','condemned','confused','cooperative','courageous','crazy','creepy','crowded','cruel','curious','cute','dangerous','dark','dead','defeated','defiant','delightful','depressed','determined','different','difficult','disgusted','distinct','disturbed','dizzy','doubtful','drab','dull','eager','easy','elated','elegant','embarrassed','enchanting','encouraging','energetic','enthusiastic','envious','evil','excited','expensive','exuberant','fair','faithful','famous','fancy','fantastic','fierce','filthy','fine','foolish','fragile','frail','frantic','friendly','frightened','funny','gentle','gifted','glamorous','gleaming','glorious','good','gorgeous','graceful','grieving','grotesque','grumpy','handsome','happy','healthy','helpful','helpless','hilarious','homeless','homely','horrible','hungry','hurt','ill','important','impossible','inexpensive','innocent','inquisitive','itchy','jealous','jittery','jolly','joyous','kind','lazy','light','lively','lonely','long','lovely','lucky','magnificent','misty','modern','motionless','muddy','mushy','mysterious','nasty','naughty','nervous','nice','nutty','obedient','obnoxious','odd','old-fashioned','open','outrageous','outstanding','panicky','perfect','plain','pleasant','poised','poor','powerful','precious','prickly','proud','puzzled','quaint','real','relieved','repulsive','rich','scary','selfish','shiny','shy','silly','sleepy','smiling','smoggy','sore','sparkling','splendid','spotless','stormy','strange','stupid','successful','super','talented','tame','tender','tense','terrible','testy','thankful','thoughtful','thoughtless','tired','tough','troubled','ugliest','ugly','uninterested','unsightly','unusual','upset','uptight','vast','victorious','vivacious','wandering','weary','wicked','wide-eyed','wild','witty','worrisome','worried','wrong','zany','zealous']
fruits = ['beet','cherry','cranberry','pomegranate','radish','raspberry','rhubarb','strawberry','tomato','watermelon','apricot','carrot','fuyu','kumquat','mango','minola','nectarine','orange','peach','persimmon','pumpkin','satsuma','tangerine','corn','lemon','pear','pineapple','plantain','quince','starfruit','artichoke','arugula','asparagus','avocado','basil','broccoflower','broccoli','cabbage','celery','chard','cilantro','cucumber','edamame','endive','escarole','fennel','honeydew','jalapeno','kale','kiwifruit','leek','lettuce','lime','mache','okra','parsley','pea','spinach','sprout','tomatillo','watercress','zucchini','blueberry','acai','boysenberry','eggplant','fig','radicchio','shallot','turnip','banana','cauliflower','coconut','garlic','ginger','jicama','lychee','mushroom','onion','parsnip','potato','blackberry','date','mushroom','truffle','grapefruit','guava','papaya']

adjectives = [x.capitalize() for x in adjectives]
fruits = [x.capitalize() for x in fruits]

class Signals():

    rooms = {}

    def clear(self):
        self.rooms = {}
        return json.dumps({ 'keys': [x for x in self.rooms.keys()] })
    clear.exposed = True

    def list(self):
        return json.dumps([x for x in self.rooms.keys() if ':offer' in x])
    list.exposed = True

    @cherrypy.tools.json_in()
    def get(self):
        result = self.rooms.get(
            cherrypy.request.json['id'],
            None
        );

        if result is None:
            raise cherrypy.HTTPError(404)
        return json.dumps(result);
    get.exposed = True

    @cherrypy.tools.json_in()
    def set(self):
        data = cherrypy.request.json

        self.rooms[data['id']] = data['data']
        print('SET:{0}={1}'.format(
            data['id'],
            data['data']
        ))
        return json.dumps({ 'status': 'OK' })
    set.exposed = True

    def default(self, room=None):
        text = None
        with open('webrtc.html') as f:
            text = ''.join(f.readlines())

        if room is None:
            room = '{0} {1}'.format(
                choice(adjectives),
                choice(fruits)
            )

        text = text.replace(
            '$DEFAULT_NAME$',
            room
        )
        return text;
    default.exposed = True

cherrypy.quickstart(
    root=Signals(),
    config={
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8003
        }
    })