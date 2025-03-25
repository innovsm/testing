def get_repo_data(repo_name: str):
    
    url = f"{GITHUB_API_URL}/repos/{repo_name}/contents"
    # fecting data
    response = requests.get(url, headers=HEADERS)
    if response.status_code!= 200:
        return "not worked"
    return response.json()    # this code is in testing phase