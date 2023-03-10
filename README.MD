**Бот шлет уведомления [в этот](https://t.me/arm_seismology_monitoring) телеграм-канал**  

**Что за бот?**  
Бот слушает веб сокет, через который Европейско-Средиземноморский сейсмологический центр рассылает алерты в *почти* реальном времени.   
Землетрясения просиходят по всей планете практические каждые 5 минут, поэтому бот парсит и шлет алерты только по тем эпизодам, которые относятся к Армении и небольшому радиусу вокруг.  

**Как завести и сменить регион?**  
Поправить нужно совсем не много вещей.  

Переменные окружения:  
* TEST_MODE - для отладки должно быть "test". Для работы - что угодно иное  
* TOKEN_TG_BOT - токен тг бота  
* CHANEL_ID - id канала, куда бот будет постить (бота нужно сделать админом)  
* ADMIN_ID - id персонального чата, куда бот будет слать уведомления в случае падения приложения или неестественно долгого ожидания ответа от сокета   

Локальное время:  
* можно брать время, которое шлет сам сервис, для этого нужно просто раскомментировать строку в prepare_msg_for_tg() из data_handler.py  
* можно формировать время самому, указав нужный регион в get_local_time() из data_handler.py

Геолокация:  
* сервис возвращает координаты (долгота, широта, высота) и наименование региона. Логика, которая с этими данными работает, находится в check_location() и check_aftershock() из data_handler.py   

*Небольшое пояснение по работе с координатами:*  
Координаты, заданные в polygon_list из consts.py  - это вершины четырехугольника, очерченного "вокруг" Армении(т.е просто комбинации широты и долготы для 4х точек).  
Поскольку земля - не плоскость, простые формулы, которые позволяют проверить, находится ли точка внутри многоугольника, работают не совсем корректно.   
Решений у этой проблемы несколько:    
1. взять радиус побольше, чтоб туда точно все попало - *сейчас так*  
2. трасформировать координаты и оперировать уже трансформированными значениями - *TODO*  


**references:**  
https://github.com/EMSC-CSEM  
https://www.emsc-csem.org/  