import requests 

#Testing Output Successfuly 
body = """
{
  allBooks (name:"Bob_Builder") {
    excerpt
    id
    title
    name
  }
  }
"""
response = requests.get("http://127.0.0.1:8000/graphql",json={"query": body}) 

breakpoint()