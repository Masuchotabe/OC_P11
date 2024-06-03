from locust import HttpUser, task


class WebsiteUser(HttpUser):
    @task
    def index_page(self):
        self.client.get('/')

    @task
    def points_display(self):
        self.client.get('/pointsDisplay')

    @task
    def login(self):
        self.client.post('/showSummary', {'email': 'john@simplylift.co'})

    @task
    def booking_places(self):
        self.client.get('/book/Summer Strongman/Simply Lift')

    @task
    def purchase_places(self):
        self.client.post('/purchasePlaces', {'club': '', 'competition': 'Summer Strongman'})


    # @task
    # def ma_funct(self):
    # @task
    # def ma_funct(self):
    # @task
    # def ma_funct(self):



