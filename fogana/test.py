for item in tasks:
    if str(item['assignee'])==str(asana_user):
        for task in item['task']:
            if task['name']==title and task['notes']==description:
                print task