import os
import time
fileSizes = []

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'

def main():
    path = input("path: ")
    for (root,dirs,files) in os.walk(path, topdown=True):
        size = 0
        for f in files:
            fp = os.path.join(path,root,f)
            size += os.path.getsize(fp)
        fileSizes.append((root,format_bytes(size)))

    #fileSizes.sort(reverse=True)
    for fileSize in fileSizes:
        print(fileSize)



if __name__=="__main__": main()

