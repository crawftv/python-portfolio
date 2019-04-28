import firebase_admin
from firebase_admin import credentials
from decouple import config
from firebase_admin import firestore
import requests
cred = credentials.Certificate(config("FIRESTORE_JSON"))
firebase_admin.initialize_app(cred,{
    'projectID' : 'porftfolio-a7d76' 
    })

db = firestore.client()

def get_medium(db):
    docs = db.collection('medium-stories').get()
    blog_list = [ doc.to_dict() for doc in docs]
    return blog_list

def update_github_events(page_num):
    r = requests.get('https://api.github.com/users/'+config("GITHUB_USERNAME")+
            '/events?page='+str(page_num))
    query = r.json()
    for q in query:
        data = { u'gheID': q['id'], u'gheTime': q['created_at'][0:10] }
        db.collection(u'github-events').document(q['id']).set(data)
def get_github_events(db):
    github_events = db.collection('github-events').get()
    github_events = [ event.ghetime for event in github_events ]
    return github_events
