import requests, hgtk, random


history = []
playing = True
#키 발급은 https://krdict.korean.go.kr/openApi/openApiInfo
apikey = 'FD2A20282D8087CD52E57772223DC20D'


def midReturn(val, s, e):
    if s in val:
        val = val[val.find(s)+len(s):]
        if e in val: val = val[:val.find(e)]
    return val


def midReturn_all(val, s, e):
    if s in val:
        tmp = val.split(s)
        val = []
        for i in range(0, len(tmp)):
            if e in tmp[i]: val.append(tmp[i][:tmp[i].find(e)])
    else:
        val = []
    return val

def findword(query):
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&pos=1&q=' + query
    response = requests.get(url)
    ans = []
    

    words = midReturn_all(response.text,'<item>','</item>')
    for w in words:
    
        if not (w in history):           
          
            word = midReturn(w,'<word>','</word>')
            pos = midReturn(w,'<pos>','</pos>')
            if len(word) > 1 and pos == '명사' and not word in history:
                ans.append(w)
    if len(ans)>0:
        return random.choice(ans)
    else:
        return ''


def findwordtwo(query,root):
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&pos=1&q=' + query
    response = requests.get(url)
    ans = []
    
   
    words = midReturn_all(response.text,'<item>','</item>')
    for w in words:
        
        if not (w in history):           
            
            word = midReturn(w,'<word>','</word>')
            pos = midReturn(w,'<pos>','</pos>')
            if word == root and len(word) > 1 and pos == '명사' and not word in history:
                ans.append(w)
    if len(ans)>0:
        return random.choice(ans)
    else:
        return ''

def checkexists(query):
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&sort=popular&num=100&pos=1&q=' + query
    response = requests.get(url)
    ans = ''

    
    words = midReturn_all(response.text,'<item>','</item>')
    for w in words:
        
        if not (w in history):           
            
            word = midReturn(w,'<word>','</word>')
            pos = midReturn(w,'<pos>','</pos>')
            if len(word) > 1 and pos == '명사' and word == query: ans = w

    if len(ans)>0:
        return ans
    else:
        return ''



    

def anothermeaning(query,original):
    start = query[0]
    ans = findwordtwo(start+'*',query)

    if ans == '' : return
        
    anothermean = midReturn(ans, '<word>', '</word>')
    anotherdef = midReturn(ans, '<definition>', '</definition>') 

    if original==anotherdef : return
    
    history.append(anothermean)

    print(query, '의 다른 뜻>', '\n('+anotherdef+')\n')
    


def anotherword(query):
    start = query[0]

    for i in range(2):

        ans = findword(start + '*')

        plusword = midReturn(ans, '<word>', '</word>') 
        plusdef = midReturn(ans, '<definition>', '</definition>') 

        history.append(plusword)
    
        print(start, '(으)로 시작하는 말>', plusword, '\n('+plusdef+')\n')

    
    
    


print('''
==========================================
사전 데이터 제공: 국립국어원 한국어기초사전

<단어 게임>

- - - 조건 - - -
1.단어를 제시하면 그에 따른 설명이 나옵니다
2.1을 수행한후,입력된 단어의 다른의미나, 그 단어로 시작하는 단어2개가 추가로 출력됩니다
3.'/종료'을 입력하면 종료되며, '/재개'를 입력하여 게임을 다시 시작할 수 있습니다.
- - - 규칙 - - -
1. 사전에 등재된 명사여야 합니다
2. 단어의 길이는 두 글자 이상이어야 합니다
3. 이미 사용한 단어를 다시 사용할 수 없습니다
4. 추가로 출력된 단어도 이미 사용한 단어로 간주합니다. 
==========================================
''')

answord = ''
anothermean=''
plusword = ''



while True:

    wordOK = False

    while(not wordOK):
        query = input(' > ')
        wordOK = True
        
        if query == '/종료':
            playing = False
            print('프로그램 종료!!')
            break
        elif query == '/재개':
            history = []
            answord = ''
            print('프로그램 다시시작!!')       
            wordOK = False
        else:         
            if query == '':
                wordOK = False

                if len(history)==0:
                    print('아무것도 입력하지 않았음! 단어입력필요.')
                    
            else:
                    
                if len(query) == 1:
                    wordOK = False
                    print('두 글자이상이 되어야함')

                if query in history:
                    wordOK = False
                    print('이미 입력한 단어')
                    

                if wordOK:
                
                    ans = checkexists(query)
                    if ans == '':
                        wordOK = False
                        print('유효한 단어를 입력해 주십시오')
                    else:
                        print('(' + midReturn(ans, '<definition>', '</definition>') + ')\n')
                        original = midReturn(ans, '<definition>', '</definition>')
                        anothermeaning(query,original)
                        anotherword(query)
                        
    history.append(query)
    
    

