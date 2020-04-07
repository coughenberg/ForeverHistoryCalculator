import re
from datetime import datetime


# Where functions are called based on input string
def mathIt(maths, patterns):
    save_maths = maths
    
    if (re.search(r'.*exit.*', maths)):
        print('exiting...')
        return 'exit'
    
    if (re.search(r'.*[a-z]|[A-Z].*', maths)):
        print('plz do not add characters :(\nmaths only plz')
        return maths

    maths = mathFind(maths, patterns)
    count = 20
    while(maths[-1:] == '0' or maths[-1:] == '.' and count >= 0):
        count = count - 1
        maths = maths[:len(maths) - 1]
    if (not count):
        print('error truncating')
    print(maths)

    history = open("calculator_history.txt", "w")
    history.write(str(datetime.now()).split('.')[0] + '\n\n' + save_maths + '\n= ' + maths)
    history.close()
    
    print('done')

def mathFind(maths, patterns):
    found = re.search(patterns[0], maths)
    if (found):
        maths = par(found.span(), patterns, maths)

    found = re.search(patterns[1], maths)
    if (found):
        maths = mul(found.span(), patterns[1], maths)

    found = re.search(patterns[2], maths)
    if (found):
        maths = div(found.span(), patterns[2], maths)

    found = re.search(patterns[3], maths)
    if (found):
        maths = add(found.span(), patterns[3], maths)

    found = re.search(patterns[4], maths)    
    if (found):
        maths = sub(found.span(), patterns[4], maths)
    
    return maths

#                     Here:||
# can break if sends in (1*2(3+4))
def par(substr, patterns, maths):
    # x, y = substr
    # submaths = maths[x+1:y-1]
    # submaths = mathFind(submaths, patterns)
    # if (not re.search(r'[+]|[-]|[*]|[/]', maths[x])):
    #     submaths = '*' + submaths
    # maths = maths[:x] + submaths + maths[y:]
    # print(maths)
    # found = re.search(patterns[5], maths)
    # if (found):
    #     maths = par(found.span(), patterns, maths)
    return maths

def mul(substr, pattern, maths):
    x, y = substr
    submaths = maths[x:y]
    submaths = submaths.split('*')
    ans = float(submaths[0]) * float(submaths[1])
    maths = maths[:x] + str(ans) + maths[y:]
    found = re.search(pattern, maths)
    if (found):
        maths = mul(found.span(), pattern, maths)
    return maths

def div(substr, pattern, maths):
    x, y = substr
    submaths = maths[x:y]
    submaths = submaths.split('/')
    ans = float(submaths[0]) / float(submaths[1])
    maths = maths[:x] + str(ans) + maths[y:]
    found = re.search(pattern, maths)
    if (found):
        maths = div(found.span(), pattern, maths)
    return maths

def add(substr, pattern, maths):
    x, y = substr
    submaths = maths[x:y]
    submaths = submaths.split('+')
    ans = float(submaths[0]) + float(submaths[1])
    maths = maths[:x] + str(ans) + maths[y:]
    found = re.search(pattern, maths)
    if (found):
        maths = add(found.span(), pattern, maths)
    return maths

def sub(substr, pattern, maths):
    x, y = substr
    submaths = maths[x:y]
    submaths = submaths.split('-')
    ans = float(submaths[0]) - float(submaths[1])
    maths = maths[:x] + str(ans) + maths[y:]
    found = re.search(pattern, maths)
    if (found):
        maths = sub(found.span(), pattern, maths)
    return maths

if __name__ == "__main__":
    patterns = []
    patterns.append(re.compile(r'[(].*[)]'))
    patterns.append(re.compile(r'\d+(\.\d+)?[*]\d+(\.\d+)?'))
    patterns.append(re.compile(r'\d+(\.\d+)?[/]\d+(\.\d+)?'))
    patterns.append(re.compile(r'\d+(\.\d+)?[+]\d+(\.\d+)?'))
    patterns.append(re.compile(r'\d+(\.\d+)?[-]\d+(\.\d+)?'))
    patterns.append(re.compile(r'[(].*[)$]'))
    maths = ''
    while (maths != 'exit'):
        maths = input('\n: ')
        maths = ''.join(maths.split(' '))
        maths = mathIt(maths, patterns)
    print('Thanks, come again soon!')
