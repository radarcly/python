import random

def judge(guess,word):
    global wrongTimes
    result=""
    flag = 0
    for x in word:
        for y in guess:
            if x==y:
                flag =1
        if flag==1:
            result +=x+" "
        else:
            result +="_ "
        flag = 0
    flag = 1
    for x in word:
        if guess[-1]==x:
            flag=0
    wrongTimes += flag

    if wrongTimes == 0:
        print(''' ______
|  |
|  
| 
|  
|  
|_____
|     |____
|__________|''')
    elif wrongTimes == 1:
        print( '''______
|  |
|  O
| 
|  
| 
|_____
|     |____
|__________|''')
    elif wrongTimes == 2:
        print( '''______
|  |
|  O
| /
|  
| 
|_____
|     |____
|__________|''')
    elif wrongTimes == 3:
        print(''' ______
|  |
|  O
| /|
|  |
|  
|_____
|     |____
|__________|''')
    elif wrongTimes == 4:
        print(''' ______
|  |
|  O
| /|\ 
|  |
|  
|_____
|     |____
|__________|''')
    elif wrongTimes == 5:
        print( '''______
|  |
|  O
| /|\ 
|  |
| /  
|_____
|     |____
|__________|''')
    else:
        print(''' ______
|  |
|  O
| /|\ 
|  |
| / \ 
|_____
|     |____
|__________|''')
    return result

f = open("words.txt", 'r')
string = f.readline()
wordList = string.split(" ")
#for x in wordList:
    #print(x)
word = wordList[random.randint(0,len(wordList)-1)]
wrongTimes = 0
times = 0
guess = []
print ("随机挑选出的单词为:" + word)

while wrongTimes < 6:
    print("请开始你的第" + str(times) + "次猜测")
    print("你已猜错" + str(wrongTimes) + "次")
    print("你已猜对" + str(times - wrongTimes) + "次")
    string = input("Enter your input: ")
    guess.append(string)
    print (guess)
    result = judge(guess,word)
    print (result)
    result = result.replace(' ','')
    times+=1
    if wrongTimes==6:
        print("游戏失败")
        exit(0)
    elif result == word:
        print("恭喜获胜")
        exit(0)

