from lib.JiraAPI import JiraAPI
from lib.jira_cloud_example import H1Issues
import os
from datetime import datetime
import re
from urllib import parse
from config import config
import pickle
from pprint import pprint


def load_all_results():
    start_at=0
    results = list()
    cur_results = 0
    total = 0
    while True:
        filter = 'project = "Information Security" and issuetype = "Баг"' #FIX IT: Jira filter, exaple: 'project = "Cats" and issuetype = "Баг"'
        response = JiraAPI.get_request('rest/api/3/search?jql=' + filter + '&startAt={}'.format(start_at) +  "&maxResults=100")
        obj_h1 = H1Issues(response.json())
        json_results = response.json()
        total = json_results['total']
        start_at = start_at + json_results['maxResults']
        results_count = len(json_results['issues'])
        if total <= results_count:
            return obj_h1.results
        results.extend(obj_h1.results)
        cur_results += 100
        if cur_results > total:
            return results




def load_data():
    pkl_path = 'cache.pkl'
    if os.environ.get('use_pickle_cache'):
        config['use_pickle_cache'] = (os.environ.get('use_pickle_cache') == 'True')
    if os.environ.get('save_to_pickle_cache'):
        config['save_to_pickle_cache'] = (os.environ.get('save_to_pickle_cache') == 'True')

    if config['use_pickle_cache'] and os.path.exists(pkl_path):
        print('[x] use pickle cache')
        with open(pkl_path,'rb') as f:
            result = pickle.load(f)
    else:
        obj_h1=load_all_results()
        result = _normolize_data(obj_h1)

    if config['save_to_pickle_cache'] and (config['use_pickle_cache'] is False or (config['use_pickle_cache'] is True and os.path.exists(pkl_path) is False) ):
        with open(pkl_path,'wb') as f:
            pickle.dump(result,f)

    return result

#приведение к универсальному формату
def _normolize_data(issues):
    results = list()
    business_criticality = config['business_criticality']
    project_list = list(business_criticality.keys())
    project_list.remove('example.ru')
    no_severity_list = []
    for issue in issues:
        #build target url
        project = 'None'
        if issue['target_url'] is not None:
            url = parse.urlparse(issue['target_url'])
            if url.netloc == 'example.ru':
                if url.path[:10] == '/cms/':
                    project = 'example.ru/cms/'
            if url.netloc != '':
                project = url.netloc
        if issue['target'] is not None and len(issue['target']) > 0:
            project = issue['target'][0]

        project = project.replace('https://', '')
        project = project.replace('http://', '')
        if project[-1] == '/':
            project = project[:-1]

        for pr in project_list:
            if pr in project:
                project = pr
                break
        if project.startswith('192.') or project.startswith('172.') or project.startswith('10'):
            project = 'infra'





        #fix severity
        if isinstance(issue['severity'], dict):
            issue['severity'] = issue['severity']['value']
        else:
            issue['severity'] = 'Medium'
            no_severity_list.append(issue["key"])
        if issue['bug_count']:
            bug_count = int(issue['bug_count'])
        else:
            bug_count = 1
        for times in range(bug_count):
            results.append(dict(state=issue['state'],
                           start_date=datetime.strptime(issue['created'].split('.')[0], '%Y-%m-%dT%H:%M:%S'),
                           end_date=datetime.strptime(issue['finished'].split('.')[0], '%Y-%m-%dT%H:%M:%S'),
                           severity=issue['severity'],
                           project=project,
                           title=issue['key'],
                           labels=issue['vuln_type'],
                           target_url=issue['target_url']
                          ))

    no_bus_crit = set()
    print(f'[x] Issues without severity: {"".join(no_severity_list)}')

    for result in results:
        if result['project'] in business_criticality:
            result['business_criticality'] = business_criticality[result['project']]
        else:
            result['business_criticality'] = 3
            no_bus_crit.add(result['project'])
            result['project'] = 'Не классифицировано'

    print('[x] Список сервисов без оценки бизнес критичности:')
    print('    ', end='')
    print(', '.join(no_bus_crit))


    return results