import os
import requests


def send_code_via_bot(id, code):
    url = f"https://api.telegram.org/bot{os.getenv("TELEGRAM_BOT_TOKEN")}/sendMessage"

    data = {
        "chat_id": id,
        "text": f"Your verification code is: ``` {code} ```"
    }
    response = requests.post(url, data=data)
    result = response.json()

    if response.status_code == 200:
        return result
    else:
        print(f"Error: {response.text}")
        return None

def get_file_link(file_id):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/getFile?file_id={file_id}"
    response = requests.get(url)
    result = response.json()

    if response.status_code == 200:
        file_path = result["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/{file_path}"
        return file_url
    else:
        print(f"Error: {response.text}")
        return None

def send_photo_and_get_file_link(IMAGE_PATH, chat_id = os.getenv("IMAGE_SAVING_ID"), message=None):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendPhoto"

    with open(IMAGE_PATH, "rb") as img:
        files = {"photo": img}
        data = {"chat_id": chat_id, "caption": message}

        response = requests.post(url, data=data, files=files)
        result = response.json()

        if response.status_code == 200:
            file_id = result["result"]["photo"][-1]["file_id"]
            file_link = get_file_link(file_id)
            if not file_link:
                return None
            return file_link
        else:
            print(f"Error: {response.text}")
            return None

def send_message_to_customer(chat_id, message):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    result = response.json()

    if response.status_code == 200:
        return result
    else:
        print(f"Error: {response.text}")
        return None
