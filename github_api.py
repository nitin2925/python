import requests

response = requests.get("https://api.github.com/repos/kubernetes/kubernetes/pulls")

complete_detail = response.json()

pr_list = {}

for i in complete_detail:
    list = i["user"]["login"]
    pr_list[list] += 1 
    print(list)


