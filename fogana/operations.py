import initialize
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
# people={"Asana": [{"id": 2396135081835, "name": "Karthik Kailash"}, {"id": 2341964888557, "name": "Todd Johnson"}, {"id": 2273084124532, "name": "Tapan Dhimant"}, {"id": 2396135081819, "name": "Dave Harrison"}, {"id": 437497778178, "name": "Chris Jantz-Sell"}, {"id": 7751245150480, "name": "Adam Gomaa"}, {"id": 2606278855495, "name": "Aden Zaman"}, {"id": 4306440740950, "name": "Allen Schober"}, {"id": 1148825222700, "name": "Alvir Navin"}, {"id": 5370792369686, "name": "amy"}, {"id": 2651152848265, "name": "Arron Bleasdale"}, {"id": 8158734251361, "name": "Boris Soliz"}, {"id": 5370792369696, "name": "caitlin"}, {"id": 8704910276663, "name": "Greg Cuellar"}, {"id": 5422999117116, "name": "Hong"}, {"id": 2342146911263, "name": "Ignacio Palladino"}, {"id": 6366165217631, "name": "jackson"}, {"id": 7789295658198, "name": "Jennifer Sands"}, {"id": 2396172128269, "name": "John Eversole"}, {"id": 2396172128245, "name": "Joshua Smallman"}, {"id": 7200348412664, "name": "Krzysztof (Maverick)"}, {"id": 2396172128253, "name": "Matt Billenstein"}, {"id": 4196093460412, "name": "Minting Xiao"}, {"id": 2288623384152, "name": "Omar Zennadi"}, {"id": 7200348412654, "name": "Pawel Solyga"}, {"id": 2262647592322, "name": "Test Developer"}]}
with open('/Users/ccxiao/src/gs/fogana/people.json', 'r') as o:
    people=json.load(o)

my_api_key='1bSdSxeQ.E8HYzXlKz8bQjDVnIafTRNE'
token='378m74pjj9g9mdfqs6g4ev6mco28hk'

def map_people_a2f(user):
    for person in people['Asana']:
        if str(person['id'])==str(user):
            first_name=person['name'].split(' ')[0]
            for person1 in people['Fogbugz']:
                if first_name in person1['name']:
                    user_fogbugz_id=person1['id']
                    found=1
                    return user_fogbugz_id
    return 0

def map_people_f2a(user):
    for person in people['Fogbugz']:
        if str(person['id'])==str(user):
            first_name=person['name'].split(' ')[0]
            for person1 in people['Asana']:
                if first_name in person1['name']:
                    user_asana_id=person1['id']
                    found=1
                    return user_asana_id
    return 0

def search_fogbugz():
    # this function searches through all tasks
    # in fogbugz and return those with the magic word
    # in their associated events contents 
    #
    # # change these two lines
    logon_url=logon_minting_fogbugz
    base_url=base_minting_fogbugz
    # logon_url=logon_samba_fogbugz
    # base_url=base_samba_fogbugz
    ixBug=1
    cmd='setCurrentFilter&sFilter=1'
    cols='events,sTitle'
    url=base_url+'cmd=%s&token=%s' % (cmd, token)
    print url
    requests.get(url)
    cmd='search'
    url1=base_url+'cmd=%s&cols=%s&token=%s' % (cmd, cols, token)
    print url1
    r=requests.get(url1)
    text=r.text.encode('utf-8').strip()
    root=ET.fromstring(text)
    magic_w='[create ticket]'
    R=[]
    for cases in root.findall('./cases/*'):
        case_id=cases.attrib['ixBug']
        ticket=False
        for events in cases.findall('./events/*'):
            dt=events.findall('dt')[0] #element indicating time modified
            s=events.findall('s')[0] #element indicating text content of the modification
            print s.text
            dt=dateutil.parser.parse(dt.text).replace(tzinfo=None)
            ps=None
            if (now-dt)>datetime.timedelta(7,0,0):
                print 'too old'
                continue
            try:
                if magic_w in s.text:
                    ticket=True
            except TypeError:
                pass
        for events in cases.findall('./events/*'):
            v=events.findall('sVerb')[0]
            if v.text=='Assigned':
                ps=events.findall('ixPersonAssignedTo')[0].text #element indicating id of the assignee
                break
        if ticket:
            R.append({'assignee':ps, 'case_id':case_id})
        print 'case id? %s create ticket? %s person assigned to? %s' % (case_id, ticket, ps)
    return R

