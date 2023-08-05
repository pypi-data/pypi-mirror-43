#-*- coding:utf-8 -*-
_author_ = '航少'
import random
def generate_poker():
    list_a=[str(i)+j for i in range(2,11) for j in '♣♥♠♦']
    list_b=[i+j for i in 'JQKA' for j in '♣♥♠♦']
    list_c=['K1','K2']
    return (list_a+list_b+list_c)
def suffer_poker(poker):
    random.shuffle(poker)
    return poker
def doudizhu (list_poler):
        a=[]
        b=[]
        c=[]
        B_score=0
        C_score=0
        while True:
            A_score=int(input("A请叫分数  （1）   （2）  （3）："))
            if A_score<1 or A_score>3:
                print("非法输入")
                A_score=0
                continue
            elif A_score==3:
                break
            while A_score!=3 :
                B_score=int(input("B请叫分数  （1）   （2）  （3）："))
                if B_score<=A_score or B_score>3:
                    print("非法输入")
                    B_score=0
                    continue
                elif B_score==3:
                    break
                while B_score!=3:
                    C_score=int(input("C请叫分数  （1）   （2）  （3）："))
                    if C_score<=B_score or C_score>3:
                        print("非法输入")
                        C_score=0
                        continue
                    elif C_score==3:
                        break
                break
            break

        print("A的地主分数:",A_score)
        print("B的地主分数:",B_score)
        print("C的地主分数:",C_score)

        cnt =int(input("请输入一次发几张牌："))
        jl=cnt
        fa=17//cnt#发牌的次数
        pj=17%cnt
        x = 0
        count = 0
        while count != fa:
            if x == 0:
                for i in list_poker[x:jl]:
                    a.append(i)#第一次a的数据存入
            else:
                for i in list_poker[x:x+cnt ]:
                    a.append(i)#第二次a的数据存入
                jl=x+cnt
            for i in list_poker[jl:jl+cnt ]:
                b.append(i)#b的数据存入
            jl = jl+cnt
            for i in list_poker[jl:jl+cnt ]:
                if jl+cnt>3*cnt*fa:
                    break
                c.append(i)#c的数据存入
            x = jl+cnt
            count += 1
        for i in list_poker[3*cnt*fa:3*cnt*fa+pj]:
            a.append(i)
        for i in list_poker[3*cnt*fa+pj:3*cnt*fa+2*pj]:
            b.append(i)
        for i in list_poker[3*cnt*fa+2*pj:3*cnt*fa+3*pj]:
            c.append(i)
        if A_score>B_score and A_score>C_score:
            for i in list_poker[51:54]:
                a.append(i)
        elif B_score>A_score and B_score>C_score:
            for i in list_poker[51:54]:
                b.append(i)
        elif C_score>A_score and C_score>B_score:
            for i in list_poker[51:54]:
                c.append(i)
        return a,b,c
list_poker=suffer_poker(generate_poker())
print(list_poker)
a,b,c=doudizhu(list_poker)
print(a)
print(b)
print(c)