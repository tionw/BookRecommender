import csv

def preprocess(file, ratingNum, bookNum):
    final=[]
    ratings = open(file, "r")
    reader = csv.reader(ratings)
    header = reader.next()
    bIndex = header.index("book_id")
    uIndex = header.index("user_id")
    rIndex = header.index("rating")

    userIDList = []
    userList = []
    bookList = [[] for k in range(bookNum)]
    newList=[]
    uL=[]
    count=0
    
    for row in reader:
        u = int(row[uIndex])
        b = int(row[bIndex])
        r = int(row[rIndex])
        uL.append(u)
        if (count!=0 and u!=uL[count-1]):
            if (len(newList)!=0):
                userList.append(newList)
            newList=[]
        newList.append([b,r])
        if (count==ratingNum-1):
            userList.append(newList)
        if (r>=4):
            bookList[(b-1)].append(u)
        if (len(userIDList)==0) or (u not in userIDList):
            userIDList.append(u)
        count+=1

##    with open('users.csv', 'w') as csvFile:
##        writer = csv.writer(csvFile)
##        writer.writerows(userList)
##
##    with open('books.csv', 'w') as csvFile:
##        writer = csv.writer(csvFile)
##        writer.writerows(bookList)

##    csvFile.close()
    
    final.append(userList)
    final.append(bookList)
    final.append(userIDList)

    return final

lol=preprocess("ratings.txt",52967,17)

test1=lol[1]

processed2=lol[0]

userlist=lol[2]

##print test1
##print
##print processed2
##print
##print userlist

def getID(inputBook):
    file = open("nameToID.txt", "r")
    reader = csv.reader(file)
    header = reader.next()
    bIndex = header.index("book_id")
    tIndex = header.index("title")

    ID = "NULL"
    
    for row in reader:
        t = row[tIndex]
        if t.lower()==inputBook.lower():
            ID = int(row[bIndex])
    return ID

def convertBack(bookID):
    file = open("nameToID.txt", "r")
    reader = csv.reader(file)
    header = reader.next()
    bIndex = header.index("book_id")
    tIndex = header.index("title")

    for row in reader:
        b = int(row[bIndex])
        if b==bookID:
            title = row[tIndex]
    print title
    
def project(string):
    if getID(string)!="NULL":
        input = getID(string)
    else:
        print "Book not found! Try again"
        return
    final=[]
    final2=[]
##    index = userlist.index(input)
    booklist = test1[input-1]
    for i in range(len(booklist)):
        for j in range(len(processed2)):
            if userlist[j]==booklist[i]:
                for k in range(len(processed2[j])):
                    if len(final)==0 and processed2[j][k][0]!=input:
                        if processed2[j][k][1]>=4:
                                final.append([processed2[j][k][0],1,1])
                        else:
                                final.append([processed2[j][k][0],1,0])
                    else:
                        for y in range(len(final)):                       
                            if processed2[j][k][0]==final[y][0]:
                                final[y][1]+=1
                                if processed2[j][k][1]>=4:
                                    final[y][2]+=1
                                break
                            elif y==len(final)-1 and processed2[j][k][0]!=final[y][0] and processed2[j][k][0]!=input:
                                if processed2[j][k][1]>=4:
                                    final.append([processed2[j][k][0],1,1])
                                else:
                                    final.append([processed2[j][k][0],1,0])
    for m in range(len(final)):
        final2.append(final[m][2]/float(final[m][1]))
    print final
    print
    print final2
    print
    if (len(final)!=0):
        finalid = final[final2.index(max(final2))][0]
        print finalid
        print convertBack(finalid)
    else:
        print "There aren't enough ratings for a recommendation!"

