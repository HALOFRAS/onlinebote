from flask import Flask, request, json

import vk_api
import random

vk = vk_api.VkApi(token="7f7295354ac9e9922cb981a93a038db9118b7b249d064ce113eb9d267deaef4a7c9f47ad89e2c06baa28f")

keyboard = {
    "one_time": False,
    "buttons": [
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "!зашёл"
                },
                "color": "positive"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "!вышел"
                },
                "color": "negative"
            }],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "!инфо"
                },
                "color": "primary"
            }]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

online=[]
onlined=""

app = Flask(__name__)

@app.route('/', methods = ["POST"])
def main():
    data = json.loads(request.data)
    if data["type"] == "confirmation":
        return "26d82a4c"
    elif data["type"] == "message_new":
        object = data["object"]
        id = object["peer_id"]
        body = object["text"]
        msg1 = body.lower().split(" ")
        idf=str(id)+".txt"
        if msg1[0] == "!ник":
            if len(msg1) == 1:
                vk.method("messages.send", {"peer_id": id, "message": "Введите !ник Имя", "random_id": random.randint(1, 2147483647),
                                            "keyboard": keyboard})
            else:
                if "_" in msg1[1]:
                    pass
                    nick = msg1[1].split("_")
                    nickname = nick[0].title()+"_"+nick[1].title()
                    file = open("mysite/"+idf, 'w')
                    file.write(nickname)
                    file.close()
                    vk.method("messages.send", {"peer_id": id, "message": "Новый ник: " + nickname, "random_id": random.randint(1, 2147483647),
                                                "keyboard": keyboard})
                else:
                    vk.method("messages.send", {"peer_id": id, "message": "Это не рп ник!", "random_id": random.randint(1, 2147483647),
                                                "keyboard": keyboard})
            if body.lower() == "!вышел":
                try:
                    file = open("mysite/"+idf)
                except IOError as e:
                    vk.method("messages.send", {"peer_id": id, "message": "Используйте !ник", "random_id": random.randint(1, 2147483647)
                                        })
                else:
                    nickname = file.read()
                    file.close()
                    try:
                        online.remove(nickname)
                    except ValueError as e:
                        vk.method("messages.send", {"peer_id": id, "message": "Игрок "+nickname+" не на сервере!", "random_id": random.randint(1, 2147483647),
                                                    "keyboard": keyboard})
                    else:
                        onlined=""
                        for i in range(len(online)):
                            if online[i] == " ":
                                pass
                            else:
                                onlined=onlined+online[i]+"\n"
                        vk.method("messages.send", {"peer_id": id, "message": "⚠ Игрок "+nickname+" вышел с сервера\n"+"Сейчас на сервере:\n"+onlined, "random_id": random.randint(1, 2147483647),
                                                    "keyboard": keyboard})
        if body.lower() == "!зашёл":
            try:
                file = open("nickname/"+idf)
            except IOError as e:
                vk.method("messages.send", {"peer_id": id, "message": "Используйте !ник", "random_id": random.randint(1, 2147483647),
                                            })
            else:
                nickname = file.read()
                file.close()
                if online.count(nickname) >= 1:
                    vk.method("messages.send", {"peer_id": id, "message": "Игрок "+nickname+" уже на сервере", "random_id": random.randint(1, 2147483647),
                                                "keyboard": keyboard})
                else:
                    online.append(nickname)
                    onlined=""
                    for i in range(len(online)):
                        if online[i] == " ":
                            pass
                        else:
                            onlined=onlined+online[i]+"\n"
        if body.lower() == "!инфо":
            vk.method("messages.send", {"peer_id": id, "message": "✅ Игрок "+nickname+" зашёл на сервер\n"+"Сейчас на сервере:\n"+onlined, "random_id": random.randint(1, 2147483647),
                                        "keyboard": keyboard})
        else:
            pass
    return "ok"