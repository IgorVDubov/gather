import struct 


def getBit(byte,position):
    '''
    return bit at position in byte (from 0)
    '''
    return byte & 1 << position != 0


def packFloatToCDAB(f:float)->list:
    '''
    pack float to 2 words LOW HIGH \n
    return [LOW_16_byte, HIGH_16_byte]
    '''
    b=[i for i in struct.pack('<f',f)]
    return [b[i+1]*256+b[i] for i in range(0,len(b),2)]

def unpackCDABToFloat(twoWords:list,roundCount:int=None)->float:
    '''
    unpack list [LOW_16bit, HIGH_16bit] \n
    return [LOW_16_byte, HIGH_16_byte] \n
    round to roundCount if exist
    '''
    try:
        hex=twoWords[1].to_bytes(2,byteorder='big')+twoWords[0].to_bytes(2,byteorder='big')
    except Exception as e:
        print (f'unpackABCDToFloat: Exception {e} list in parameters: {twoWords}')
        return None
    try:
        result=struct.unpack('!f', hex)[0]
        if roundCount:
            return round(result, roundCount)
        else:
            return result
    except Exception:
        print(f"unpackCDABToFloat: can't unpack {twoWords}")
        return None

def unpackABCDToFloat(twoWords:list,roundCount:int=None)->float:
    '''
    unpack list [LOW_16bit, HIGH_16bit] \n
    return [LOW_16_byte, HIGH_16_byte] \n
    round to roundCount if exist
    '''
    try:
        hex=twoWords[0].to_bytes(2,byteorder='big')+twoWords[1].to_bytes(2,byteorder='big')
    except Exception as e:
        print (f'unpackABCDToFloat: Exception {e} list in parameters: {twoWords}')
        return None
    try:
        result=struct.unpack('!f', hex)[0]
        if roundCount:
            return round(result, roundCount)
        else:
            return result
    except Exception:
        print(f"unpackCDABToFloat: can't unpack {twoWords}")
        return None

def tests():
    a=4.01
    print (f'testing pack/unpackCDABToFloat: {a== unpackCDABToFloat(packFloatToCDAB(a),2)}')

if __name__ == "__main__":
    a=unpackABCDToFloat([0,0],2)
    print (getBit(655,0))

    # tests()
    # r=packFloatToCDAB(29.01)
    # print (r)
    # r=packFloatToCDAB(4.01)
    # print (r)
    # f=unpackCDABToFloat(r,2)
    # print(f)
