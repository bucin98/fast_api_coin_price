from locust import FastHttpUser, task, between


class MyUser(FastHttpUser):
    min_wait = 0
    max_wait = 0
    @task
    def get_courses_binance(self):
        response = self.client.get("/api/v1/courses/?source=binance")
        assert response.status_code == 200

    @task
    def get_courses_coingecko(self):
        response = self.client.get("/api/v1/courses/?source=coingecko")
        assert response.status_code == 200

    @task
    def get_courses_with_pair(self):
        response = self.client.get("/api/v1/courses/?source=binance&pair=BTC_USDT")
        assert response.status_code == 200

    @task
    def get_courses_pair_not_found(self):
        response = self.client.get("/api/v1/courses/?source=binance&pair=INVALID_PAIR")
        assert response.status_code == 200

    @task
    def get_courses_invalid_source(self):
        response = self.client.get("/api/v1/courses/?source=invalid_source")
        assert response.status_code == 200
