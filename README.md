<img align="left" width="159px" src="md/cat_icon.png">

<h3>CatBotNightly</h3>
Бот предназначенный для оповещения о трансляциях на twitch в discord каналах, а также просмотре фотографий и фактов о котах. Добавьте в базу данных twitch.db каналы, о которых хотите получать оповещения и установите зависимости проекта.

##
* На Windows ```pip install -r requirements.txt```
* На Linux 
  * установить зависимость для виртуальной среды ```pip install virtualenv```
  * создание вируальной среды ```python -m venv catbot_venv```
  * активирование вируальной среды ```source catbot_venv/bin/activate```  

И запустите бота, написав ```python bot.py```

##
Чтобы посмотреть возможные комманды для бота напишите ```!catbot_help```