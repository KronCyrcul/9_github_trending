import json
import requests
import datetime


def get_trending_repositories(top_size, days_ago):
    trending_repositories = []
    request_url = "https://api.github.com/search/repositories"
    today = datetime.datetime.today()
    past_date = today - datetime.timedelta(days=days_ago)
    search_params = {"q": " created:>{}".format(
        past_date.strftime("%Y-%m-%d")),
        "sort": "star"}
    response = requests.get(request_url, params=search_params)
    repos_list = response.json()['items']
    for repository in repos_list[:top_size]:
        trending_repositories.append(repository)
    return trending_repositories


def get_trending_repositories_info(trending_repositories):
    trending_repositories_info = []
    for repo in trending_repositories:
        repo_owner = repo['owner']['login']
        repo_name = repo['name']
        star_count = repo['stargazers_count']
        open_issues_list = get_open_issues_list(repo_owner, repo_name)
        open_issues_amount = len(open_issues_list)
        open_issues_urls = [issue["url"] for issue in open_issues_list
            if len(open_issues_list) > 0]
        trending_repositories_info.append([repo_owner, repo_name, star_count,
            open_issues_amount, open_issues_urls])
    return (trending_repositories_info)


def get_open_issues_list(repo_owner, repo_name):
    request_url = "https://api.github.com/repos/{}/{}/issues"
    open_issues_response = requests.get(request_url.format(
        repo_owner, repo_name))
    open_issues_list = open_issues_response.json()
    return open_issues_list


def print_trending_repositories(trending_repositories_info):
    print("Топ 20 репозиториев:")
    for repo in trending_repositories_info:
        repo_owner = repo[0]
        repo_name = repo[1]
        star_count = repo[2]
        open_issues_amount = repo[3]
        open_issues_urls = repo[4]
        print("{} / {}".format(repo_owner, repo_name))
        print("Stars: {}".format(star_count))
        if open_issues_amount > 0:
            print("Open issues {} with urls {}".format(
                open_issues_amount, ", ".join(open_issues_urls)))


if __name__ == "__main__":
    top_size = 20
    days_ago = 7
    trending_repositories = get_trending_repositories(top_size, days_ago)
    trending_repositories_info = get_trending_repositories_info(
        trending_repositories)
    print_trending_repositories(trending_repositories_info)
