import os
import requests
import json
from pprint import pprint


class JiraAPI:
    BASE_URL = os.environ['jira_cloud_base_url'] #FIX IT
    JIRA_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

    @staticmethod
    def post_request(url: str, data: dict) -> object:
        username = os.environ['jira_cloud_username']
        token = os.environ['jira_cloud_token']
        url = JiraAPI.BASE_URL + url
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, auth=(username, token), json=data, headers=headers)
        return response



    @staticmethod
    def get_request(url: str) -> object:
        username = os.environ['jira_cloud_username']
        token = os.environ['jira_cloud_token']
        url = JiraAPI.BASE_URL + url
        headers = {
            "Content-Type": "application/json"
        }
        proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

        response = requests.get(url, auth=(username, token), headers=headers)
        return response

    @staticmethod
    def create_issue():
        data = {
            "fields": {
                "project": {"key": "IS"},
                "customfield_10014": "IS-381",
                "summary": "No REST for the Wicked.",
                "description": {
                  "version": 1,
                  "type": "doc",
                  "content": [
                    {
                      "type": "paragraph",
                      "content": [
                        {
                          "type": "text",
                          "text": "Hello "
                        },
                        {
                          "type": "text",
                          "text": "world",
                          "marks": [
                            {
                              "type": "strong"
                            }
                          ]
                        }
                      ]
                    }
                  ]
                },
                "issuetype": {
                    "name": "Баг",
                    "id": 10119
                }
            }
        }
        # print('[x] Список сервисов без оценки бизнес критичности:')
        # print('    ', end='')
        # pprint( json.dumps(data) )
        response = JiraAPI.post_request(url="rest/api/3/issue/", data=data)
        return response

if __name__ ==\
        '__main__':
    JiraAPI.main()