import time
import random
import requests

TOKEN = "8753029904:AAGQ-3SVKBOeSSNVePevtjw1fFu0P4o8Ra4"
CHAT_ID = -1003974427872

offset = None


def send(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    })


def get_updates(offset):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

    r = requests.get(url, params={
        "timeout": 30,
        "offset": offset
    })

    return r.json()


while True:

    # Ждём 5–10 секунд (для теста)
    # Для 5–7 часов:
    # random.randint(18000, 25200)

    wait = random.randint(5, 10)
    time.sleep(wait)

    # Получаем последние сообщения
    data = get_updates(offset)

    last_user = None
    last_name = None

    if data.get("ok"):

        for update in data.get("result", []):

            offset = update["update_id"] + 1

            if "message" not in update:
                continue

            msg = update["message"]

            # Проверяем чат
            if msg.get("chat", {}).get("id") != CHAT_ID:
                continue

            user = msg.get("from")

            if not user:
                continue

            # Игнорируем ботов
            if user.get("is_bot"):
                continue

            # Сохраняем последнего человека
            last_user = user["id"]
            last_name = user.get("first_name", "User")

    # Если нашли человека
    if last_user:

        gift = random.choice([
            "🧸 Мишка",
            "💖 Сердце"
        ])

        send(
            f"🎁 ДРОП ЗАВЕРШЁН!\n\n"
            f"🏆 Победитель:\n"
            f"<a href='tg://user?id={last_user}'>{last_name}</a>\n\n"
            f"🎁 Приз: {gift}\n\n"
            f"⚠️ Напишите сюда чтобы получить приз в течение 30 минут:\n"
            f"@tgstorc"
        )
