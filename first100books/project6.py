import csv
import time
import random

#k-fold corss validation
ratingNo = 994688
total = 52880
folds = 2
split = total/folds


booknameid = [2]
f = open('nametoID.txt','r')
fr = csv.reader(f)
header = fr.next()
bn = header.index("title")
for line in fr:  
    booknameid.append(line[bn])
f.close()

def preprocess(file, ratingNum):
    start = time.time()
    final=[]
    ratings = open(file, "r")
    reader = csv.reader(ratings)
    header = reader.next()
    bIndex = header.index("book_id")
    uIndex = header.index("user_id")
    rIndex = header.index("rating")

    userIDList = []
    userIDset = set()
    userList = []
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
        if (u not in userIDset):
            userIDList.append(u)
            userIDset.add(u)
        count+=1

    final.append(userList)
    final.append(userIDList)
    end = time.time()
    print end-start
    return final

def preprocess2(file, bookNum, userlist3):
##    start = time.time()
    final=[]
    ratings = open(file, "r")
    reader = csv.reader(ratings)
    header = reader.next()
    bIndex = header.index("book_id")
    uIndex = header.index("user_id")
    rIndex = header.index("rating")

    bookList = [[] for k in range(bookNum)]

    for row in reader:
        u = int(row[uIndex])
        b = int(row[bIndex])
        r = int(row[rIndex])
##        if n==4:
##            if (r>=4) and u<=userlist[split*3-1]:
##                bookList[(b-1)].append(u)
##        elif n==3:
##            if (r>=4) and (u<=userlist[split*2-1] or u>userlist[split*3-1]):
##                bookList[(b-1)].append(u)
##        elif n==2:
##            if (r>=4) and (u<=userlist[split-1] or u>userlist[split*2-1]):
##                bookList[(b-1)].append(u)
##        else:
##            if (r>=4) and (u>userlist[split-1]):
##                bookList[(b-1)].append(u)
        if (r>=4) and (u in userlist3):
            bookList[(b-1)].append(u)
        
##    end = time.time()
##    print end-start
    return bookList

lol=preprocess("ratings77.txt",ratingNo)

processed2=lol[0]
userlist=lol[1]
test1=preprocess2("ratings77.txt", 100, set(userlist))

print len(userlist)

c = list(zip(processed2, userlist))
random.shuffle(c)
processed2, userlist = zip(*c)

def splitL(split,n,processed2,userlist,folds):
    ret=[]
    if (n==folds):
        processed22=processed2[split*(folds-1):]
##        userlist2=userlist[split*(folds-1):]
        processed23=processed2[:split*(folds-1)]
        userlist3=userlist[:split*(folds-1)]

    elif (n==1 and folds!=1):
        processed22=processed2[:split]
##        userlist2=userlist[:split]
        processed23=processed2[split:]
        userlist3=userlist[split:]

    elif (n==1 and folds==1):
        processed22=processed2[52880-5288:]
        processed23=processed2
        userlist3=userlist

    else:
        processed22=processed2[split*(n-1):split*n]
##        userlist2=userlist[split*(n-1):split*n]
        processed23=processed2[:split*(n-1)]+processed2[split*n:]
        userlist3=userlist[:split*(n-1)]+userlist[split*n:]
    ul3=set(userlist3)
    test1=preprocess2("ratings77.txt",100,ul3)

    ret.append(processed22)
##    ret.append(userlist2)
    ret.append(test1)
    ret.append(processed23)
    ret.append(userlist3)
    return ret

print len(processed2)

def testData(processed2,userlist,folds, thresh):
    avgpct=0
    avgtp=0
    avgtn=0
    avgfp=0
    avgfn=0
    totalscore=0
    totaloutof=0
    for z in range(1,folds+1):
