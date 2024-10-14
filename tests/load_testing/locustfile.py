from locust import HttpUser,task, between


class AppUser(HttpUser):
    wait_time = between(2,5)

    def on_start(self):
        """This method is called when a simulated user starts. It will handle login."""
        self.login()

    def login(self):
        # Define the login endpoint and the credentials
        login_data = {
            'email': 'testuser@example.com',  # Replace with actual credentials
            'password': 'password123'         # Replace with actual password
        }
        response = self.client.post('/', data=login_data)

        if response.status_code == 200:
            print("Login successful!")
        else:
            print(f"Login failed with status code {response.status_code}")

    @task
    def home_page(self):
        self.client.get('/')

    @task
    def dashboard(self):
        self.client.get('/dashboard')

    @task 
    def qa_chat(self):
        self.client.get('/chat')

    @task
    def about(self):
        self.client.get('/about')
    
    @task
    def math_solver(self):
        self.client.get('/math_solver')

    @task
    def feedback(self):
        self.client.get('/feedbacks')
    
    @task
    def documentation(self):
        self.client.get('/documentation')
