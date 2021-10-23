import requests
import json

"""
牌的样式：
黑桃:S
红桃:H
梅花:C
方块:D
"""
"""
ai选择的出牌策略编号：
 0-抽牌
 1-出手牌黑桃
 2-出手牌红桃
 3-出手牌梅花
 4-出手牌方块
"""

ai={'S': 0, 'H': 0, 'C': 0, 'D': 0, 'count': 0}             #实时记录ai方的手牌情况
deck={'S': 13, 'H' :13, 'C':13, 'D':13, 'count':52, 'most':'S'}      #实时记录此时卡组里牌的情况
open={'count':0,'top':' '}   #实时记录此时放置区里牌的情况
ai_S={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}    #记录ai手牌中黑桃花色牌的编号
ai_H={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}    #记录ai手牌中红桃花色牌的编号
ai_C={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}    #记录ai手牌中梅花花色牌的编号
ai_D={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}    #记录ai手牌中方块花色牌的编号

open_S={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}    #记录放置区中黑桃花色牌的编号
open_H={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}    #记录放置区中红桃花色牌的编号
open_C={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}    #记录放置区中梅花花色牌的编号
open_D={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}    #记录放置区中方块花色牌的编号

headers = {"Content-Type": "application/json;charset=UTF-8"}
id=''
idjilu=''
pwdjilu=''
datas = {   #记录用户账号密码信息
    'student_id': '',
    'password': ''
}
def login():
    """
    登录，并获取token
    """
    global id
    fail = 0
    url = "http://172.17.173.97:8080/api/user/login"
    r=''
    while True:
        try:
            if fail >= 10:
                break
            r = requests.post(url=url, data=datas)
            if r.status_code == 200:
                r=r.json()
                id = r['data']['detail']['id']   #获取用户id
                r = r["data"]["token"]           #获取token
            else:
                continue
        except:
            fail += 1
            print("登录连接失败，正在重连中。。。。。失败次数：", fail)
        else:
            break
    return r   #将获取到的token返回

def creat_game():
    """
    创建新的对局
    """
    datas['private'] = True
    r = requests.post(
        url="http://172.17.173.97:9000/api/game",
        data=json.dumps(datas),
        headers=headers
    )
    return r.json()["data"]["uuid"]   #将获取的uuid返回

def join_game(uuid):
    """
    加入对局
    """
    r = requests.post(
        url="http://172.17.173.97:9000/api/game/" + str(uuid),
        data=json.dumps(datas),
        headers=headers
    )
    r=r.json()
    if r['msg']=='操作成功':
        print("加入对局成功")

def get_last(uuid):
    """
    获取上步操作
    """
    url = "http://172.17.173.97:9000/api/game/" + uuid + "/last"
    r = requests.get(
        url=url,
        data=json.dumps(datas),
        headers=headers
    )
    return r.json()

def player_do(x,y,uuidji):
    """
    执行玩家操作
    """
    datas["type"] = x
    if x==1:
        datas["card"] = str(y)
    uuid=uuidji
    url = "http://172.17.173.97:9000/api/game/" + uuid
    r = requests.put(
        url=url,
        data=json.dumps(datas),
        headers=headers
    )
    return r.json()

def getresult(uuid):
    """
    获取对局结果
    :return:
    """
    url = "http://172.17.173.97:9000/api/game/" + uuid
    r = requests.get(
        url=url,
        data=json.dumps(datas),
        headers=headers
    )
    return r.json()

