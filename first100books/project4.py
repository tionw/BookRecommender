import csv
import time
import random

booknameid = [2]
f = open('nametoID.txt','r')
fr = csv.reader(f)
header = fr.next()
bn = header.index("title")
for line in fr:  
    booknameid.append(line[bn])
f.close()

def preprocess(file, ratingNum, bookNum):
    start = time.time()
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
    newList=set()
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
            newList=set()
        newList.add((b,r))
        if (count==ratingNum-1):
            userList.append(newList)
        if (r>=4):
            bookList[(b-1)].append(u)
        if (len(userIDList)==0) or (u not in userIDList):
            userIDList.append(u)
        count+=1

    final.append(userList)
    final.append(bookList)
    final.append(userIDList)
    end = time.time()
    print end-start
    return final

lol=preprocess("ratings.txt",218477,100)
##lol=preprocess("ratings66.txt",994879,100)

test1=lol[1]
processed2=lol[0]
userlist=lol[2]

lol2=preprocess("testSet.txt",1761,100)

test2 = lol2[1]
processed22=lol2[0]
userlist2=lol[2]
print len(userlist)

def testData():
    score = 0
    outof = 0
    for i in processed22:
        for j in i:
            if j[1]>=4:
                result = project(str(convertBack(j[0])))
##                print convertBack(result)
                for p in i:
                    if(p[0]==result):
                        if(p[1]>=4):
                            score+=1
                        outof+=1
                        break
    print score/float(outof)
    print score
    print outof

def getID(inputBook):
##    if inputBook not in booknameid:
##        print "Book not found"
##        return 0
    return booknameid.index(inputBook)

def convertBack(bookID):
    if bookID > len(booknameid):
        print "Book not found"
        return ''
    return booknameid[bookID]

def testtime():
    start = time.time()
    testData()
    end = time.time()
    print end-start
#testtime()

def testtime2(string):
    start = time.time()
    project(string)
    end = time.time()
    print end-start

def project(string):
    if getID(string)!=0:
        input = getID(string)
    else:
        print "Book not found! Try again"
        return
    final=[]
    indexes=[]
    indexSet=set()
    booklist = test1[input-1]
##    print input
##    print
##    print len(booklist)
##    print
    for i in booklist:
        for k in processed2[userlist.index(i)]:
            if k[0] not in indexSet and k[0]!=input:
                indexes.append(k[0])
                indexSet.add(k[0])
                if k[1]>=4:
                    final.append([k[0],1,1])
                else:
                    final.append([k[0],1,0])
            if k[0] in indexSet:
                final[indexes.index(k[0])][1]+=1
                if k[1]>=4:
                    final[indexes.index(k[0])][2]+=1
    if (len(final)!=0):
        ct=0
        maxindex=0
        max=final[0][2]/float(final[0][1])
        maxunder100=0
        maxindex100=0
        for q, m in enumerate(final):
            if m[2]/float(m[1]) > max:
                if m[1]>100:
                    max = m[2]/float(m[1])
                    maxindex = q
                    ct+=1
                maxunder100 = m[2]/float(m[1])
                maxindex100 = q
            elif m[2]/float(m[1]) == max:
                if m[1]>final[maxindex][1]:
                    if m[1]>100:
                        max = m[2]/float(m[1])
                        maxindex = q
                        ct+=1
                    maxunder100 = m[2]/float(m[1])
                    maxindex100 = q
                if m[1]>final[maxindex100][1]:
                    maxunder100 = m[2]/float(m[1])
                    maxindex100 = q
            if m==len(final)-1 and ct==0:
                max = maxunder100
                maxindex = maxindex100
        finalid=final[maxindex][0]
##        print finalid
##        print "Recommended Book: "+str(convertBack(finalid))
##        print "Link Rating: "+str(max)
##        print "Total Common Ratings: "+str(final[maxindex][1])
    else:
        print "There aren't enough ratings for a recommendation!"
        print "ERROR"
##    print
##    print final
    return finalid