def search_asana():
    # this function searches through all tasks
    # in Asana and return those with the magic word
    # in their associated descriptions and comments
    R=[]
    OJ={'data':[]}
    base_url='https://app.asana.com/api/1.0/'
    workspace_url='https://app.asana.com/api/1.0/workspaces/938725484794/' # workspace "flingo.tv"
    ## people=construct_people_dict_asana()
    starttime=datetime.datetime.now()
    for person in people["Asana"]:
        user=person['id']
        ##for testing
        if not user==4196093460412:
            continue
        url1=os.path.join(workspace_url,'tasks?assignee=%s&opt_fields=name,notes,modified_at,assignee' % user)
        print url1+'\n'
        r=requests.get(url1, auth=HTTPBasicAuth(my_api_key, ''))
        task_data=json.loads((r.text).encode('utf-8').strip())['data']
        OJ['data'].append({'assignee':user, 'task':task_data})
        now=datetime.datetime.now()
        magic_w='[create ticket]'
        for task in task_data:
            try:
                task_id=str(task['id'])
                print task_id
                # url2=os.path.join(base_url,'tasks','%s?opt_fields=name,notes,modified_at' % task_id)
                # r2=requests.get(url2, auth=HTTPBasicAuth(my_api_key, ''))
                # task_info=json.loads((r2.text).encode('utf-8').strip())['data']
                task_mt=task['modified_at']
                mt=dateutil.parser.parse(task_mt).replace(tzinfo=None)
                if (now-mt)>datetime.timedelta(70,0,0):
                    print 'too old'
                    continue
                task_note=task['notes']
                print task_note
                if magic_w in task_note:
                    print magic_w
                    print task_id
                    R.append({'assignee':user, 'task_id':task_id})
                    continue
                url3=os.path.join(base_url,'tasks',task_id, 'stories')
                r3=requests.get(url3, auth=HTTPBasicAuth(my_api_key, ''))
                stories=json.loads((r3.text).encode('utf-8').strip())['data']
                OJ['data'].append({'assignee':user, 'stories':stories})
                for story in stories:
                    if story['type']=='comment':
                        if magic_w in story['text']:
                            print magic_w
                            print task_id
                            R.append({'assignee':user, 'task_id':task_id})
                            continue
            except ValueError:
                print 'error occurred'
                pass
            except TypeError:
                print 'error occurred'
                pass
    endtime=datetime.datetime.now()
    with open(asana_tasks_output, 'w+') as o:
        o.write(json.dumps(OJ,indent=4, separators=(',', ':')))
    print 'time elapsed:'
    print endtime-starttime
    return R

def search_exist_in_asana(asana_user, task_id, title='', description=''):
    # The functionality is
    # check whether an equivalency link is included in a task
    asana_user=str(asana_user)
    task_id=str(task_id)
    base_url='https://app.asana.com/api/1.0/'
    url1=os.path.join(base_url,'tasks', task_id)
    print url1
    r=requests.get(url1, auth=HTTPBasicAuth(my_api_key, ''))
    print r.text
    task_data=json.loads((r.text).encode('utf-8').strip())['data']
    #equivalency link to be put in F cases
    for line in task_data['notes'].split('\n'):
        if 'Equivalency link' in line:
            print line
            return True
    return False

def search_exist_in_fogbugz(case_id, tittle='', description=''):
    # The functionality is
    # check whether an equivalency link is included in a task
    case_id=str(case_id)
    base_url=base_minting_fogbugz
    # logon_url=logon_samba_fogbugz
    # base_url=base_samba_fogbugz
    cmd='setCurrentFilter&sFilter=1'
    url=base_url+'cmd=%s&token=%s' % (cmd, token)
    print url
    requests.get(url)
    cmd='search'
    cols='events,sTitle'
    q=case_id
    url1=base_url+'cmd=%s&q=%s&cols=%s&token=%s' % (cmd, q, cols, token)
    print url1
    r=requests.get(url1)
    text=r.text.encode('utf-8').strip()
    root=ET.fromstring(text)
    case=root.findall('./cases/*')[0]
    title=case.findall('sTitle')[0].text
    found=False
    for event in case.findall('./events/*'):
        verb=event.findall('sVerb')[0].text
        if verb=='Opened':
            descrip=event.findall('s')[0].text
            for line in descrip.split('\n'):
                if 'Equivalency link' in line:
                    print descrip
                    found=True
        if verb=='Assigned':
            assignee=event.findall('ixPersonAssignedTo')[0].text
    return found

