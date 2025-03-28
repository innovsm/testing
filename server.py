
from mcp.server.fastmcp import FastMCP
import requests
from secrets_1 import get_github_token, get_user
import pandas as pd
import base64

# creating mcp server
mcp = FastMCP("Github App")

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = get_github_token()
USER = get_user()


HEADERS = {
     "Authorization": f"Bearer {GITHUB_TOKEN}",
     "Accept": "application/vnd.github.v3+json"
 }
 
 
 # =============================  MAIN FUNCTIONS ================================
 
 
@mcp.tool(name = "user_details" , description="gives user information")  # in name space cannot be user
def get_user_details(username: str):
     url = f"{GITHUB_API_URL}/users/{username}"
     response = requests.get(url, headers=HEADERS)
     if response.status_code != 200:
         return "errror"
     return response.json()
 
@mcp.tool(name = "repository_list", description="this provides all the repositories metadata")
 
 # this functions fetches the  repo metadata and saves it in local storage
def list_repositories():  # bad coding practice
 
     url = f"{GITHUB_API_URL}/user/repos"
     response = requests.get(url, headers=HEADERS)
 
     # making a dataframe and saving it 
     data_1 = pd.DataFrame(response.json())
     data_1.to_csv("repo_list.csv")
     
     if response.status_code != 200:
         return "not worked"
     return data_1['name'].to_json()  # this will return all the name of the repos user have
 
 
 
 # fetch repo 
@mcp.tool(name = "fetch_repo", description = "this function is used to fetch repositories data")
def get_repo_data(repo_name: str):
     url = f"{GITHUB_API_URL}/repos/{USER}/{repo_name}/contents"
     # fecting data
     response = requests.get(url, headers=HEADERS)
     if response.status_code!= 200:
         return "not worked"
     return response.json()    # this code is in testing phase
 
 
@mcp.tool(name = "download-data", description = "It will download any specific content of repo")
 
def download_file(url):
     response = requests.get(url, headers=HEADERS)
     if response.status_code!= 200:
         return "not worked"
     else:
         # saving to local directory
         return response.content 
 
 
 # creating function to upload the data 
@mcp.tool(name = "modify_upload", description= "This Function is used for modifying the existing code")
 # --------------------------- LAST AND MOST IMPORTANT FUNCTION -------------------------------------# unstable function 
def push_file_to_github(owner: str, repo : str,sha : str,  path : str, code_content : str, commit_message : str):
     token = GITHUB_TOKEN  # user token
     try:
         # Read and encode the file to Base64
         content = base64.b64encode(code_content.encode('utf-8')).decode('utf-8')  # basic encoding
         if sha is None:
             print("Failed to get file SHA")
             return
 
         # Create payload
         data = {
             "message": commit_message,
             "content": content,
             "sha": sha
         }
 
         # Push using API
         url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
         headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
 
         response = requests.put(url, json=data, headers=headers)
 
         if response.status_code == 200 or response.status_code == 201:
             return "Success"
         else:
             return "Failure"
     except Exception as e: 
         return e  # returning the main error
 
 
@mcp.tool(name ="fetch_public_repo", description="it is used to fetch public repositories")
def get_repo_data(repo_name: str):
     
     url = f"{GITHUB_API_URL}/repos/{repo_name}/contents"
     # fecting data
     response = requests.get(url, headers=HEADERS)
     if response.status_code!= 200:
         return "not worked"
     return response.json()    # this code is in testing phase
 
 
 
@mcp.tool(name = "download_public_files", description="it is used to download data from public repositories")
 
def download_file(url):
     response = requests.get(url, headers=HEADERS)
     if response.status_code!= 200:
         return "not worked"
     else:
         # saving to local directory
         return response.content
 
if __name__ == "__main__":
    mcp.run(transport="stdio")

