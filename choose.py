import json
import random

def make_bubble(choices):
    choice_idx = random.randint(0, len(choices)-1)
    bubble = json.load(open('./bubble.json'))
    for idx in range(len(choices)):
        content = {
            "type": "button",
            "style": "secondary",
            "height": "md",
            "action": {
                "type": "postback",
                "label": choices[idx],
                "data": '可惜了，這就是命',
                "displayText": "殘念～原來是抽到"
                },
            "offsetBottom": "sm",
            }
        content["action"]["displayText"] += ' ' + choices[idx]
        if idx == choice_idx:
            content["style"] = "primary"
            content["action"]["data"] = '恭喜恭喜'
            content["action"]["displayText"] = '太好了抽到 ' + choices[idx]
        bubble["body"]["contents"].append(content)
        
    return bubble, choices[choice_idx]