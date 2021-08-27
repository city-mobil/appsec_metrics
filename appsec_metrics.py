import lib.load.github as github
import lib.load.cloud_jira as cloud_jira
from lib.upload.mongodb import upload_to_mongodb #грузим модуль для экспорта в mongo
import lib.calculate_metrics as calculate_metrics
from config import config #грузим конфиг
# from lib.load.defect_dojo import dd
import pickle

#функция выгрузки данных.
def upload_data(timeline, db, collection):
    #если у в вас не mongo можно написать что-то свое и подставить тут
    upload_to_mongodb(timeline, db, collection)

#если включен импорт данных из github
if config['services']['github']['enabled'] == True:
    #загрузка всех issues
    print('[x] Выгрузка данных из GitHub')
    issues = github.load_from_github()
    #если в конфиге указано WRT: True
    if config['services']['metrics']['wrt']:
        #считаем wrt
        print('[x] Calculate wrt')
        wrt = calculate_metrics.calculate_wrt_timeline(issues)
        #выгружаем данные
        print('[x] Upload wrt to db')
        upload_data(wrt, config['services']['github']['upload_db'], 'wrt')

    # если в конфиге указано drw: True
    if config['services']['metrics']['drw']:
        drw = calculate_metrics.calculate_wrt_timeline(issues)
        upload_data(drw,config['services']['github']['upload_db'],'drw')

#если включен импорт данных из jira cloud
if config['services']['jira_cloud']['enabled'] == True:
    #загрузка всех issues

    print('[x] Выгрузка данных из Jira Cloud')
    issues = cloud_jira.load_data()
    #если в конфиге указано WRT: True

    if config['services']['metrics']['wrt']:
        #считаем wrt
        print('[x] Calculate wrt')
        wrt = calculate_metrics.calculate_wrt_timeline(issues)
        #выгружаем данные
        print('[x] Upload wrt to db')
        upload_data(wrt, config['services']['github']['upload_db'], 'wrt')

    # если в конфиге указано drw: True
    if config['services']['metrics']['drw']:
        print('[x] Calculate drw')
        drw = calculate_metrics.calculate_drw_timeline(issues)
        print('[x] Upload drw to db')
        upload_data(drw,config['services']['github']['upload_db'],'drw')

print('[x] Done')
