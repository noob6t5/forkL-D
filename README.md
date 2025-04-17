## forkL-D
 **ForkL-D** is a simple Python script to list and delete  repositories directly from your terminal. Customize it to your needs, or contribute via PRs to expand its functionality!

# Insp
 I don't use other **GH** tool and Have ton's of forked repo Deleting them would be hassle . So, I created this By which u can guess   `Why I haven't improved this too much....`

## Features

- List All Repositories(Public,Forked,Private): Quickly see all your forked repositories with a numbered list.
- Bulk Delete Forked Repositories: Specify indices to delete multiple repositories at once.
- Clear, Minimal Output: After deletion, the updated list of remaining forked repositories is shown.


## Requirements

- Python 3.x
- requests library: Install with `pip install requests`
- GitHub Personal Access Token (PAT) with **Delete and Repo** Permission Enabled

## Usage

1. **Clone the Repository**
  First,clone the Repo:
```
git clone https://github.com/noob6t5/forkL-D.git
cd forkL-D
```
2. **Configure Your GitHub Credentials**:
  
 Open `config.txt` in a text editor and add your GitHub username and personal access token (PAT).
 
# Inside config.txt without "" in separate line
```
"YOUR_GITHUB_TOKEN"
"YOUR_GITHUB_USERNAME"
```
Note: Replace YOUR_GITHUB_TOKEN with your actual token and YOUR_GITHUB_USERNAME with your GitHub username.

3. **Run ForkL-D**:

`python3 forklide.py`

This command will display a numbered list of all your forked repositories.

4. **Use it from Anywhere in Terminal** or use can make alises (Much faster)

```
chmod +x forklide.py
sudo ln -sf $(pwd)/forklide.py /usr/local/bin/forklide
```
**Ensure it's running by hitting `forklide` in terminal**

# Delete Specific Forked Repositories

To delete specific repositories, use the -r option followed by the indices of the repositories you want to remove, `separated by commas`.

`forklide -r 1,3,5`



