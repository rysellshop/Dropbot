import requests
import time
import random
import os

# Railway Variables
TOKEN = os.getenv("8753029904:AAFeLa-DNdvJ62Yk6pAnL6QzRHLwoOWVhJ8")

# ID группы
CHAT_ID = -1003974427872

last_user = None
last_name = None
offset = None

# следующий дроп через 5–7 часов
next_drop = time.time() + random.randint(18000, 25200)


def send(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
    )


while True:

    try:

        # получаем сообщения
        response = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/getUpdates",
            params={
                "offset": offset,
                "timeout": 10
            }
        ).json()

        if response.get("ok"):

            for update in response.get("result", []):

                offset = update["update_id"] + 1

                if "message" in update:

                    msg = update["message"]

                    # сохраняем ПОСЛЕДНЕГО написавшего
                    if "from" in msg:

                        last_user = msg["from"]["id"]
                        last_name = msg["from"]["first_name"]

        # если время дропа пришло
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
                    f"⚠️ Напишите чтобы получить приз в течение 30 минут:\n"
                    f"@tgstorc"
                )

                # сброс
                last_user = None
                last_name = None

            # новый таймер 5–7 часов
            next_drop = time.time() + random.randint(18000, 25200)

        time.sleep(2)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(5)
