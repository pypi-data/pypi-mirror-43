import hashlib

booksize = 8
Lfill = []
Lcode = []
i = 0

# ====================== TESTING=============================

with open("input.jpg", "rb") as input:
    while True:
        data = input.read(1024 * booksize)
        print(data)
        if data == b"":
            input.close()
            break
        Lfill.append('')
        Lcode.append(hashlib.md5(data).hexdigest())
        # print(data)

print('SHA1 codes')
print(Lcode)
print('List to be filled')
print(Lfill)

with open("input.jpg", "rb") as input:
    while True:
        data = input.read(1024 * booksize)
        if data == b"":
            input.close()
            break
        if hashlib.md5(data).hexdigest() == Lcode[i]:
            Lfill[i] = data
        i += 1

print('Filled list:')
print(Lfill)
# print(b''.join(Lfill))

with open("output.jpg", "wb") as output:
    for chunk in Lfill:
        output.write(chunk)

# ===================== END OF TESTING ===================================

# Function that generates the LIB file
def libgenerator(tracker_address, libfilename, filename, userfilename, filesize, chunksize):

    with open(libfilename,'w') as output:

        output.write('# the address of the tracker\n')
        output.write('hub : '+tracker_address+'\n')
        output.write('# the name of the stuff\n')
        output.write('name : '+userfilename+'\n')
        output.write('# the size of the stuff\n')
        output.write('size : '+str(filesize)+'Ko\n')
        output.write('# the size used for books\n')
        output.write('size : ' + str(chunksize)+'Ko\n')


        output.write('# SHA1 of each books \nbooks : \n')
        with open(filename, "rb") as input:
            while True:
                data = input.read(1024 * booksize)
                if data == b"":
                    input.close()
                    break
                output.write(str(hashlib.md5(data).hexdigest())+'\n')

# Associates the name of stuff with the filename so that we can locate the requested files
def lib_biyection(stuffname, filename):

    with open('filenames.bi', 'w') as output:
        for i in range(len(filename)):
            output.write(stuffname[i]+' : '+ filename[i] +'\n')

libgenerator('198.54.21.1:6115', '001.lib', 'input.jpg','Lord of Yarrak', '63', '8')


stuffnames = ['Lord of Yarrak', 'El Cacique Guaicaipuro','Er Conde der Guacharo']
filenames = ['input.jpg','cacique.mp4','conde.rar']

lib_biyection(stuffnames, filenames)


