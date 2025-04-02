from django.test import TestCase

# Create your tests here.
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
       questionFrontendId
      title
      titleSlug
      content
    }
  }
}

payload={
                "query":query,
                "variables":{"submissionId":values['id']}
                
                
            }
        
            extra_submission=fetch_data(url=url_details,headers=headers,payload=payload,type="post")