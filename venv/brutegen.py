import copy




letters = [
"A","B","C","D",
"E","F","G","H",
"J","K","L","M",
"N","O","P","Q",
"R","S","T","U",
"V","W","X","Y",
"Z",
"1","2","3","4",
"5","6","7","8",
"9","0"]

def progress_bar(current, total, bar_length = 100):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * bar_length - 1) + '>'
    spaces  = ' ' * (bar_length - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

counter = 0
pswlist = []
#30260340

for a in range(len(letters)):#1
  for b in range(len(letters)):#2
    for c in range(len(letters)):#3   
      for d in range(len(letters)):#4
        print("a:", a, "/", len(letters),
        "b:", b, "/", len(letters),
        "c:", c, "/", len(letters),
        "d:", d, "/", len(letters),
        end="\r")
        for e in range(len(letters)):#5
          for f in range(len(letters)):#6
            for g in range(len(letters)):#7
              for h in range(len(letters)):#8
                counter += 1
                if counter >= 100000000:
                  counter=0
                  print("writing to a txt file...", end="\r")
                  with open("brutelist.txt", "a") as output:
                    for password in pswlist:
                      output.write(password)
                      output.write("\n")
                    #output.close()
                    pswlist = []
                psw = letters[a]+letters[b]+letters[c]+letters[d]+letters[e]+letters[f]+letters[g]+letters[h]
                pswlist.append(psw)
                #progress_bar(counter, 30260340)
                
                

               
                  
file=open("brutelist.txt", "a")
for password in pswlist:
  file.write(password)
  file.write("\n")
file.close()


    

