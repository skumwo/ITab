from locust import HttpUser, task, between
from bs4 import BeautifulSoup

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # 1. Получаем страницу логина и вытаскиваем токен
        response = self.client.get("/users/login/")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", attrs={"name": "csrfmiddlewaretoken"})["value"]

        # 2. Отправляем логин с csrf
        self.client.post("/users/login/", {
            "username": "buyer",
            "password": "test123456",
            "csrfmiddlewaretoken": csrf_token
        }, headers={"Referer": "/users/login/"})

    @task
    def view_products(self):
        self.client.get("/products/")
