config = {
    #no sensitive data. Just examples from internet
    'github_projects': {
        'ClickHouse/ClickHouse': {'business_criticality': 13, 'tags': ['security']},
        'authelia/authelia': {'business_criticality': 9, 'tags': ['security']},
        'gravitational/teleport': {'business_criticality': 17, 'tags': ['security']},
        'rust-lang/rust': {'business_criticality': 5, 'tags': ['A-security']},
        'openshift/origin': {'business_criticality': 7, 'tags': ['area/security']},
        'kubernetes/kubernetes': {'business_criticality': 7, 'tags': ['area/security']},
        'ansible/ansible': {'business_criticality': 14, 'tags': ['security']},
        'dotnet/runtime': {'business_criticality': 12, 'tags': ['Security']},
        'nodejs/node': {'business_criticality': 16, 'tags': ['security']}

    },
    'github_severity_list': (
        #(comments_count, Severity)
        (11, 'Critical'),
        (8, 'High'),
        (3, 'Medium'),
        (0, 'Low')

    ),
    'defect_criticality_dict': {
    #{Severity, criticality rate}
        'Critical': 11,
        'High': 8,
        'Highest': 8,
        'Medium': 3,
        'Low':   1,
        'Lowest':   1,
        'No impact': 0
    },
    'fix_time': {
        'Critical': 1,
        'High': 2,
        'Medium': 3,
        'Low': 4,
        'No impact': 5
    },

    'services': {
        'github': {
            'enabled': False,
            'upload_db': 'wrt',
        },
        'jira_cloud': {
            'enabled': True,
            'upload_db': 'wrt',
        },
        'metrics': {
            'wrt': True,
            'drw': True
        }
    },
    'business_criticality': {
        'exampl1': 8,
        'example2:': 10

    },
    'use_pickle_cache': True,
    'save_to_pickle_cache': True
}
