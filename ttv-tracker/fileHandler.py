import os
import json
import logging

class FileHandler():
    def __init__(self) -> None:
        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        self.data_dir = os.path.join(self.main_dir, "data")
        
        #setting up logs and disabling unnecessary loggers
        logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logging.getLogger("urllib3.util.retry").disabled = True
        logging.getLogger("urllib3.util").disabled = True
        logging.getLogger("urllib3").disabled = True
        logging.getLogger("urllib3.connection").disabled = True
        logging.getLogger("urllib3.response").disabled = True
        logging.getLogger("urllib3.connectionpool").disabled = True
        logging.getLogger("urllib3.poolmanager").disabled = True
        logging.getLogger("requests").disabled = True

    def make_save(self):
        monday =    [0 for x in range(0,24)]
        tuesday =   [0 for x in range(0,24)]
        wednesday = [0 for x in range(0,24)]
        thursday =  [0 for x in range(0,24)]
        friday =    [0 for x in range(0,24)]
        saturday =  [0 for x in range(0,24)]
        sunday =    [0 for x in range(0,24)]
        week = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]
        
        alreadyStreamed = [False,0]
        
        lastStream = {
            "date":   "0000-00-00", 
            "hour":   "00", 
            "minute": "00"
            }
        
        data = {
                "week": week,
                "alreadyStreamed": alreadyStreamed,
                "lastStream": lastStream
                }
        
        return data
    
    def make_settings(self):
        self.settings = {
            "channelname": f"{input('channelname: ')}",
            "authorization": "ChangeMe",
            "telegram_bot_enabled": False,
            "telegram_bot_API": "",
            "telegram_chatID": "",       
            "server_ip": "0.0.0.0",
            "port": "5785",
            "timediff": "0",
            "authorized_ips": {"ip": "Authorization"}
        }
        self.save_settings() #TODO: replace with a return

    def load(self, channelname): #load savefile function
        try:
            fullname = os.path.join(self.data_dir, f'{channelname}_data.json')
            with open(fullname, 'r') as file:
                data = json.load(file)
        except Exception as err:
            logging.error(err)
            print(f"no savefile found for {channelname}")
            if input(f"make a new save for {channelname}? y/n : ") == "y":
                self.save(self.make_save(), channelname)
                try:
                    with open(fullname, 'r') as file:
                        data = json.load(file)
                except Exception as err:
                    logging.error(err)
                    print(err)
                else:
                    return data
            else:
                return None
        
        else: 
            return data

    
    def save(self, data, channelname):
        fullname = os.path.join(self.data_dir, f'{channelname}_data.json')
        with open(fullname, 'w') as file:
            json.dump(data, file)
            
            
    def save_settings(self):
        for setting in self.settings:
            if self.settings[setting] in self.userscripts:
                isUserscript = True
            else:
                isUserscript = False
            self.settings[setting] = [self.settings[setting], isUserscript]
        fullname = os.path.join(self.main_dir, 'settings.json')
        with open(fullname, "w") as file:
            json.dump(self.settings,file)
        self.load_settings() #TODO: replace with a return            
            
    def load_settings(self):
        try:
            self.userscripts = []
            fullname = os.path.join(self.main_dir, 'settings.json')
            with open(fullname, "r") as file:
                self.settings = json.load(file)
            try: 
                for setting in self.settings:
                    if isinstance(self.settings[setting], list):
                        if self.settings[setting][1]:
                            self.userscripts.append(self.settings[setting][0])
                        self.settings[setting] = self.settings[setting][0]
            except Exception:
                pass
            

        except Exception as err:
            logging.error(err),
            self.make_settings()
            with open(fullname, "r") as file:
                self.settings = json.load(file)

if __name__ == "__main__":
    pass
