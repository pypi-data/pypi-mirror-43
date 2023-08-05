import struct
import binascii
from pyDes import *
import base64

class IdEncrypt:
    NAPI_QUESTION_CRYPT_KEY = 'iVPed<7K'
    NAPI_ARTICLE_CRYPT_KEY  = '^.vAy$TT'
    QB_QUESTION_CRYPT_KEY   = 'lVPed<8K'
    ZYB_CHARGE_CRYPT_KEY    = '^.vAy$TG'
    ZYB_UID_CRYPT_KEY       = '^.vB>$TS'
    ZYB_LECTURE_CRYPT_KEY   = '*)<~0YZS'
    ZYB_OPENID_CRYPT_KEY    = '^.iC$eSC>'
    MAGIC_NUM = 65521
    MAGIC_NUM2 = 65519
    INT32MAX = 4294967296

    def convert(self,s):
        list_h = []
        for c in s:
            print(c)
            list_h.append(str(hex(ord(c))[2:]))
        return ''.join(list_h)

    def encodeQid(self,qid,type=0):
        qid=int(qid)
        if (qid>=self.INT32MAX):
            str=struct.pack('!LLHBBLLHB',qid>>32,qid%self.INT32MAX,qid % self.MAGIC_NUM,0,0) + struct.pack('<LLHB',qid>>32,qid % self.INT32MAX,qid % self.MAGIC_NUM2,0)
        else:
            str=struct.pack('!LHBB',qid,qid % self.MAGIC_NUM,0,0) + struct.pack('<LHB',qid,qid % self.MAGIC_NUM2,0)
        if not type:
            key=self.NAPI_QUESTION_CRYPT_KEY
        else:
            key=self.QB_QUESTION_CRYPT_KEY
        desO=des(key,ECB,padmode=PAD_PKCS5)
        es=desO.encrypt(str)
        res=binascii.hexlify(es)
        res=res.decode()
        return res

    def decodeQid(self,type=0):
        mid=binascii.unhexlify(str)
        if not mid:
            return 0
        if not type:
            key=self.NAPI_QUESTION_CRYPT_KEY
        else:
            key=self.QB_QUESTION_CRYPT_KEY

        desO=des(key,ECB,padmode=PAD_PKCS5)
        es=desO.decrypt(mid)
        qid=0
        qid2=0
        zero1=0
        zero2=0
        zeropad=0
        check=0
        check2=0
        if len(es)==23:
            return
        elif len(es)==15:
            res1 = struct.unpack('!LHBBLHB', es)
            res2 = struct.unpack('LHBBLHB', es)
            qid=res1[0]
            qid2=res2[4]
            check=res1[1]
            check2=res2[5]
            zero1=res1[2]
            zero2=res1[3]
            zeropad=res2[6]
        if zero1 or zero2 or zeropad:
            return 0
        if qid % self.MAGIC_NUM==check and qid2 % self.MAGIC_NUM2==check2 and qid == qid2:
            return qid
        else:
            return 0

    def encodeAQid(self,qid):
        str = struct.pack('!LHBB', qid, qid % self.MAGIC_NUM, 0, 0) + struct.pack('<LH', qid, qid % self.MAGIC_NUM2,0)
        key=self.NAPI_ARTICLE_CRYPT_KEY
        desO = des(key, ECB,pad='\x00', padmode=PAD_NORMAL)
        es = desO.encrypt(str)
        res = binascii.hexlify(es)
        res = res.decode()
        return res

    def decodeAQid(self,str):
        mid = binascii.unhexlify(str)
        if not mid:
            return 0
        key = self.NAPI_ARTICLE_CRYPT_KEY
        desO = des(key, ECB,padmode=PAD_NORMAL)
        es = desO.decrypt(mid)
        res1 = struct.unpack('!LHBBLHBB', es)
        res2 = struct.unpack('LHBBLHBB', es)
        qid = res1[0]
        qid2 = res2[4]
        check = res1[1]
        check2 = res2[5]
        zero1 = res1[2]
        zero2 = res1[3]
        zeropad = res2[6]
        if zero1 or zero2 or zeropad:
            return 0
        if qid % self.MAGIC_NUM==check and qid2 % self.MAGIC_NUM2==check2 and qid == qid2:
            return qid
        else:
            return 0

    def encodeCid(self,qid):
        str = struct.pack('!LHBB', qid, qid % self.MAGIC_NUM, 0, 0) + struct.pack('<LH', qid, qid % self.MAGIC_NUM2,0)
        key=self.ZYB_CHARGE_CRYPT_KEY
        desO = des(key, ECB,pad='\x00', padmode=PAD_NORMAL)
        es = desO.encrypt(str)
        res = binascii.hexlify(es)
        res = res.decode()
        return res

    def decodeCid(self,str):
        mid = binascii.unhexlify(str)
        if not mid:
            return 0
        key = self.ZYB_CHARGE_CRYPT_KEY
        desO = des(key, ECB,padmode=PAD_NORMAL)
        es = desO.decrypt(mid)
        res1 = struct.unpack('!LHBBLHBB', es)
        res2 = struct.unpack('LHBBLHBB', es)
        qid = res1[0]
        qid2 = res2[4]
        check = res1[1]
        check2 = res2[5]
        zero1 = res1[2]
        zero2 = res1[3]
        zeropad = res2[6]
        if zero1 or zero2 or zeropad:
            return 0
        if qid % self.MAGIC_NUM==check and qid2 % self.MAGIC_NUM2==check2 and qid == qid2:
            return qid
        else:
            return 0

    def encodeLid(self,qid):
        str = struct.pack('!LHBB', qid, qid % self.MAGIC_NUM, 0, 0) + struct.pack('<LH', qid, qid % self.MAGIC_NUM2,0)
        key=self.ZYB_LECTURE_CRYPT_KEY
        desO = des(key, ECB,pad='\x00', padmode=PAD_NORMAL)
        es = desO.encrypt(str)
        res = binascii.hexlify(es)
        res = res.decode()
        return res

    def decodeLid(self,str):
        mid = binascii.unhexlify(str)
        if not mid:
            return 0
        key = self.ZYB_LECTURE_CRYPT_KEY
        desO = des(key, ECB,padmode=PAD_NORMAL)
        es = desO.decrypt(mid)
        res1 = struct.unpack('!LHBBLHBB', es)
        res2 = struct.unpack('LHBBLHBB', es)
        qid = res1[0]
        qid2 = res2[4]
        check = res1[1]
        check2 = res2[5]
        zero1 = res1[2]
        zero2 = res1[3]
        zeropad = res2[6]
        if zero1 or zero2 or zeropad:
            return 0
        if qid % self.MAGIC_NUM==check and qid2 % self.MAGIC_NUM2==check2 and qid == qid2:
            return qid
        else:
            return 0

    def encodeOuid(self,qid):
        str = struct.pack('!LHBB', qid, qid % self.MAGIC_NUM, 0, 0) + struct.pack('<LH', qid, qid % self.MAGIC_NUM2,0)
        key=self.ZYB_OPENID_CRYPT_KEY
        desO = des(key, ECB,pad='\x00', padmode=PAD_NORMAL)
        es = desO.encrypt(str)
        res = binascii.hexlify(es)
        res = res.decode()
        return res

    def decodeOuid(self,str):
        mid = binascii.unhexlify(str)
        if not mid:
            return 0
        key = self.ZYB_OPENID_CRYPT_KEY
        desO = des(key, ECB,padmode=PAD_NORMAL)
        es = desO.decrypt(mid)
        res1 = struct.unpack('!LHBBLHBB', es)
        res2 = struct.unpack('LHBBLHBB', es)
        qid = res1[0]
        qid2 = res2[4]
        check = res1[1]
        check2 = res2[5]
        zero1 = res1[2]
        zero2 = res1[3]
        zeropad = res2[6]
        if zero1 or zero2 or zeropad:
            return 0
        if qid % self.MAGIC_NUM==check and qid2 % self.MAGIC_NUM2==check2 and qid == qid2:
            return qid
        else:
            return 0

    def encodeUid(self,qid):
        str = struct.pack('!LHBB', qid, qid % self.MAGIC_NUM, 0, 0) + struct.pack('<LH', qid, qid % self.MAGIC_NUM2,0)
        key=self.ZYB_UID_CRYPT_KEY
        desO = des(key, ECB,pad='\x00', padmode=PAD_NORMAL)
        es = desO.encrypt(str)
        res = binascii.hexlify(es)
        res = res.decode()
        return res

    def decodeUid(self,str):
        mid = binascii.unhexlify(str)
        if not mid:
            return 0
        key = self.ZYB_UID_CRYPT_KEY
        desO = des(key, ECB,padmode=PAD_NORMAL)
        es = desO.decrypt(mid)
        res1 = struct.unpack('!LHBBLHBB', es)
        res2 = struct.unpack('LHBBLHBB', es)
        qid = res1[0]
        qid2 = res2[4]
        check = res1[1]
        check2 = res2[5]
        zero1 = res1[2]
        zero2 = res1[3]
        zeropad = res2[6]
        if zero1 or zero2 or zeropad:
            return 0
        if qid % self.MAGIC_NUM==check and qid2 % self.MAGIC_NUM2==check2 and qid == qid2:
            return qid
        else:
            return 0

if __name__=="__main__":
    id=IdEncrypt()
    id.decodeAQid(b'02fb5bbb7ebd91445bdc4e3eaaa1701c')