def aipan():
    """
    ai策略判断算法
    """
    if open['count']!=0:
        """
        此时放置区有牌
        """
        if ai['count']<=8:
            """
            当手牌数小于等于8时
            """
            if deck['most']!=open['top']:
                """
                若此时放置区顶的牌的花色与卡组中牌数最多的花色
                不相同，则选择抽牌
                """
                return 0
            else:
                """
                若此时放置区顶的牌的花色与卡组中牌数最多的花色
                相同，则在手牌中另外三种花色中选择手牌最多的那种花色
                """
                jilutype=open['top']
                jilunum=ai[jilutype]
                ai[jilutype]=0
                Max=max(ai['S'],ai['H'],ai['C'],ai['D'])
                if Max==0:
                    """
                    若手牌只有与放置区顶相同的花色或者没有牌
                    则选择抽牌
                    """
                    return 0
                if ai['S']==Max:
                    ai[jilutype]=jilunum
                    return 1
                if ai['H']==Max:
                    ai[jilutype] = jilunum
                    return 2
                if ai['C']==Max:
                    ai[jilutype] = jilunum
                    return 3
                if ai['D']==Max:
                    ai[jilutype] = jilunum
                    return 4
        else:
            """
            当手牌数大于8时
            """
            jilutype1 = open['top']
            jilunum1 = ai[jilutype1]
            ai[jilutype1]=0
            jilutype2 = deck['most']
            if ai[jilutype2]!=0 :
                """
                若此时手牌中有与卡组中牌最多的花色一致的牌，则打出这个花色
                """
                if jilutype2=='S':
                    ai[jilutype1] = jilunum1
                    return 1
                if jilutype2=='H':
                    ai[jilutype1] = jilunum1
                    return 2
                if jilutype2=='C':
                    ai[jilutype1] = jilunum1
                    return 3
                if jilutype2=='D':
                    ai[jilutype1] = jilunum1
                    return 4
            else:
                """
                若此时手牌中没有与卡组中牌最多的花色一致的牌
                则打出非这个花色的手牌中数量最多的花色
                """
                Max = max(ai['S'], ai['H'], ai['C'], ai['D'])
                if Max == 0:
                    """
                    若手牌只有与放置区顶相同的花色
                    则选择抽牌
                    """
                    return 0
                if ai['S'] == Max:
                    ai[jilutype1] = jilunum1
                    return 1
                if ai['H'] == Max:
                    ai[jilutype1] = jilunum1
                    return 2
                if ai['C'] == Max:
                    ai[jilutype1] = jilunum1
                    return 3
                if ai['D'] == Max:
                    ai[jilutype1] = jilunum1
                    return 4
    else:
        """
        放置区没牌
        """
        jilutype3=deck['most']
        if ai[jilutype3]!=0:
            if jilutype3 == 'S':
                return 1
            if jilutype3 == 'H':
                return 2
            if jilutype3 == 'C':
                return 3
            if jilutype3 == 'D':
                return 4
        else:
            if ai['count']==0:
                return 0
            else:
                Max = max(ai['S'], ai['H'], ai['C'], ai['D'])
                if ai['S'] == Max:
                    return 1
                if ai['H'] == Max:
                    return 2
                if ai['C'] == Max:
                    return 3
                if ai['D'] == Max:
                    return 4
