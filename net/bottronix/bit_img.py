# 
test = bytearray([0x00,0xFF,0x00,0xFF,0x00,0xFF,0X00,0x00, \
                0XFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0X00, \
                0x00,0XFF,0x00,0xFF,0x00,0xFF,0x00,0xFF, \
                0X00,0x00,0XFF,0x00,0xFF,0XFF,0XFF,0X00,
                0x00,0xFF,0xFF,0X00,0xFF])
# 01010100, 10101010, 01010101, 00101110
# 54,AA,55,2E,68
class BitImg :
    
    """

    """
    
    def __init__(self):
        pass
        
    def get_bit_bytes(self,src):

        # padding
        pad_offset = len(src)%8;
        if(pad_offset>0):
            for p in range(8-pad_offset):
                src.append(0x00)
    
        result = bytearray()
        val=0
        count = 0
        for i in range(len(src)):
            shift = 7-i%8
            bit = 0x00
            if(src[i]>127):
                bit = 0x01
            
        #     print(src[i])
        #     print(bin(bit))
            
            val = (val | ((src[i] & bit) << shift)) & 0xFF
        #     print(bin((val)))
        #     print(hex(val))
            count+=1
            if(count==8):
#                 print(bin(val))
                val ^= 0xFF;
#                 print(bin(val))
                result.append(val)
#                 print(bin(result[len(result)-1]))
                val=0
                count=0
            #     print("===================")
            
        return result
    
if __name__ == '__main__':
    bi = BitImg()
    bi.get_bit_bytes(test)