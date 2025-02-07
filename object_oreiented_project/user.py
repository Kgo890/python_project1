class User:
    def __init__(self, email, name, password, current_job_title):
        self.email = email
        self.name = name
        self.password = password
        self.current_job_title = current_job_title

    def change_password(self, new_password):
        self.password = new_password

    def change_job_title(self, new_job):
        self.current_job_title = new_job

    def user_information(self):
        print(f"The user {self.name} currently works at {self.current_job_title} and you can contract them at {self.email}")


user_one = User("gorekaden501@gmail.com", "Kaden Gore", "kad4", "college")

