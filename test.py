import fanbookbotapi

token=''
print(fanbookbotapi.getme(token).text)
print(fanbookbotapi.sendmessage(token,chatid=433212507046281216).text)
print(fanbookbotapi.getPrivateChat(token,userid=389320179948986368).text)
fanbookbotapi.send_user_message(bot_token=token,channel_id='433212507046281216',guild_id='433204455396081664',text='{\"type\":\"text\",\"text\":\"6\",\"contentType\":0}')