w1 = 5
w2 = 4


daM = {1:(-2,1),
       2:(-1,2),
       3:(1,2),
       4:(2,1),
       5:(2,-1),
       6:(1,-2),
       7:(-1,-2),
       8:(-2,-1),
       }
def wraOne(p1,p2,a,b):
    a = p1+a
    b = p2+b
    if a<0 or b<0 or a>w1 or b>w2:
        return False,0,0
    return True,a,b

def getNextPos(a,b,n):
    return wraOne(a,b,daM[n][0],daM[n][1])
curPos = (0,0)
posList = []
tryTimeList = []
tryTime = 1
co = 0
while True:
    co += 1
    if co %1000000==0:
        print (co)
    if len(posList)==(w1+1)*(w2+1)-1 and abs(curPos[0])+abs(curPos[1])==3 and curPos[0]*curPos[1]!=0:
        print ('ok')
        print(posList,curPos)
        #print(posList)
        break
    if tryTime == 9:
        #print(len(hasIn),posList)
        if not posList:
            print('failed')
            break
        curPos = posList[-1]
        tryTime = tryTimeList[-1]
        posList = posList[:-1]
        tryTimeList = tryTimeList[:-1]
        tryTime += 1
        continue
    r,a,b = getNextPos(curPos[0],curPos[1],tryTime)
    if not r or (a,b) in posList:
        tryTime += 1
        continue
    #print(a,b,tryTime,len(hasIn))
    posList.append(curPos)
    tryTimeList.append(tryTime)
    curPos = (a,b)
    tryTime = 1
if __name__ == '__main__':
    s = getNextPos(2,2,4)
    print (s)
