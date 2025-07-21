#СДЕЛАЛ В ФОРМАТЕ ПРИЛОЖЕНИЯ НА FLET








import requests
import flet as ft
from datetime import datetime


GITHUB_TOKEN = ""
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_user_data(username):
    try:
        user_url = f"https://api.github.com/users/{username}"
        response = requests.get(user_url, headers=headers)
        response.raise_for_status()
        user_data = response.json()


        email_url = f"https://api.github.com/users/{username}/emails"
        email_response = requests.get(email_url, headers=headers)
        emails = email_response.json() if email_response.status_code == 200 else []


        created_at = datetime.strptime(user_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        account_age_days = (datetime.now() - created_at).days
        account_age_years = account_age_days // 365


        user_info = {
            "Логин": user_data.get("login"),
            "ID": user_data.get("id"),
            "Node ID": user_data.get("node_id"),
            "Компания": user_data.get("company") or "Не указана",
            "Дата создания": created_at.strftime('%Y-%m-%d'),
            "Возраст аккаунта": f"{account_age_years} лет ({account_age_days} дней)",
            "Публичные репозитории": user_data.get("public_repos"),
            "Email": emails[0].get("email") if emails else "Не указан",
            "URL подписчиков": user_data.get("followers_url"),
            "URL форков": f"https://api.github.com/repos/{username}/instagram_bot/forks",
            "URL событий": user_data.get("received_events_url"),
            "URL языков": f"https://api.github.com/repos/{username}/discount_bot/languages",
            "Разрешено форкирование": "Да"
        }
        
        return user_info
    
    except Exception as e:
        raise e

def main(page: ft.Page):
    page.title = "Инфо о пользователях Github"
    page.bgcolor = ft.Colors.BLACK
    page.window_width = 1920
    page.window_height = 1080
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO


    username_input = ft.TextField(
        label="Введите GitHub username",
        width=400,
        autofocus=True,
        border_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE)
    )
    
    result_column = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    status_text = ft.Text("", color=ft.Colors.RED)
    loading_indicator = ft.ProgressRing(visible=False)
    
    def create_info_row(key, value):
        return ft.Row(
            controls=[
                ft.Text(f"{key}:", weight=ft.FontWeight.BOLD, width=200),
                ft.Text(value, selectable=True)
            ],
            spacing=10
        )

    def show_user_data(e):
        username = username_input.value.strip()
        if not username:
            status_text.value = "Пожалуйста, введите username"
            status_text.color = ft.Colors.RED
            page.update()
            return
        
        loading_indicator.visible = True
        status_text.value = "Загрузка данных..."
        status_text.color = ft.Colors.BLUE
        page.update()
        
        try:
            user_data = get_user_data(username)
            result_column.controls.clear()
            

            result_column.controls.append(
                ft.Text(f"Данные пользователя {username}:", 
                       size=18, 
                       weight=ft.FontWeight.BOLD,
                       color=ft.Colors.WHITE)
            )
            

            for key, value in user_data.items():
                result_column.controls.append(create_info_row(key, value))
            
            status_text.value = f"Данные успешно загружены!"
            status_text.color = ft.Colors.GREEN
            
        except requests.exceptions.HTTPError as e:
            status_text.value = f"Ошибка: {str(e)}"
            status_text.color = ft.Colors.RED
            result_column.controls.clear()
        except Exception as e:
            status_text.value = f"Произошла ошибка: {str(e)}"
            status_text.color = ft.Colors.RED
            result_column.controls.clear()
        finally:
            loading_indicator.visible = False
            page.update()


    page.add(
        ft.Column(
            [
                ft.Text("Информация о пользователях Github", 
                       size=24, 
                       weight=ft.FontWeight.BOLD,
                       color=ft.Colors.WHITE),
                ft.Divider(height=10),
                ft.Row(
                    [
                        username_input,
                        ft.ElevatedButton(
                            "Получить данные",
                            on_click=show_user_data,
                            icon=ft.Icons.SEARCH,
                            bgcolor=ft.Colors.WHITE30,
                            color=ft.Colors.WHITE
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
                ft.Row(
                    [loading_indicator, status_text],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(height=20),
                ft.Container(
                    content=result_column,
                    padding=20,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=10,
                    expand=True
                )
            ],
            spacing=10,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