if __name__ == "__main__":
    idjilu=input("请输入账号：")
    pwdjilu=input("请输入密码：")
    datas['student_id']=idjilu
    datas['password']=pwdjilu
    headers["Authorization"] = str(login())  # 登录成功后，将返回的token放在该请求的header中
    jilu={}
    uuid=''
    aicz={}
    yjilu=''
    choose=input("请选择加入对局或者创建对局(0为创建对局，1为加入对局):")
    if choose=='0':
        uuidcreat = creat_game()
        print("uuid=",uuidcreat)
        uuid=uuidcreat
    else:
        uuid_join = input("请输入要加入对局的uuid:")
        join_game(uuid_join)
        uuid=uuid_join
    while(1):
        """
        判断对局是否已经开始了
        """
        jilu = get_last(uuid)
        if jilu['msg']=="非法操作":
            continue
        elif jilu['msg']=="操作成功":
            break
    while(1):
        answer=-1
        flag=0
        while(1):
            jilu = get_last(uuid)
            if jilu['code']!=200:
                flag=1
                break
            if jilu['data']['your_turn'] == True:
                break
            elif jilu['data']['your_turn'] == False:
                continue
        if flag==1:
            break
        if jilu['data']['last_msg']=="对局刚开始":
            answer=aipan()

        else:
            code = jilu['data']['last_code']
            cztype = code[2]
            ptype = code[4]
            pnumber = code[5:]
            if cztype=='0':
                print("对方从<牌库>翻开了一张 ", ptype, pnumber)
                if ptype==open['top']:
                    print("对方吃牌")
                    open['top']=' '
                    open['count']=0
                    for key in open_S:
                        open_S[key] = 0
                    for key in open_H:
                        open_H[key] = 0
                    for key in open_C:
                        open_C[key] = 0
                    for key in open_D:
                        open_D[key] = 0
                else:
                    open['count'] += 1
                    open['top'] = ptype
                    if ptype=='S':
                        open_S[pnumber]=1
                    if ptype=='H':
                        open_H[pnumber]=1
                    if ptype=='C':
                        open_C[pnumber]=1
                    if ptype=='D':
                        open_D[pnumber]=1

                deck[ptype] = deck[ptype] - 1
                deck['count'] = deck['count'] - 1
                Max = max(deck['S'], deck['H'], deck['C'], deck['D'])
                if deck['S'] == Max:
                    deck['most'] = 'S'
                elif deck['H'] == Max:
                    deck['most'] = 'H'
                elif deck['C'] == Max:
                    deck['most'] = 'C'
                elif deck['D'] == Max:
                    deck['most'] = 'D'

            else:
                print("对方打出了手牌 ", ptype, pnumber)
                if ptype==open['top']:
                    open['top']=' '
                    open['count']=0
                    for key in open_S:
                        open_S[key]=0
                    for key in open_H:
                        open_H[key]=0
                    for key in open_C:
                        open_C[key]=0
                    for key in open_D:
                        open_D[key]=0
                else:
                    open['count'] += 1
                    open['top'] = ptype
                    if ptype=='S':
                        open_S[pnumber]=1
                    if ptype=='H':
                        open_H[pnumber]=1
                    if ptype=='C':
                        open_C[pnumber]=1
                    if ptype=='D':
                        open_D[pnumber]=1
                open['count'] += 1
                open['top'] = ptype
            answer=aipan()
        if answer==0:
            aicz=player_do(0,"",uuid)
        elif answer==1:
            for key in ai_S:
                if ai_S[key]==1:
                    ai_S[key]=0
                    yjilu=key
                    break
            yjilu='S'+yjilu
            if len(yjilu)>=2:
                aicz=player_do(1,yjilu,uuid)
            else:
                aicz = player_do(0, "", uuid)
            yjilu=""
        elif answer==2:
            for key in ai_H:
                if ai_H[key]==1:
                    ai_H[key]=0
                    yjilu=key
                    break
            yjilu = 'H' + yjilu
            if len(yjilu) >= 2:
                aicz = player_do(1, yjilu, uuid)
            else:
                aicz = player_do(0, "", uuid)
            yjilu =""
        elif answer==3:
            for key in ai_C:
                if ai_C[key]==1:
                    ai_C[key]=0
                    yjilu=key
                    break
            yjilu = 'C' + yjilu
            if len(yjilu) >= 2:
                aicz = player_do(1, yjilu, uuid)
            else:
                aicz = player_do(0, "", uuid)
            yjilu =""
        elif answer==4:
            for key in ai_D:
                if ai_D[key]==1:
                    ai_D[key]=0
                    yjilu=key
                    break
            yjilu = 'D' + yjilu
            if len(yjilu) >= 2:
                aicz = player_do(1, yjilu, uuid)
            else:
                aicz = player_do(0, "", uuid)
            yjilu =""
        code=aicz['data']['last_code']
        cztype = code[2]
        ptype = code[4]
        pnumber = code[5:]
        if cztype == '0':
            print("你从<牌库>翻开了一张 ", ptype, pnumber)
            if ptype == open['top']:
                print("你吃牌")
                open['top'] = ' '
                ai['count']+=open['count']
                open['count'] = 0
                for key in open_S:
                    ai['S']+=open_S[key]
                    ai_S[key]+=open_S[key]
                    open_S[key] = 0
                for key in open_H:
                    ai['H'] += open_H[key]
                    ai_H[key] += open_H[key]
                    open_H[key] = 0
                for key in open_C:
                    ai['C'] += open_C[key]
                    ai_C[key] += open_C[key]
                    open_C[key] = 0
                for key in open_D:
                    ai['D'] += open_D[key]
                    ai_D[key] += open_D[key]
                    open_D[key] = 0
                ai['count']+=1
                ai[ptype]+=1
                if ptype=='S':
                    ai_S[pnumber]+=1
                if ptype=='H':
                    ai_H[pnumber]+=1
                if ptype=='C':
                    ai_C[pnumber]+=1
                if ptype=='D':
                    ai_D[pnumber]+=1
            else:
                open['count'] += 1
                open['top'] = ptype
                if ptype == 'S':
                    open_S[pnumber] = 1
                if ptype == 'H':
                    open_H[pnumber] = 1
                if ptype == 'C':
                    open_C[pnumber] = 1
                if ptype == 'D':
                    open_D[pnumber] = 1

            deck[ptype] = deck[ptype] - 1
            deck['count'] = deck['count'] - 1
            Max = max(deck['S'], deck['H'], deck['C'], deck['D'])
            if deck['S'] == Max:
                deck['most'] = 'S'
            if deck['H'] == Max:
                deck['most'] = 'H'
            if deck['C'] == Max:
                deck['most'] = 'C'
            if deck['D'] == Max:
                deck['most'] = 'D'

        else:
            print("你打出了手牌 ", ptype, pnumber)
            if ptype == open['top']:
                open['top'] = ' '
                ai['count']+=open['count']
                open['count'] = 0
                for key in open_S:
                    ai_S[key] += open_S[key]
                    open_S[key] = 0
                for key in open_H:
                    ai_H[key] += open_H[key]
                    open_H[key] = 0
                for key in open_C:
                    ai_C[key] += open_C[key]
                    open_C[key] = 0
                for key in open_D:
                    ai_D[key] += open_D[key]
                    open_D[key] = 0
                ai['count'] += 1
                ai[ptype] += 1
                if ptype == 'S':
                    ai_S[pnumber] = 1
                if ptype == 'H':
                    ai_H[pnumber] = 1
                if ptype == 'C':
                    ai_C[pnumber] = 1
                if ptype == 'D':
                    ai_D[pnumber] = 1
            else:
                open['count'] += 1
                open['top'] = ptype
                ai['count']=ai['count']-1
                if ptype == 'S':
                    ai_S[pnumber]=0
                    open_S[pnumber] = 1
                if ptype == 'H':
                    ai_H[pnumber] = 0
                    open_H[pnumber] = 1
                if ptype == 'C':
                    ai_C[pnumber] = 0
                    open_C[pnumber] = 1
                if ptype == 'D':
                    ai_D[pnumber] = 0
                    open_D[pnumber] = 1
        if deck['count'] == 0:
            break
    result=getresult(uuid)
    if result['data']['winner']==0:
        print("对局结束,胜利者为1P")
    else:
        print("对局结束,胜利者为2P")