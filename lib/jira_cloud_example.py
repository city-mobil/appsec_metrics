import json
import os
import pytz
from pprint import pprint
from datetime import datetime
from lib.JiraAPI import JiraAPI


class H1Issues:
    def __init__(self, h1_issues_json):
        self.arr_parsed_issues_row = []
        self.arr_unique_target_url = []
        self.list_vuln_score = []
        self.results = self.get_issues_row(h1_issues_json)


    def getIssuesRow(self):
        return self.arr_parsed_issues_row

    def getUniqueTargetUrl(self):
        return self.arr_parsed_issues_row

    def getVulnScore(self):
        return self.list_vuln_score

    def get_issues_row(self, h1_issues_json):
        """
        Метод h1_issues_parse парсит Jira Issues и собирает результаты в отдельный list
        arr_parsed_issues = [{arr_parsed}, {arr_parsed}, ...]
        :param cache_file:
        :return:
        """
        arr_parsed_issues_row = []
        for issue in h1_issues_json['issues']:
            arr_parsed = {}
            arr_parsed['key'] = issue['key']
            arr_parsed['jira_link'] = 'https://example.atlassian.net/browse/' + issue['key']
            arr_parsed['h1_report'] = issue['fields']['customfield_1']
            arr_parsed['severity'] = issue['fields']['customfield_2']
            arr_parsed['bug_count'] = issue['fields']['3']
            arr_parsed['vuln_type'] = None if issue['fields']['customfield_3'] is None else issue['fields']['customfield_4'][0]['value']
            arr_parsed['priority'] = None if issue['fields']['priority'] is None else issue['fields']['priority']['name']
            arr_parsed['team'] = issue['fields']['customfield_5']
            arr_parsed['target_url'] = issue['fields']['customfield_6']
            arr_parsed['gitlab'] = issue['fields']['customfield_7']
            arr_parsed['created'] = issue['fields']['created']
            arr_parsed['target'] = issue['fields']['customfield_8']
            # если статус "Done" - берем дату изменения статуса, в другом случае - текущую дату
            if issue['fields']['status']['name'] == "Done":
                arr_parsed['finished'] = issue['fields']['statuscategorychangedate'] # просто время изменения статуса
                arr_parsed['state'] = 'Done'
            else:
                arr_parsed['state'] = 'Open'
                arr_parsed['finished'] = datetime.now(pytz.timezone('Europe/Moscow')).strftime(JiraAPI.JIRA_TIME_FORMAT)

            self.arr_parsed_issues_row.append(arr_parsed)
        return self.arr_parsed_issues_row

    def get_vuln_score(self, arr_h1_issues: dict, db):
        """
        Сначала фильтруем уникальные [target_url]
        Затем в target_url собираем уязвимости {target_url: [vulns]}
        Затем считаем vuln score для каждой баги
        :param arr_h1_issues:
        :param db:
        :return:
        """
        for el in arr_h1_issues:
            if el['target_url'] is None:
                continue
            if el['target_url'] not in self.arr_unique_target_url:
                self.arr_unique_target_url.append(el['target_url'])

        # пересобираем в dict
        dict_issues = {}
        for el in self.arr_unique_target_url:
            dict_issues[el] = []

        # sort vulns by target_url
        for el in arr_h1_issues:
            if el['target_url'] is None:
                continue
            dict_issues[el['target_url']].append(el)

        self.vuln_score = self.count_vuln_score(dict_issues,db)
        return self.vuln_score

    def count_vuln_score(self, dict_issues: dict, db):
        """
        Подсчет vuln score для каждой vulnerability
        :param dict_issues:
        :param db:
        :return:
        """
        # target_url | wrt | datetime (year+month)
        for target_url, items in dict_issues.items():
            db.cur.execute(
                'SELECT value FROM business_criticality_example WHERE service = %(service)s;',
                {'service': target_url}
            )
            weight_select = db.cur.fetchone()
            if weight_select is None:
                weight = 2
            else:
                weight = int(weight_select[0])

            target_url_vuln_score = []
            for issue in items:
                if issue['priority'] == 'Highest':
                    score = 10 * weight
                if issue['priority'] == 'High':
                    score = 8 * weight
                if issue['priority'] == 'Medium':
                    score = 5 * weight
                if issue['priority'] == 'Low':
                    score = 2 * weight
                if issue['priority'] == 'Lowest':
                    score = 1 * weight
                dict_vuln = {
                    'score': score,
                    'created': datetime.strptime(issue['created'], JiraAPI.JIRA_TIME_FORMAT),
                    'finished': datetime.strptime(issue['finished'], JiraAPI.JIRA_TIME_FORMAT),
                    'target_url': target_url
                }
                target_url_vuln_score.append(dict_vuln)
            self.list_vuln_score.append(target_url_vuln_score)
        return self.list_vuln_score