from locust import HttpUser, task


class WebsiteUser(HttpUser):
    @task
    def index_page(self):
        self.client.get('/')

    def login(self):
        self.client.post('/showSummary', )

