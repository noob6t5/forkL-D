#!/usr/bin/env python3

import os
import requests
import argparse

GITHUB_API_URL = "https://api.github.com"
CONFIG_FILE = "config.txt"


def load_credentials():
    """
    Load GitHub token and username from the config file.
    If the file is missing or empty, prompt the user to edit it.
    """
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            f.write("# Enter your GitHub token and username below (one per line):\n")
            f.write("# Line 1: GitHub token\n")
            f.write("# Line 2: GitHub username\n")
        print(
            f"Config file '{CONFIG_FILE}' created. Please edit it and add your GitHub token and username."
        )
        exit(1)

    with open(CONFIG_FILE, "r") as f:
        lines = [line.strip() for line in f if not line.strip().startswith("#")]

    if len(lines) < 2 or not lines[0] or not lines[1]:
        print(
            f"Config file '{CONFIG_FILE}' is incomplete. Please edit it and add your GitHub token and username."
        )
        exit(1)

    return lines[0], lines[1]


# Load credentials from the config file
GITHUB_TOKEN, USERNAME = load_credentials()


def get_all_repos():
    """
    Retrieve a list of all repositories (public, private, and forked) for the authenticated user.
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
            repos.extend(repos_batch)
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
    Display a numbered list of all repositories for selection.
    Indicate whether each repository is private, public, or forked.
    """
    print("\nRepositories:\n")
    for idx, repo in enumerate(repos, start=1):
        privacy = "Private" if repo.get("private") else "Public"
        forked = " (Forked)" if repo.get("fork") else ""
        print(f"  {idx}. {repo['full_name']} ({privacy}{forked})")
    print()


def main():
    parser = argparse.ArgumentParser(description="List and delete GitHub repositories.")
    parser.add_argument(
        "-r", "--remove", help="Delete selected repositories by index (e.g., -r 1,2,3)"
    )
    args = parser.parse_args()

    # Fetch all repositories
    repos = get_all_repos()

    if not repos:
        print("No repositories found.")
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

            repos = get_all_repos()  # New list of repositories
            if repos:
                print("Remaining Repositories:\n")
                show_repos(repos)
            else:
                print("All repositories have been deleted.")

        except ValueError:
            print(
                "Invalid input for deletion. Please use comma-separated indices (e.g., -r 1,2,3)."
            )

    else:
        # No option provided, prompt user to select repositories interactively
        show_repos(repos)
        try:
            selected_indices = input(
                "Enter the indices of repositories to delete (comma-separated): "
            )
            indices = [int(i.strip()) - 1 for i in selected_indices.split(",")]
            print("\nDeleting Selected Repositories:\n")
            deletion_count = 0
            for index in indices:
                if 0 <= index < len(repos):
                    if delete_repo(repos[index]["full_name"]):
                        deletion_count += 1
                else:
                    print(f"  ⚠️  Invalid index: {index + 1}")

            print(f"\nDeletion Completed: {deletion_count} repository(ies) deleted.\n")

            repos = get_all_repos()  # New list of repositories
            if repos:
                print("Remaining Repositories:\n")
                show_repos(repos)
            else:
                print("All repositories have been deleted.")

        except ValueError:
            print("Invalid input. Please enter comma-separated indices (e.g., 1,2,3).")


if __name__ == "__main__":
    main()
