import requests
import json

# Ваш токен (никому не показывайте!)
GITHUB_TOKEN = ""

# Настройки запроса
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_private_user_data(username):
    # Основные данные пользователя
    user_url = f"https://api.github.com/users/{username}"
    response = requests.get(user_url, headers=headers)
    response.raise_for_status()
    user_data = response.json()

    # Приватная почта (если доступна)
    email_url = f"https://api.github.com/users/{username}/emails"
    email_response = requests.get(email_url, headers=headers)
    emails = email_response.json() if email_response.status_code == 200 else []

    # Дополнительные данные (например, события)
    events_url = f"https://api.github.com/users/{username}/events"
    events_response = requests.get(events_url, headers=headers)
    events = events_response.json() if events_response.status_code == 200 else []

    return {
        "user": user_data,
        "private_emails": emails,
        "activity_events": events
    }

if __name__ == "__main__":
    username = input("Введите GitHub username: ")
    data = get_private_user_data(username)
    
    with open(f"github_user_{username}_private.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Данные сохранены в github_user_{username}_private.json")








