from github import Github,GithubException



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
            path=path,
            message=message,
            content=code,
           
        )
           repo.create_file(
               path=path_2,
               message="Readme uploaded",
               content=content
               
           )
        
         
   
    print("File created successfully")


        
    
    

def show_repo(token):
    token=Github(token)
    user=token.get_user()
    repos=user.get_repos()
    data=[data.raw_data.get('full_name') for data in repos]
    
    return {"list":data}
