<img align="left" width="159px" src="md/cat_icon.png">

<h3>CatBotNightly</h3>
Бот предназначенный для оповещения о трансляциях на twitch в discord каналах, прослушивания youtube видео, также просмотра фотографий и фактов о котах. Добавьте в базу данных twitch.db каналы, о которых хотите получать оповещения, заполните поля в .env файле по примему из .env.example и установите зависимости проекта.

##
* На Windows ```pip install -r requirements.txt``` и ```pip install -U discord.py[voice]```
* На Linux 
  * установить пакет для работы с виртуальной средой ```sudo apt install virtualenv``` (debian, ubuntu, mint, pop os, zorin os)
  * создание вируальной среды ```python3 -m venv catbot_venv```
  * активирование виртуальной среды ```source catbot_venv/bin/activate```  
  * установка зависимостей ```pip install -r requirements.txt``` и ```python3 -m pip install -U discord.py[voice]```

Для того чтобы запустить бота, напишите ```python bot.py```

##
Чтобы посмотреть возможные комманды для бота напишите ```!catbot_help```