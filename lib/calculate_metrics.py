import math
from collections import Counter
from datetime import datetime,timedelta
from config import config
import math

def calculate_wrt_for_issue(issue, app_weight, dc_dict):
    severity = issue['severity']
    defect_criticality = dc_dict[severity]
    if app_weight is None:
        app_weight = issue['business_criticality']
    issue_wrt = defect_criticality * app_weight
    return dict(wrt=issue_wrt, severity=severity, defect_criticality=defect_criticality, app_weight=app_weight)


def _get_is_last_4_month(date: datetime):
    delta =  datetime.now() - date
    if delta.days <= 120:
        return True
    else:
        return False
def _get_m_by_date(date: datetime):
    return "{}-{}".format(date.year, date.month)


def _get_q_by_date(date: datetime):
    q = math.ceil(date.month / 3)
    return "{}-Q{}".format(date.year, q)




def _get_timeline_ends(issues):
    # инициализируем переменные
    first_date = (datetime.now() + timedelta(days=1))
    end_date = (datetime.now() - timedelta(days=365 * 30))
    # находим значения для frst_date & last_date
    for issue in issues:
        if issue['start_date'] < first_date:
            first_date = issue['start_date']
        if issue['end_date'] > end_date:
            end_date = issue['end_date']
    return first_date, end_date


def calculate_wrt_timeline(issues, app_weight=None):
    for cur_issue in issues:
        # подсчитываем wrt для конкретного issue
        cur_issue.update(calculate_wrt_for_issue(cur_issue, app_weight, config['defect_criticality_dict']))

    c = Counter()
    result = list()
    fix_time_regulation = config['fix_time']
    for cur_issue in issues:
        fix_time = cur_issue['end_date'] - cur_issue['start_date']
        cur_issue['date'] = _get_m_by_date(cur_issue['start_date'])
        m = _get_m_by_date(cur_issue['start_date'])
        q = _get_q_by_date(cur_issue['start_date'])
        is_last4m = _get_is_last_4_month(cur_issue['start_date'])
        project = cur_issue['project']
        c[ '|'.join((project,'M',m)) ] += cur_issue['wrt']
        c[ '|'.join((project,'q',q)) ] += cur_issue['wrt']
        if is_last4m:
            c['|'.join((project, 'last_4M_wrt', m))] += cur_issue['wrt']
        c['|'.join((project, 'M_convergence_wrt', m))] += cur_issue['wrt']
        c['|'.join((project, 'Q_convergence_wrt', q))] += cur_issue['wrt']
        c['|'.join((project, 'M_convergence_issue_count', m))] += 1
        c['|'.join((project, 'Q_convergence_issue_count', q))] += 1

        #уменьшаем convergence_issue_count в дату решения задачи
        #-> для не решенных задач уменьшение не происходит
        if cur_issue['state'] == 'Done':
            c['|'.join((project, 'M_convergence_wrt', _get_m_by_date(cur_issue['end_date'])))] -= cur_issue['wrt']
            c['|'.join((project, 'Q_convergence_wrt', _get_q_by_date(cur_issue['end_date'])))] -= cur_issue['wrt']
            c['|'.join((project, 'M_convergence_issue_count', _get_m_by_date(cur_issue['end_date'])))] -= 1
            c['|'.join((project, 'Q_convergence_issue_count', _get_q_by_date(cur_issue['end_date'])))] -= 1
            c['|'.join((project, 'm_fixed_issues', _get_m_by_date(cur_issue['end_date'])))] += 1

        c['|'.join((project, 'M_DRW_5', m))] += (fix_time.days / fix_time_regulation[cur_issue['severity']]) * cur_issue['wrt']
        c['|'.join((project, 'M_DRW_6', m))] += (fix_time.days - fix_time_regulation[cur_issue['severity']]) * cur_issue['wrt']
        c['|'.join((project, 'M_technical_debt', m))] += 1
        c['|'.join((project, 'M_fix_time.days', m))] += fix_time.days
        c['|'.join((project, 'M_DRW_3', m))] += 1 / fix_time_regulation[cur_issue['severity']]
        c['|'.join((project, 'M_DRW_4', m))] += (fix_time - timedelta(days=fix_time_regulation[cur_issue['severity']])).days






    for header,value in c.items():
        project, date_type, date = header.split('|')
        if date_type=='M' or date_type=='q':
            if value >= 40:
                significant = True
            else:
                significant = False
        elif date_type=='M_convergence_wrt' or date_type=='Q_convergence_wrt':
            if value >= 2:
                significant = True
            else:
                significant = False
        else:
            significant = 'undefind'
        result.append(dict(project=project, aggregation_type=date_type, date=date, wrt=value, significant=significant))

    return result



def calculate_drw_timeline(issues):
    #TODO agregate by month
    def _get_timerange(date1,date2):
        cur_day = date1
        while cur_day <=date2:
            yield cur_day
            cur_day += timedelta(days=1)

    def _get_timerange_by_month(date1,date2):
        cur_day = date1
        prev_date_month = _get_m_by_date(date1)
        yield cur_day

        while cur_day <=date2:
            cur_month = _get_m_by_date(cur_day)
            if cur_month == prev_date_month:
                cur_day += timedelta(days=1)
            else:
                yield cur_day
                cur_day += timedelta(days=1)
                prev_date_month = _get_m_by_date(cur_day)

    fix_time_regulation = config['fix_time']
    first_date, end_date = _get_timeline_ends(issues)
    timeline_counter = Counter()

    for cur_issue in issues:
        cur_issue_id = cur_issue['title']
        cur_issue['wrt']

        fix_time = cur_issue['end_date'] - cur_issue['start_date']
        normalized_fix_time = (fix_time.total_seconds() / 60 / 60 / 24) - fix_time_regulation[cur_issue['severity']]
        if cur_issue_id == 'IS-966':
            a='asdasd'
        for day in _get_timerange_by_month(cur_issue['start_date'], cur_issue['end_date']):
            header = '#'.join((cur_issue['project'],day.strftime('%Y-%m')))
            timeline_counter[header + '#technical_debt'] += 1
            timeline_counter[header + '#drw2'] += fix_time.days
            timeline_counter[header + '#drw3'] += 1 / fix_time_regulation[cur_issue['severity']]
            timeline_counter[header + '#drw4'] += (fix_time - timedelta(days=fix_time_regulation[cur_issue['severity']])).days
            timeline_counter[header + '#drw5'] += ((fix_time.total_seconds()/60/60/24) / fix_time_regulation[cur_issue['severity']]) * cur_issue['wrt']
            if True:
                timeline_counter[header + '#drw6'] += normalized_fix_time * cur_issue['wrt']

    # v = list(timeline_counter.values())
    # f = list()
    # for k,v in timeline_counter.most_common():
    #     if v <0:
    #         f.append((k,v))

    result_timeline = list()
    for header, value in timeline_counter.most_common():
        project, date, metrics = header.split('#')
        date = datetime.strptime(date, '%Y-%m')
        result_timeline.append(dict(project=project, date=date, metrics=metrics, drw=value, significant=True))
    return result_timeline




