from flask import json
import firebase_admin
from firebase_admin import credentials
from decouple import config
from firebase_admin import firestore
import requests
import itertools
import re
cred = credentials.Certificate(config("FIRESTORE_JSON"))
firebase_admin.initialize_app(cred,{
    'projectID' : 'porftfolio-a7d76' 
    })

db = firestore.client()

def get_medium(db):
    docs = db.collection('medium-stories').order_by(u'publish_num',
            direction=firestore.Query.DESCENDING).get()
    blog_list = [ doc.to_dict() for doc in docs]
    return blog_list

def update_github_events(db, page_num):
    r = requests.get('https://api.github.com/users/'+config("GITHUB_USERNAME")+
            '/events?page='+str(page_num))
    query = r.json()
    for q in query:
        data = { u'gheID': q['id'], u'gheTime': q['created_at'][0:10] }
        db.collection(u'github-events').document(q['id']).set(data)

def get_github_events(db):
    github_events = db.collection('github-events').get()
    github_events = [ event.to_dict() for event in github_events ]
    github_events = [ (key, list(num for _, num in value)) for key, value in
            itertools.groupby(github_events, lambda x:x['gheTime']) ]
    labels = [ github_events[i][0] for i in range(len(github_events)) ]
    data   = [ len(github_events[i][1]) for i in range(len(github_events)) ]
    labels = json.dumps(labels)
    data = json.dumps(data)
    return labels, data

def update_repos(db,page_num):
    r = requests.get('https://api.github.com/users/'+config("GITHUB_USERNAME")+"/repos?page="+str(page_num))
    query = r.json()
    for q in query:
        data = {u'repo_name':q['name'], u'repo_id':q["id"] }
        db.collection(u'git-repos').document(str(q['name'])).set(data)

def update_repo_files(db):
    repos = db.collection('git-repos').get()
    repos = [ repo.to_dict() for repo in repos ]
    for repo in repos:
        sha = requests.get('https://api.github.com/repos/'+config("GITHUB_USERNAME")+"/"+repo["repo_name"]+"/commits")
        sha = sha.json()[0]["sha"]
        try:
            tree = requests.get('https://api.github.com/repos/'+config("GITHUB_USERNAME")+"/"+repo["repo_name"]+
                        '/git/trees/'+sha+'?recursive=1').json()

            tree = [ t["path"] for t in tree["tree"] ]
            tree = check_file_type(tree)
            db.collection(u'git-repos').document(str(repo["repo_name"])).set({u'tree': tree }, merge=True)
        except:
            pass

#UTILITU FUNCTIONS BELOW
def check_file_type(list_string):
    new_list = []
    for s in list_string:
        if re.match(r'^.*(node_modules|solutions)\\',s):
            pass
        elif re.match(r'^.*\.(py|js|jl|elm|ipynb|html)',s):
            new_list.append(s)
    return new_list
