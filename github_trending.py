import json
import requests
import datetime


def get_trending_repositories(top_size):
    trending_repositories = []
    request = "https://api.github.com/search/repositories?q=+created:>{}&sort=star"
    today = datetime.datetime.today()
    week_ago_date = today - datetime.timedelta(days=7)
    request_repo = requests.get(request.format(
        week_ago_date.strftime("%Y-%m-%d")))
    repos_dict = request_repo.json()
    for repository_info in range(top_size):
        repo_owner = repos_dict['items'][repository_info]['owner']['login']
        repo_name = repos_dict['items'][repository_info]['name']
        star_count = repos_dict['items'][repository_info]['stargazers_count']
        open_issues_amount = get_open_issues_amount(repo_owner, repo_name)
        open_issues_urls = get_open_issues_urls(repo_owner, repo_name)
        trending_repositories.append([
            repo_owner, repo_name, star_count,
            open_issues_amount, open_issues_urls])
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
    request = "https://api.github.com/repos/{}/{}/issues"
    open_issues_response = requests.get(request.format(repo_owner, repo_name))
    open_issues_list = open_issues_response.json()
    return open_issues_list


def print_trending_repositories(trending_repositories):
    print("Топ 20 репозиториев:\n")
    for repo in trending_repositories:
        (repo_owner, repo_name, star_count,
            open_issues_amount, open_issues_urls) = repo
        print("{} / {}".format(repo_owner, repo_name))
        print("Stars: {}".format(star_count))
        if open_issues_amount > 0:
            print("Open issues {} with urls {}".format(
                open_issues_amount, ", ".join(open_issues_urls)))


if __name__ == "__main__":
    trending_repositories = get_trending_repositories(20)
    print_trending_repositories(trending_repositories)
