from user import User
from post import Post

user_one = User("gorekaden501@gmail.com", "kaden", "kad3", "engineer")
user_one.user_information()

user_two = User("stevesmith@gmail.com", "steve", "stev3", "doctor")
user_two.user_information()

user_one_post = Post("that game was fucking horrible", user_one.name)
user_one_post.post_information()
