import requests
from database import MongoDB
from sys import argv
import json

def check_pull_requests(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_name}/pulls"
    response = requests.get(url)
    if response.status_code == 200:
        with open('bots/AvailableQuests.json', 'r') as file:
            quests = json.load(file)
        pull_requests = response.json()
        for pr in pull_requests:
            print(f"User has successfully submitted a pull request")
        db = MongoDB()
        user_data = db.download_user_data(repo_owner)
        # TODO: add points to the system
        user_data['user_data']['xp'] += quests['first_PR']['xp']
        user_data['user_data']['accepted'].remove('first_PR')
        if user_data['user_data'].get('completed') is not None:
            user_data['user_data']['completed'] += ['first_PR']
        else:
            user_data['user_data']['completed'] = ['first_PR']
        db.update_data(user_data)
    else:
        print("Failed to fetch pull requests")


if __name__ == '__main__':
    repository_owner = argv[1]
    repository_name = argv[2]
    check_pull_requests(repository_owner, repository_name)
