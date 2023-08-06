Getting new messages and answer

```python
from py_telegram_bot.bot import Bot

bot = Bot('Token')
api = bot.get_api()

for update in bot.get_updates():
    # Here you can use "update['text']"
    if update.text == '/start':
        # And here you can use "update['chat']['id']"
        api.send_message(chat_id=update.chat.id,
                         text='Hello!')
```

Uploading photo, videos or docs

```python
from py_telegram_bot.bot import Bot

bot = Bot('Token')
uploader = bot.get_uploader()

for update in bot.get_updates():
    if update.text == 'video':
        uploader.send_video(update.chat.id,
        # or use here video id
        open('video.mp4', 'rb'))
    elif update.text == 'photo':
        uploader.send_photo(update.chat.id,
        # or use here photo id
        open('photo.png', 'rb'))
    elif update.text == 'doc':
        uploader.send_photo(update.chat.id,
        # or use here doc id
        open('doc.zip', 'rb'))
```