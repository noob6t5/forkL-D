#!/usr/bin/env python3

import requests
import argparse


# Replace with your GitHub token and username
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
USERNAME = "YOUR_GITHUB_USERNAME"
GITHUB_API_URL = "https://api.github.com"


def get_forked_repos():
    """
    Retrieve a list of forked repositories for the authenticated user.
    Only includes repositories where `fork` is True.
    """
    url = f"{GITHUB_API_URL}/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    params = {"type": "all", "per_page": 100}
    repos = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={**params, "page": page})

        if response.status_code == 200:
            repos_batch = response.json()
            forked_repos = [repo for repo in repos_batch if repo.get("fork")]
            repos.extend(forked_repos)
            if len(repos_batch) < 100:
                break
            page += 1
        else:
            print(f"Error retrieving repositories: {response.status_code}")
            return []

    return repos


def delete_repo(repo_full_name):
    """
    Delete a repository by its full name (e.g., 'username/repo_name').
    """
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"  ✔️  Deleted: {repo_full_name}")
        return True
    else:
        print(
            f"  ❌  Failed to delete {repo_full_name}. Status code: {response.status_code}"
        )
        return False


def show_repos(repos):
    """
    Display a numbered list of forked repositories for selection.
    """
    print("\nForked Repositories:\n")
    for idx, repo in enumerate(repos, start=1):
        print(f"  {idx}. {repo['full_name']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="List and delete forked GitHub repositories."
    )
    parser.add_argument(
        "-r", "--remove", help="Delete selected repositories by index (e.g., -r 1,2,3)"
    )
    args = parser.parse_args()

    # Fetch forked repositories
    repos = get_forked_repos()

    if not repos:
        print("No forked repositories found.")
        return

    if args.remove:
        # If remove option is used, delete selected repositories
        try:
            print("\nDeleting Selected Repositories:\n")
            indices = [int(i.strip()) - 1 for i in args.remove.split(",")]
            deletion_count = 0
            for index in indices:
                if 0 <= index < len(repos):
                    if delete_repo(repos[index]["full_name"]):
                        deletion_count += 1
                else:
                    print(f"  ⚠️  Invalid index: {index + 1}")

            print(f"\nDeletion Completed: {deletion_count} repository(ies) deleted.\n")

            repos = get_forked_repos()  # New list of forked repos
            if repos:
                print("Remaining Forked Repositories:\n")
                show_repos(repos)
            else:
                print("All forked repositories have been deleted.")

        except ValueError:
            print(
                "Invalid input for deletion. Please use comma-separated indices (e.g., -r 1,2,3)."
            )

    else:
        # No option = repo
        show_repos(repos)


if __name__ == "__main__":
    main()
