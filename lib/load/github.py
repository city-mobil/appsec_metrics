from github import Github
from collections import OrderedDict
from config import config
import os
from datetime import datetime

#загрузка данных из github
def load_from_github():
    g = Github(os.environ['github_token'])
    result_issue = list()
    for project, info in config['github_projects'].items():
        repo = g.get_repo(project)
        business_criticality = info['business_criticality']
        tags = info['tags']
        issues = repo.get_issues(labels=tags, state='all')
        issues = _normolize_data(list(issues),repo,business_criticality)
        result_issue.extend(issues)
    result_issue.sort(key=lambda x:x['start_date'])
    return result_issue

#приведение к универсальному формату
def _normolize_data(issues, github_repo,business_criticality):
    def get_severity_by_comments(issue, dc_table):
        for dc_threshold, severity in dc_table:
            if issue.comments >= dc_threshold:
                return severity

    result = []
    for issue in issues:
        #получаем имя проекта
        project = github_repo.full_name.split('/')[1]
        #получаем severity на основе информации о количестве комментариев
        severity = get_severity_by_comments(issue, config['github_severity_list'])

        #если задача находится в статусе open, то в качестве end_date используем текущую на данный день дату
        if issue.state == 'open' or issue.closed_at is None:
            end_date = datetime.now()
        else:
            end_date = issue.closed_at

        result.append(dict( state=issue.state,
                            start_date=issue.created_at,
                            end_date=end_date,
                            severity=severity,
                            project=project,
                            title=issue.title,
                            business_criticality=business_criticality,
                            labelts=issue.labels))


    return result