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
            "action": {"type": "message","label": choices[idx],"text": "就跟你說我選"},
            "offsetBottom": "sm",
            }
        content["action"]["text"] += ' ' + choices[idx]
        if idx == choice_idx:
            content["style"] = "primary"
            content["action"]["text"] = '是的我就是選 ' + choices[idx]
        bubble["body"]["contents"].append(content)
    return bubble, choices[choice_idx]