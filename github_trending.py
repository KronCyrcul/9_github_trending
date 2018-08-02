import json
import requests
import datetime


def get_trending_repositories(top_size):
    trending_repositories = []
    request_url = "https://api.github.com/search/repositories"
    today = datetime.datetime.today()
    days_ago = 7
    past_date = today - datetime.timedelta(days=days_ago)
    search_params = {"q": " created:>{}".format(
        past_date.strftime("%Y-%m-%d")),
        "sort": "star"}
    response = requests.get(request_url, params=search_params)
    repos_list = response.json()['items']
    for repository in repos_list[:top_size]:
        trending_repositories.append(repository)
    return trending_repositories


def get_open_issues_amount(repo_owner, repo_name):
    open_issues_list = get_open_issues_list(repo_owner, repo_name)
    return len(open_issues_list)


def get_open_issues_urls(repo_owner, repo_name):
    open_issues_list = get_open_issues_list(repo_owner, repo_name)
    open_issues_urls = [issue["url"] for issue in open_issues_list
        if len(open_issues_list) > 0]
    return open_issues_urls


def get_open_issues_list(repo_owner, repo_name):
    request_url = "https://api.github.com/repos/{}/{}/issues"
    open_issues_response = requests.get(request_url.format(
        repo_owner, repo_name))
    open_issues_list = open_issues_response.json()
    return open_issues_list


def print_trending_repositories(trending_repositories):
    print("Топ 20 репозиториев:")
    for repo in trending_repositories:
        repo_owner = repo['owner']['login']
        repo_name = repo['name']
        star_count = repo['stargazers_count']
        open_issues_amount = get_open_issues_amount(repo_owner, repo_name)
        open_issues_urls = get_open_issues_urls(repo_owner, repo_name)
        print("{} / {}".format(repo_owner, repo_name))
        print("Stars: {}".format(star_count))
        if open_issues_amount > 0:
            print("Open issues {} with urls {}".format(
                open_issues_amount, ", ".join(open_issues_urls)))


if __name__ == "__main__":
    top_size = 20
    trending_repositories = get_trending_repositories(top_size)
    print_trending_repositories(trending_repositories)
