import classes
import time



def parseAttrParams(attrParam):
    if isinstance(attrParam, str):                                     #аттрибут - связь 
        s=''
        for i in range(0,len(attrParam)):
            if attrParam[i]=='.':
                break
        first=attrParam[:i+(1 if len(attrParam)==1 else 0)]
        other=attrParam[i+1:]
        print(f'{i=},{first=},{other=}')
        try:
            BindChannel=int(first)
            if not other:
                attr=None
            else:
                attr=other
        except ValueError:
            BindChannel='self'
            attr=first

        print(f'{attrParam=}: {BindChannel=},{attr=}')

    elif not(attrParam) or isinstance(attrParam, (int, float)):   #аттрибут - число или None
        print (f'{attrParam=}')

if __name__=='__main__':
    parseAttrParams('123.attr.b')
    parseAttrParams('attr.b')
    parseAttrParams('b')
    parseAttrParams(2)