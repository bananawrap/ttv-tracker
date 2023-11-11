import socket
import json

class TtvServer():
    def __init__(self, fh) -> None:
        self.fh = fh

    def update_reslist(self, data):
        week = data["week"]
        resList = []
        combinedDays = [0 for x in range(0,24)]
        for i in range(len(combinedDays)):
            resList.append(combinedDays[i]+week[0][i]+week[1][i]+week[2][i]+week[3][i]+week[4][i]+week[5][i]+week[6][i])
        return resList

    def main(self):
        s = socket.socket()
        BUFFERSIZE = 1024
        port = int(self.fh.settings["port"])
        authorized_ips = self.fh.settings["authorized_ips"]
        s.bind(('', port))        
        print (f"[+] socket binded to {port}")

        s.listen(5)    
        print ("[+] socket is listening")

        while True:
            try:
                c, addr = s.accept()

                print ('\n[+] Got connection from', addr )

                client_message = c.recv(BUFFERSIZE).decode()
                if client_message:
                    
                    client_message = json.loads(client_message)
                    client_authorization = client_message["authorization"]
                    if authorized_ips[addr[0]] == client_authorization:
                        
                        
                        client_channelname = client_message["channelname"]
                        client_data = client_message["data"]
                        
                        client_totalsum = sum(self.update_reslist(client_data))
                        print(f"[+] authorization accepted\n[+] requested channel: {client_channelname}")
                        if len("") != len(client_channelname):
                            data = self.fh.load(client_channelname)
                            
                        resList = self.update_reslist(data)
                        
                        totalsum = sum(resList)

                        if totalsum > client_totalsum:
                            option = "send_to_client"
                        elif totalsum < client_totalsum:
                            option = "send_to_server"
                        elif totalsum == client_totalsum:
                            option = "synced"
                        
                        
                        if option=="send_to_client":
                            
                            message = json.dumps({
                                "option":option,
                                "channelname":client_channelname,
                                "data":data,
                            })
                            
                            c.send(message.encode())
                            
                            print(f"sent {client_channelname}_data.json to {addr[0]}")
                            
                            c.close()

                            
                        elif option=="send_to_server":
                            
                            message = json.dumps({
                                "option":option,
                                "channelname":client_channelname,
                            })
                            
                            c.send(message.encode())
                            
                            self.fh.save(client_data,client_channelname)
                            
                            print(f"saved {client_channelname}_data.json from {addr[0]}")
                            
                            c.close()
                        
                        elif option=="synced":
                            
                            message = json.dumps({
                                "option":option,
                                "channelname":client_channelname,
                            })
                            
                            c.send(message.encode())
                            
                            print(f"[+] {client_channelname}_data.json was in sync with {addr[0]}")
                            
                            c.close()
                            
                        else:
                            c.close()
                    else:
                        c.send("Unauthorized".encode())
                        c.close()
                else:
                    c.send("Unauthorized".encode())
                    c.close()
                
            except Exception as err:
                try:
                    c.send(err.encode())
                    c.close()
                except Exception:
                    try:
                        c.close()
                    except Exception:
                        pass
                    pass
                print(err)

if __name__=="__main__": 
    TtvServer.main()
