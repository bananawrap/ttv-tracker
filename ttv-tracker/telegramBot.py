import requests

class TelegramBot():
    def __init__(self, bot_token) -> None:
        self.bot_token = bot_token
    
    def send(self, chatID, message):
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + chatID + '&parse_mode=Markdown&text=' + message
        
        response = requests.get(send_text)
        
        return response
    
if __name__=="__main__":
    pass