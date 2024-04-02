plate=input('enter:')
def check(plate):
    l=''
    for i in range(len(plate)):
        if plate[i].isalpha():
            l=l+plate[i]
    if len(plate)>=2 and len(plate)<=6:
        if  plate[:len(l)].isalpha():
            if plate[:2].isalpha() and plate[len(l)]!='0':
                print('valid')
            else:
                print('invalid')
        else:
            print('invalid')
    else:
        print('invalid')

check(plate)