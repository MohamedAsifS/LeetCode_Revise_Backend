from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount,SocialToken,SocialApp
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from github import Github
import time
import json
import requests
from .Github_upload import show_repo,github_uploader

from .fetching_leetcode_data import header,time_difference,fetch_data

values={}
# Create your views here.
@login_required
def HandleGithubCallback(request):
    
    user=request.user
   
    social_account=SocialAccount.objects.filter(user=user).first()
    if not social_account:
       return  redirect(f'https://jgaocgbidphajniogibgjdeleaiocpoh.chromiumapp.org/?error=NoSocialAccount')
    token=SocialToken.objects.filter(account=social_account,account__provider='github').first()
    if token:
        get_refresh=RefreshToken.for_user(user)
        print(get_refresh)
        get_access=get_refresh.access_token
        print(get_access)
        return redirect(f'https://jgaocgbidphajniogibgjdeleaiocpoh.chromiumapp.org/?access={get_access}&refresh={get_refresh}')
    else:
        return redirect("https://jgaocgbidphajniogibgjdeleaiocpoh.chromiumapp.org/?error=NoAccessToken")

class submit_to_github(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated] 
  def post(self,request):
      print(request.user)
      
     
      
      url_details="https://leetcode.com/graphql"
      url_for_code="https://leetcode.com/api/submissions/?limit=1"
    
      headers=header(request.body)
      repo=json.loads(request.body)['repo_path']
      print(repo)
      languages = {
  "C": '.c',
  'C++': '.cpp',
  'C#': '.cs',
  "Bash": '.sh',
  "Dart": '.dart',
  "Elixir": '.ex',
  "Erlang": '.erl',
  "Go": '.go',
  "Java": '.java',
  "JavaScript": '.js',
  "Javascript": '.js',
  "Kotlin": '.kt',
  "MySQL": '.sql',
  'MS SQL Server': '.sql',
  "Oracle": '.sql',
  "PHP": '.php',
  "Pandas": '.py',
  "PostgreSQL": '.sql',
  "Python": '.py',
  "Python3": '.py',
  "Racket": '.rkt',
  "Ruby": '.rb',
  "Rust": '.rs',
  "Scala": '.scala',
  "Swift": '.swift',
  "TypeScript": '.ts',
}

      
   
   
   
    
      time.sleep(2)
      check_accepted_and_code=fetch_data(url=url_for_code,headers=headers,type='get')
      if(check_accepted_and_code):
        data=check_accepted_and_code['submissions_dump'][0]
        values={
            "timestamp":data['timestamp'],
            "status_display":data['status_display'],
            "title":data['title'],
            "runtime":data['runtime'],
            "memory":data['memory'],
            "code":data['code'],
            "id":data['id'],
            "lang":data['lang'],
            "question_id":data['question_id'],
            
            
        }
        # print(values)
      if values["status_display"]=='Accepted':
            
            query="""
            query submissionDetail($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    id
    statusCode
    runtime
    memory
    runtimeDisplay
    memoryDisplay
    timestamp
    code
 
    runtimePercentile
    memoryPercentile
    question {
      title
      titleSlug
      content
    }
  }
}

            """
            print(type(values['id']),type(int(values['id'])),values['id'])
            payload={
                "query":query,
                "variables":{"submissionId":values['id']}
                
                
            }
        
            extra_submission=fetch_data(url=url_details,headers=headers,payload=payload,type="post")
            if(extra_submission):
              print(extra_submission)
              SocialAccounts=SocialAccount.objects.filter(user=request.user).first()
              if SocialAccounts:
                  token=SocialToken.objects.filter(account=SocialAccounts,account__provider='github').first().token
                  print(token,repo)
                  message=f"Runs in {extra_submission['data']['submissionDetails']['runtimeDisplay']} using {extra_submission['data']['submissionDetails']['memoryDisplay']}, beating {round(extra_submission['data']['submissionDetails'][ 'runtimePercentile'])}% in speed. - LeetRevise "
                  content=f"{extra_submission['data']['submissionDetails']['question']['title']} {extra_submission['data']['submissionDetails']['question']['content']}"
                  print(content)
                  res=github_uploader(token=token,repo=repo,title=f"{values["question_id"]}-{values["title"]}",lang=languages[values["lang"].capitalize()],message=message,code=values["code"],branch="main",content=content)
                  # github_uploader(token,repo,values['title'],"py","please","print('Asifars')","main")

                  # print(res)
                  print(values["lang"],languages['python3'.capitalize()])
                  
                  print(message,res)
                 
                
               
            else:
                print(False)
    
  
   
    
 
        
    
       
         
                  
    
      return JsonResponse({"message":"success"})
        
        
        
    
    
class list_repo(generics.ListAPIView):
  authentication_classes=[JWTAuthentication]
  permission_classes=[IsAuthenticated]
  def get(self, request, *args, **kwargs):
       user=request.user
       print(user)
  
  
       SocialAccounts=SocialAccount.objects.filter(user=user).first()
       print(SocialAccounts)
       if SocialAccounts:
             token=SocialToken.objects.filter(account=SocialAccounts,account__provider='github').first().token
             
             data=show_repo(token)
             print(data)
             return JsonResponse(data)
       else:
            return JsonResponse({"message":"Account is not linked with GITHUB"},status=401)
  
  #  print(token)
  #  repo=Github(token)
  #  user=repo.get_user()
  #  repos=user.get_repos()
  #  print(repos,type(repos))
  #  repo_select=repo.get_repo("MohamedAsifS/Test_code")
  #  print(repo_select)
  #  create=repo_select.create_file(
  #    path="Asif/readme.md",
  #    message="this is first",
  #     content="# folder1\n\nThis folder contains myfile.txt and more.",
  #      branch="main"
      
  #  )
  
    
   
  
  
  
       return JsonResponse({"message":"nope"})
  
  
  
@csrf_exempt
def show_profile(request):
  print(request.body)
  headers=header(request.body)
  request.session['values']=headers
  print(request.session.get('values'),"here")
  url_details="https://leetcode.com/graphql"
  query="""
  query {
  user {
    username
  } 

}
    """
  payload = {
    "query": query,
    "variables": {}   
}
  username=fetch_data(url=url_details,headers=headers,payload=payload,type="post")
  username=username['data']['user']['username']
  query="""
                query combinedQuery($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
     
    
      countryName
      userAvatar
     
      ranking
    }
    submitStats {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
  
}
                """
  payload={
                    "query":query,
                    "variables":{"username":username}
                }
                
  user_data=fetch_data(url=url_details,headers=headers,type="post",payload=payload)
  if(user_data):
                    print(type(user_data),user_data)
                    send={
                      "usernmae":user_data['data']['matchedUser']['username'],
                      "avatar":user_data['data']['matchedUser']['profile']['userAvatar'],
                      "country":user_data['data']['matchedUser']['profile']['countryName'],
                      "ranking":user_data['data']['matchedUser']['profile']['ranking'],
                      "submission":user_data['data']['matchedUser']['submitStats']['acSubmissionNum'][1:],
                      "status":True
                    }
                   
                    request.session["User"]=user_data
  else:
                    print(False)
  return JsonResponse(send)



