## Teaching Report Flask
### Информационная система "Мониторинг участия преподавателей ОДОД в плановых мероприятиях".
### Ver.0.2.0
>ИС позволяет вести базу данных мероприятий, в которых участвуют педагоги дополнительного образования, с возможностью выгрузки отчетов. Работа системы реализована на сервере образовательного учреждения, на виртуальной машине под выделенным IP.

#### Используемые технологии:
+ Flask (основа)
+ Flask-WTF (формы)
+ Flask-Login (авторизация)
+ Werkzeug (кеш паролей)
+ SQLAlchemy (работа с БД)
+ Openpyxl (импорт в файл)
+ Tempfile (генерация файла)

> ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
> ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
> ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
> ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)
> ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
> ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
> ![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
> ![Visual Studio](https://img.shields.io/badge/Visual%20Studio-5C2D91.svg?style=for-the-badge&logo=visual-studio&logoColor=white)

#### На момент версии 0.2.0 реализован функционал:
> - основной пользовательский интерфейс;
> - авторизация пользователей (педагогов ДО);
> - просмотр сводной ведомости всех мероприятий на главной странице с возможностью фильтрации;
> - импорт списка мероприятий в файл формата .xlsx;
> - страница "функционал" с формой добавления/редактирования/удаления мероприятий;
> - регистрация новых пользователей администратором;
> - добавление/удаление периодов мероприятий для фильтрации.

#### Доступные пользователи (для тестирования):
> #### логины:
> + popov  (администратор)
> + glush
> + kotel
> + tupol
> + korol
>
>#### пароль для всех: 123456

### Стартовый файл index.py

#### В планах реализация:
> - личный кабинет пользователя;
> - добавление видов пользовательского доступа;
> - добавление таблиц "курс/объединение" с привязкой к пользователю и мероприятию;
> - прикрепление фотографий к мероприятиям;
> - план будущих мероприятий;
> - оповещение пользователей о необходимых действиях;
> - ...

### скрины рабочих запусков:
![Screenshots](static/screenshots.jpg)
