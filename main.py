import time
import random
import requests

TOKEN = "8753029904:AAGQ-3SVKBOeSSNVePevtjw1fFu0P4o8Ra4"
CHAT_ID = -1003974427872

last_user = None
last_name = None
offset = None

# время следующего дропа
next_drop = time.time() + random.randint(18000, 25200)


def send(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    })


def get_updates(offset):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

    return requests.get(url, params={
        "timeout": 10,
        "offset": offset
    }).json()


while True:

    data = get_updates(offset)

    if data.get("ok"):

        for update in data.get("result", []):

            offset = update["update_id"] + 1

            if "message" in update:

                msg = update["message"]

                if "from" in msg:
                    last_user = msg["from"]["id"]
                    last_name = msg["from"]["first_name"]

    # проверка времени дропа
    if time.time() >= next_drop:

        if last_user:

            gift = random.choice([
                "🧸 Мишка",
                "💖 Любовь"
            ])

            send(
                f"🎁 ДРОП ЗАВЕРШЁН!\n\n"
                f"🏆 Победитель:\n"
                f"<a href='tg://user?id={last_user}'>{last_name}</a>\n\n"
                f"🎁 Приз: {gift}\n\n"
                f"⚠️ Напишите сюда чтобы получить приз в течение 30 минут:\n"
                f"@tgstorc"
            )

            # сброс победителя
            last_user = None
            last_name = None

        # новый таймер 5–7 часов
        next_drop = time.time() + random.randint(18000, 25200)

    time.sleep(5)
