from github import Github,GithubException
import requests


def github_uploader(token,repo,title,lang,message,code,branch,content):
    token=Github(token)
    repo=token.get_repo(repo)
    path=f"{title}/code{lang}"
    path_2=f"{title}/readme.md"
    try:
        file=repo.get_contents(path)
      
        print(file)
       
        print("File already exists.")
        repo.update_file(
                path=file.path,
                message=message,
                content=code,
                branch=branch,
                sha=file.sha
            )
        
    except GithubException as e:
        if e.status == 404:
            repo.create_file(
               path=path_2,
               message="Readme uploaded",
               content=content
               
           )
        
            
            repo.create_file(
            path=path,
            message=message,
            content=code,
           
        )
           
         
   
    print("File created successfully")


        
    
    

def show_repo(token):
    token=Github(token)
    user=token.get_user()
    name=user.name.replace(" ","")
    repos=requests.get(f"https://api.github.com/users/{name}/repos")
    repos=repos.json()
    total_length=len(repos)
    datas=[data.get("full_name") for data in repos]
    print(datas)

    
    return {"list":datas}