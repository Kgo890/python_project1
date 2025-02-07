class Post:
    def __init__(self, message, author):
        self.message = message
        self.author = author

    def post_information(self):
        print(f"Post: {self.message} was written by {self.author}")

    def change_post(self, new_message):
        self.message = new_message
