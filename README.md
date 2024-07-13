<img align="left" width="159px" src="md/cat_icon.png">

<h3>CatBotNightly</h3>
Бот предназначенный для оповещения о трансляциях на twitch в discord каналах, прослушивания youtube видео, а также просмотра фотографий и фактов о котах. Добавьте в базу данных twitch.db каналы, о которых хотите получать оповещения, заполните все поля в .env файле по примему из .env.example и установите зависимости проекта.

##
* На Windows ```pip install -r requirements.txt```
* На Linux 
  * установить зависимость для виртуальной среды ```pip install virtualenv```
  * создание вируальной среды ```python -m venv catbot_venv```
  * активирование виртуальной среды ```source catbot_venv/bin/activate```  

Для того чтобы запустить бота, напишите ```python bot.py```

##
Чтобы посмотреть возможные комманды для бота напишите ```!catbot_help```