# ПОЛУЧАЮ ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ








import requests
import csv
from time import sleep


TOKEN = ""
SEARCH_QUERY = "python"
MIN_FOLLOWERS = 1000
MAX_USERS = 10
DELAY = 1
OUTPUT_FILE = "github_users_simple.csv"

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_users_from_github(page=1, per_page=100):
    api_url = f"https://api.github.com/search/users?q={SEARCH_QUERY}&type=users&page={page}&per_page={per_page}"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return []

def get_user_followers(username):
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user_data = response.json()
        followers = user_data.get('followers', 0)
        if followers >= MIN_FOLLOWERS:
            return {
                'login': user_data.get('login', ''), 
                'profile_url': user_data.get('html_url', ''),
                'followers': followers
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных пользователя {username}: {e}")
        return None

def save_to_csv(users_data, filename):

    if not users_data:
        print("Нет данных для сохранения")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['login', 'profile_url', 'followers'])
        writer.writeheader()
        writer.writerows(users_data)
    
    print(f"\nДанные сохранены в {filename}")

def main():
    print(f"Начинаем парсинг пользователей по запросу: '{SEARCH_QUERY}'")
    

    all_users = []
    page = 1
    
    while len(all_users) < MAX_USERS:
        users = get_users_from_github(page)
        if not users:
            break
        
        remaining = MAX_USERS - len(all_users)
        all_users.extend(users[:remaining])
        
        print(f"Страница {page}: получено {len(users)} пользователей (всего {len(all_users)})")
        
        if len(users) < 100 or len(all_users) >= MAX_USERS:
            break
        
        page += 1
        sleep(DELAY)


    users_data = []
    for i, user in enumerate(all_users, 1):
        user_info = get_user_followers(user['login'])
        if user_info:
            users_data.append(user_info)
        print(f"Обработано {i}/{len(all_users)} пользователей", end='\r')
        sleep(DELAY)


    save_to_csv(users_data, OUTPUT_FILE)

if __name__ == "__main__":
    main()
