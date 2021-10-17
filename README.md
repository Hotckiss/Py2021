# Py2021
Py 2021


Deploy: ```bash deploy.sh```

On remote host: ```bash run.sh```

Example (server is always available): ```curl --header "Content-Type: application/json"   --request POST   --data '{"name": "sample", "max_parallel_pools": 2, "min_pool_acceptance_rate": 0.7, "max_hourly_appeals": 15, "check_interval_minutes": 5, "soft_alert_multiplier": 0.6}'   http://84.252.142.128:6067/api/track```



Tests:

```cd FlaskApp && python3 -m pytest```

gql:

```
{
   tracks(limit: 2, pattern: "p") {
     maxParallelPools,
     minPoolAcceptanceRate,
     softAlertMultiplier,
     maxHourlyAppeals,
     checkIntervalMinutes
     project {
       id,
       publicName
     }
   }
 }
 ```

Архитектура:

1) Track Service отвечает на запросы регистрации алера и их хранение
2) DataLens Service отвечает за трансляцию сырых данных проектов и сообщений в дашборд DataLens
3) Toloka Project Service предоставляет фасад для работы с проектами Толоки
4) Toloka Messages Service предоставляет фасад для работы с сообщениями Толоки
5) Notification Service отвечает за уведомление пользователя о сработавших алертах
![Architectire](https://github.com/Hotckiss/Py2021/blob/master/toloka.png)
