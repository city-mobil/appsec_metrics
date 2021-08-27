# Зачем это нужно?
При построении AppSec в компаниях со значительным количеством проектов становится актуальным вопрос подсчета метрик ИБ для проектов. Построение метрик основано на https://owasp.org/www-pdf-archive/Magic_Numbers_-_5_KPIs_for_Measuring_WebAppSec_Program_Success_v3.2.pdf

Список метрик можно посмотреть в секции ниже.

Предпологается что результаты отгружаются в mongodb, а затем визуализируются с помощью MetaBase


# О чем приложение
Appsec-metrics - это готовое решение для подсчета и визуализации некоторых метрик ИБ:
- WRT_Total 
- WRT по проектам по отрезкам в месяцы и кварталы
- размер технического долга по ИБ (количество всех не решенных задач по ИБ)
- количество исправленных багов
- разница между количеством поставляемых и исправляемых задач
- DRW


## Источники данных для подсчета 
- GitHub (рабочий пример)
- Jira Cloud (требует доробки под вашу Jira)


## Как работает приложение?
Приложние запрашивает по API все необходимые данные, подсчитывает метрики и сохраняет результат в mongodb. Дальше результат отображается в MetaBase


# Настройка приложения
Для работы приложения, необходимо заполнить необходимые переменные GitLab:
1. jira_cloud_username:    имя пользователя Jira, например a.voznesenskii@city-mobil.ru
2. jira_cloud_token:       Jira API токен
3. jira_cloud_base_url:    Jira Cloud URL, например: https://city-mobil.atlassian.net/
4. mongodb_connect_string: MongoDB connect string
5. save_to_pickle_cache:   переменная позволяет сохранять данные, полученные из Jira Cloud в pickle; это кэш, удобный для отладки 
6. use_pickle_cache:       переменная позволяет использовать данные, сохраненные в pickle 


## Интеграция с Jira Cloud
Интеграция с Jira Cloud осуществляется с помощью трех переменных: jira_cloud_username, jira_cloud_token, jira_cloud_base_url. Токен для Jira Cloud можно сгенерировать на [этой странице](https://id.atlassian.com/manage-profile/security/api-tokens).

### Тестовый запрос, для проверки интеграции с Jira Cloud 
```bash
curl --request GET \
  --url 'https://example.atlassian.net/rest/api/3/issue/SEC-100500' \
  --user 'owner@example.com:<your token>' \
  --header 'Accept: application/json' | jq 
```

### layers of abstraction over jira
1. Высокоуровневое API - cloud_jira.py: Связано с другими уровнями абстракции. Ничего не знает о Jira и подробстях нормализации данных
2. Средний уровень API - jira_cloud_example.py: Сильно привязано к тому как отдаются данные из Jira Cloud. Требуется дороботка при использовании на каждом новом проекте. Выполняет нормализацию данных.
3. Низкоуровневое API fat-api.py Выполняет запросу к конкретному API Jira. Не имеет значения какие данные возвращает Jira Cloud



# Интеграция с metabase
## Запуск metabase
```bash
docker run -d \
  -p 80:3000 \
  -v ~/metabase-data6:/metabase-data \
  -e "JAVA_OPTS=-Xmx3g" \
  -e "MB_DB_FILE=/metabase-data/metabase.db" \
  --name metab7 metabase/metabase
```


# О нас
appsec_metrics поддерживают:
* [Вацлав Довнар](https://www.linkedin.com/in/vatclav-dovnar/) 
* [Александр Вознесенский](https://www.linkedin.com/in/voznesensky/)
* [Георгий Старостин](https://www.linkedin.com/in/georgii-starostin-06932942/)


# Спонсор
![](static/img/city.logo.png)


## Лицензия

appsec_metrics лицензируется под [Apache License 2.0](LICENSE)