def ticket_in_asana_to_case_in_fogbugz(asana_user='4196093460412', task_id='9246471123287'):
    # Given an id of a task in asana
    # CREATE a case in Fogbugz
    # with the link pointing back to this task in Asana
    # in the event content area of Fogbugz
    # 
    # Retrieve information from A
    asana_user=str(asana_user)
    task_id=str(task_id)
    link_back=os.path.join('https://app.asana.com/0',asana_user,task_id)
    print link_back
    ## tentative keys
    base_url='https://app.asana.com/api/1.0/'
    task_url=os.path.join(base_url, 'tasks', task_id)
    print task_url
    r=requests.get(task_url, auth=HTTPBasicAuth(my_api_key, ''), params={"opt_fields":"name,notes"})
    task_info=json.loads((r.text).encode('utf-8').strip())['data']
    print task_info
    task_name=task_info['name']
    task_notes=task_info['notes']
    task_notes+='\nEquivalency link:\n'+link_back
    # Start creating a case in F
    logon_url=logon_minting_fogbugz
    base_url=base_minting_fogbugz
    # logon_url=logon_samba_fogbugz
    # base_url=base_samba_fogbugz
    user=map_people_a2f(asana_user)
    print user
    # create equivalency case in F
    cmd='new'
    data={'sTitle':task_name, 'sEvent':task_notes, 'ixPersonAssignedTo':user}
    print data
    url=base_url+'cmd=%s&token=%s' % (cmd, token)
    print url
    r=requests.post(url, data=data)
    print r.text
    text=r.text.encode('utf-8').strip()
    text=ET.fromstring(text)[0]
    case_id=text.attrib['ixBug']
    # edit task_notes
    link_out=os.path.join('https://minting.fogbugz.com/f/cases/',case_id)
    task_notes1=task_info['notes']
    task_notes1+='\nEquivalency link:\n'+link_out
    data={'notes': task_notes1}
    r=requests.put(task_url, data=data, auth=HTTPBasicAuth(my_api_key, ''))
    return 0

def ticket_in_fogbugz_to_task_in_asana_in_test(fogbugz_user='2', case_id=14):
    # Given an id of a case in fogbugz
    # CREATE a task in Asana
    # with the link pointing back to this task in Asana
    # in the event content area of Fogbugz
    # 
    # Retrieve information from F
    fogbugz_user=str(fogbugz_user)
    case_id=str(case_id)
    link_back=os.path.join('https://minting.fogbugz.com/f/cases/',case_id)
    print link_back
    cmd='search'
    q=case_id
    # 
    # 
    logon_url=logon_minting_fogbugz
    base_url=base_minting_fogbugz
    url=base_url+'cmd=%s&q=%s&token=%s' % (cmd,q,token)
    r=requests.get(url, params={"cols":"sTitle,events"})
    text=r.text.encode('utf-8').strip()
    root=ET.fromstring(text)
    case=root.findall('./cases/*')[0]
    title=case.findall('sTitle')[0].text
    for event in case.findall('./events/*'):
        verb=event.findall('sVerb')[0].text
        if verb=='Opened':
            descrip=event.findall('s')[0].text
        if verb=='Assigned':
            assignee=event.findall('ixPersonAssignedTo')[0].text
    # create equivalent case in A
    last_ixBugEvent=event.attrib['ixBugEvent']
    descrip+='\nEquivalency link:\n%s' % link_back
    asana_user=map_people_f2a(fogbugz_user)
    base_url='https://app.asana.com/api/1.0/'
    workspace_url='https://app.asana.com/api/1.0/workspaces/938725484794/tasks'
    data={'name':title,'assignee':asana_user, 'notes':descrip}
    print data
    r=requests.post(workspace_url, data=data, auth=HTTPBasicAuth(my_api_key, ''))
    # Edit the case description in F
    task_info=json.loads((r.text).encode('utf-8').strip())['data']
    print r.text
    task_id=str(task_info['id'])
    asana_user=str(asana_user)
    link_out=os.path.join('https://app.asana.com/0',asana_user,task_id)
    descrip1='Equivalency link\n'+link_out
    data={'sEvent':descrip1,'ixBugEvent':last_ixBugEvent}
    cmd='edit'
    url=base_minting_fogbugz+'cmd=%s&ixBug=%s&token=%s' % (cmd,case_id,token)
    r=requests.post(url, data=data)
    # return 0

def main():
    token=initialize.token_fogbugz('minting')
    DA=search_asana()
    DF=search_fogbugz()
    print '\n\n'
    # DA Sample result:
    # [{'assignee': 4196093460412, 'task_id': '9128647251522'}, {'assignee': 4196093460412, 'task_id': '9246471123287'}]
    # DF sample result:
    # {'assignee': '2', 'case_id': '6'}]
    for item in DA:
        print item
        asana_user=item['assignee']
        task_id=item['task_id']
        if search_exist_in_asana(asana_user,task_id):
            print 'link exists'
            continue
        else:
            print 'link not found'
            ticket_in_asana_to_case_in_fogbugz(asana_user, task_id)
    for item in DF:
        print item
        case_id=item['case_id']
        fogbugz_user=item['assignee']
        if search_exist_in_fogbugz(case_id):
            print 'link exists'
            continue
        else:
            print 'link not found'
            ticket_in_fogbugz_to_task_in_asana_in_test(fogbugz_user, case_id)







