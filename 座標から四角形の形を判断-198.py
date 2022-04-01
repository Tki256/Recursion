import math

def getShapeType(ax,ay,bx,by,cx,cy,dx,dy):
    # 座標から四角形の形を判断
    #今回はclass使わずオール関数で

    #対角線
    ac_x, ac_y, bd_x, bd_y = vectorDiagonal(ax,ay,bx,by,cx,cy,dx,dy)
    mid_acX, mid_acY = getMidPoint(ax,ay,cx,cy)
    mid_bdX, mid_bdY = getMidPoint(bx,by,dx,dy)

    vertical = isVertical(ac_x,ac_y,bd_x,bd_y)
    lineDistanceType = getSameLengthType(ax,ay,bx,by,cx,cy,dx,dy)
    midDistanceType = getDistanceFromMidPointType(mid_acX,mid_acY,ax,ay,bx,by,cx,cy,dx,dy)
    if isSamePoint(ax,ay,bx,by,cx,cy,dx,dy) or isPointInLine(ax,ay,bx,by,cx,cy,dx,dy):
        return "not a quadrilateral"

    if vertical and midDistanceType==1:
        #対角線が垂直かつ中心からの距離が全て同じ
        return "square（正方形）"
    elif vertical and midDistanceType==2 and lineDistanceType==1:
        #対角線が垂直かつ中心からの距離が向き合う頂点で同じ
        return "rhombus（ひし形）"
    elif not vertical and midDistanceType==1:
        #対角線が垂直にはならないかつ中心からの距離が全て同じ
        return "rectangle（長方形）"
    elif not vertical and midDistanceType==2:
        #対角線が垂直にはならないかつ中心からの距離が向き合う頂点で同じ
        return "parallelogram（平行四辺形）"
    elif trapezoidHelper(ax,ay,bx,by,cx,cy,dx,dy) and isParallel(bx-ax,by-ay,dx-cx,dy-cy) or isParallel(cx-bx,cy-by,ax-dx,ay-dy) and midDistanceType==4 or midDistanceType==5:
        #向き合う辺の一組が平行かつ中心からの距離が隣り合う頂点で同じ，もしくは全ての長さが違う
        return "trapezoid（台形）"
    elif vertical and midDistanceType==2 or midDistanceType==4 and lineDistanceType==3:
        #対角線が垂直かつ中心からの距離が向かい合う頂点で同じ，かつ隣り合う辺の長さが同じ
        return "kite（凧）"
    else:
        return "other（その他）"


def vectorDiagonal(ax,ay,bx,by,cx,cy,dx,dy):
    #対角線のベクトル
    ac_x = cx - ax
    ac_y = cy - ay
    bd_x = dx - bx
    bd_y = dy - by
    return ac_x, ac_y, bd_x, bd_y

def isParallel(line1_x,line1_y,line2_x,line2_y):
    #平行(比)
    return line1_x * line2_y == line2_x * line1_y

def isVertical(line1_x,line1_y,line2_x,line2_y):
    #垂直(内積)
    return line1_x * line2_x + line1_y * line2_y == 0

def getMidPoint(Ax,Ay,Bx,By):
    #中点の座標を出す
    midX = Ax + (Bx-Ax)/2
    midY = Ay + (By-Ay)/2
    return midX, midY

def getLength(ax,ay,bx,by):
        distance = math.pow(math.pow(ax-bx,2)+math.pow(ay-by,2),(1/2))
        return distance

def getSameLengthType(ax,ay,bx,by,cx,cy,dx,dy):
    #同じ長さの辺の数
    ab = getLength(ax,ay,bx,by)
    bc = getLength(bx,by,cx,cy)
    cd = getLength(cx,cy,dx,dy)
    da = getLength(dx,dy,ax,ay)
    return getType(ab,bc,cd,da)

def getDistanceFromMidPointType(mid_x,mid_y,ax,ay,bx,by,cx,cy,dx,dy):
    #中心からの距離
    distanceA = getLength(mid_x,mid_y,ax,ay)
    distanceB = getLength(mid_x,mid_y,bx,by)
    distanceC = getLength(mid_x,mid_y,cx,cy)
    distanceD = getLength(mid_x,mid_y,dx,dy)
    return getType(distanceA,distanceB,distanceC,distanceD)

def getType(a,b,c,d):
    if a == b == c == d:
        #全て同じ
        type = 1
    elif a == c and b == d:
        #向かい合う2辺が同じ
        type = 2
    elif a == b and c == d:
        #隣り合う2辺が同じ
        type = 3
    elif a == c or b == d:
        #向かい合う1辺が同じ
        type = 4
    else:
        type = 5
    return type

def isSamePoint(ax,ay,bx,by,cx,cy,dx,dy):
    #同じ座標のものがあるか判断
    l = [ax,ay,bx,by,cx,cy,dx,dy]
    for i in range(0,len(l)-3,2):
        for j in range(i+2,len(l)-1,2):
            if l[i] == l[j] and l[i+1] == l[j+1]:
                return True

def isPointInLine(ax,ay,bx,by,cx,cy,dx,dy):
    #3辺平行か判断
    return parallel_threeLine(ax,ay,bx,by,cx,cy) or parallel_threeLine(bx,by,cx,cy,dx,dy) or parallel_threeLine(cx,cy,dx,dy,ax,ay) or parallel_threeLine(dx,dy,ax,ay,bx,by)

def parallel_threeLine(x1,y1,x2,y2,x3,y3):
    line1_x = x2 - x1
    line1_y = y2 - y1
    line2_x = x3 - x2
    line2_y = y3 - y2
    line3_x = x3 - x1
    line3_y = y3 - y1

    return isParallel(line1_x,line1_y,line2_x,line2_y) and isParallel(line2_x,line2_y,line3_x,line3_y) and isParallel(line1_x,line1_y,line3_x,line3_y)

def trapezoidHelper(ax,ay,bx,by,cx,cy,dx,dy):
    #平行な辺が交差してなければ台形，交差してればその他
    abX = bx - ax
    abY = by - ay
    cdX = dx - cx
    cdY = dy - cy
    return abX * cdX <= 0 and abY * cdY <= 0 or abX == cdX == 0 and abY > 0 and cdY < 0 or abY < 0 and cdY > 0
