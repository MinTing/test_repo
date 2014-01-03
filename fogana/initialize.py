import os
import requests
import datetime
import dateutil.parser
import xml.etree.ElementTree as ET
import json
import base64

from requests.auth import HTTPBasicAuth

logon_minting_fogbugz='https://minting.fogbugz.com/api.asp?cmd=logon&email=xmt1216@gmail.com&password=fogbugzminting'
logon_samba_fogbugz='https://samba-tv.fogbugz.com/api.asp?cmd=logon&email=minting@samba.tv&password=fogbugzminting'
base_minting_fogbugz='https://minting.fogbugz.com/api.asp?'
base_samba_fogbugz='https://samba-tv.fogbugz.com/api.asp?'
now=datetime.datetime.now()
OJ=dict({})

asana_tasks_output='/Users/ccxiao/src/gs/fogana/asana_tasks.json'
fogbugz_cases_output='/Users/ccxiao/src/gs/fogana/fogbugz_cases.json'

def token_fogbugz(domain='minting'):
    token=''
    print domain=='minting'
    if domain=='minting':
        logon_url=logon_minting_fogbugz
        base_url=base_minting_fogbugz
    if domain=='samba':
        logon_url=logon_samba_fogbugz
        base_url=base_samba_fogbugz
    r=requests.get(logon_url)
    root=ET.fromstring(r.text)
    print root
    # get token
    for child in root.iter():
        print child.text
        if child.tag=='token':
            token=child.text
    return token

def construct_people_dict_fogbugz():
    url='https://samba-tv.fogbugz.com/api.asp?cmd=listPeople&token=%s' % (token)
    r=requests.get(url)
    text=r.text.encode('utf-8').strip()
    root=ET.fromstring(text)
    infile='/Users/ccxiao/Fogana/people_fogbugz.xml'
    outfile='/Users/ccxiao/Fogana/people.json'
    List=[]
    for person in root.findall('./people/*'):
        person_id=person.findall('./ixPerson')[0].text
        person_name=person.findall('./sFullName')[0].text
        List.append({'id':person_id, 'name':person_name})
    D=json.dumps({'fogbugz': List})
    return D

def construct_people_dict_asana():
    base_url='https://app.asana.com/api/1.0/'
    home_url=os.path.join(base_url, 'users', 'me')
    # res=requests.get(home_url, auth=HTTPBasicAuth(my_api_key, ''))
    users=os.path.join(base_url, 'users')
    r=requests.get(users, auth=HTTPBasicAuth(my_api_key, ''))
    j=json.loads(r.text)
    D=json.dumps({'Asana': j['data']})
    return D

    # for person in people["Asana"]:
    #     user=person['id']
    #     for task in task_data:
    #         try:
    #             task_id=str(task['id'])
    #             print task_id
    #             # url2=os.path.join(base_url,'tasks','%s?opt_fields=name,notes,modified_at' % task_id)
    #             # r2=requests.get(url2, auth=HTTPBasicAuth(my_api_key, ''))
    #             # task_info=json.loads((r2.text).encode('utf-8').strip())['data']
    #             task_mt=task['modified_at']
    #             mt=dateutil.parser.parse(task_mt).replace(tzinfo=None)
    #             if (now-mt)>datetime.timedelta(7,0,0):
    #                 print 'too old'
    #                 continue
    #             task_note=task['notes']
    #             if magic_w in task_note:
    #                 print magic_w
    #                 print task_id
    #                 R.append({'assignee':user, 'task_id':task_id})
    #                 continue         
    #             url3=os.path.join(base_url,'tasks',task_id, 'stories')
    #             r3=requests.get(url3, auth=HTTPBasicAuth(my_api_key, ''))
    #             stories=json.loads((r3.text).encode('utf-8').strip())['data']
    #             for story in stories:
    #                 if story['type']=='comment':
    #                     if magic_w in story['text']:
    #                         print magic_w
    #                         print task_id
    #                         R.append({'assignee':user, 'task_id':task_id})
    #                         continue
    #         except ValueError:
    #             print 'error occurred'
    #             pass
    #         except TypeError:
    #             print 'error occurred'
    #             pass