##        print "Fold: "+str(z)
        start = time.time()
        ret = splitL(split,z,processed2,userlist,folds)
        processed22=ret[0]
        test1=ret[1]
        processed23=ret[2]
        userlist3=ret[3]
        
        array=[]
        for w in range(100):
    ##        print w+1
            #array.append(project(str(convertBack(w+1)),processed23,userlist3,test1, thresh))
            array.append(25)
        ##true positives = user input highly rated book and rated recommended book highly
        score = 0
        ##false positives = user input highly rated book and rated recommended book poorly
        score2= 0
        ##false negatives = user input lowly rated book, and rated recommended book highly
        score3= 0
        ##true negatives = user input lowly rated book, and rated recommended book poorly
        score4= 0
        
        outof = 0
        count = 0
        for i in processed22:
            for j in i:
                count+=1
                if j[1]>=4:
                    for l in i:
                        if(array[j[0]-1]==l[0]):
                            if(l[1]>=4):
                                score+=1
                            else:
                                score2+=1
                            outof+=1
                            break
                else:
                    for l in i:
                        if(array[j[0]-1]==l[0]):
                            if(l[1]>=4):
                                score3+=1
                            else:
                                score4+=1
                            outof+=1
                            break
                                
##        print "Accuracy: "+str((score+score4)/float(outof))
        avgpct+=(score+score4)/float(outof)
##        print "True Positives: "+str(score)
        avgtp+=score
##        print "False Positives: "+str(score2)
        avgfp+=score2
##        print "False Negatives: "+str(score3)
        avgfn+=score3
##        print "True Negatives: "+str(score4)
        avgtn+=score4
##        print "Common books(>=4): " + str(score)
##        totalscore+=score
##        print "Common books: "+str(outof)
##        totaloutof+=outof
##        print "No. ratings in test set: " + str(count)
        end = time.time()
##        print "Time taken: " + str(end-start)
##        print "-------------------------------------------"
    print "Total Accuracy: "+str(avgpct/float(folds))
##    print "Average Common books(>=4): "+str(totalscore/float(folds))
##    print "Average Common books: "+str(totaloutof/float(folds))
    print "TP: "+str(avgtp)
    print "FP: "+str(avgfp)
    print "FN: "+str(avgfn)
    print "TN: "+str(avgtn)
    print

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
##    for i in range(0,3000,100):
    thresh=1500
    testData(processed2, userlist, folds, thresh)
    end = time.time()
    print "Total time taken: "+str(end-start)
#testtime()

def testtime2(string):
    start = time.time()
    project(string)
    end = time.time()
    print end-start

def project(string, processed2, userlist, test1, thresh):
    if getID(string)!=0:
        input = getID(string)
    else:
        print "Book not found! Try again"
        return
    final=[]
    indexes=[]
    indexSet=set()
    booklist = test1[input-1]
    for i in booklist:
        for k in processed2[userlist.index(i)]:
            if k[0] not in indexSet and k[0]!=input:
                indexes.append(k[0])
                indexSet.add(k[0])
                if k[1]>=4:
                    final.append([k[0],1,1])
                else:
                    final.append([k[0],1,0])
            elif k[0] in indexSet:
                final[indexes.index(k[0])][1]+=1
                if k[1]>=4:
                    final[indexes.index(k[0])][2]+=1
    if (len(final)!=0):
        ct=0
        ct2=0
        maxindex=0
        minindex=0
        max=final[0][2]/float(final[0][1])
        min=final[0][2]/float(final[0][1])
        maxunder100=0
        maxindex100=0
        minunder100=0
        minindex100=0
        for q, m in enumerate(final):
            if m[2]/float(m[1]) > max:
                if m[1]>thresh:
                    max = m[2]/float(m[1])
                    maxindex = q
                    ct+=1
                maxunder100 = m[2]/float(m[1])
                maxindex100 = q
                
            if m[2]/float(m[1]) < min:
                if m[1]>50:
                    min = m[2]/float(m[1])
                    minindex = q
                    ct2+=1
                minunder100 = m[2]/float(m[1])
                minindex100 = q
                
            elif m[2]/float(m[1]) == max:
                if m[1]>final[maxindex][1]:
                    if m[1]>thresh:
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
            if m==len(final)-1 and ct2==0:
                min = minunder100
                minindex = minindex100
                
        finalid=final[maxindex][0]
        finalid2=final[minindex][0]
##        print finalid
##        print "Recommended Book: "+str(convertBack(finalid))
##        print "Link Rating: "+str(max)
##        print "Total Common Ratings: "+str(final[maxindex][1])
    else:
        print "There aren't enough ratings for a recommendation!"
        print "ERROR"
        finalid=0
        finalid2=0
##    print
##    print final
    return finalid
