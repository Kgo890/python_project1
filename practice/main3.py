import requests


response = requests.get("https://gitlab.com/api/v4/:user_id/projects")
my_project = response.json()

for project in my_project:
    print(f"Project Name {project['name']}\nProject Url: {project['web_url']}\n")