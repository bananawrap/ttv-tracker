import requests
channelName = "xqc"
contents = requests.get('https://www.twitch.tv/' +channelName).content.decode('utf-8')
print(contents)
name = ""
index = contents.find('meta name="description" content=')#len 32
index += 33
end_index = contents.find('"',index)
for char in range(index, end_index):
    name += contents[char]
print(name)