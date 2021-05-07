from datetime import datetime
from dateutil.relativedelta import relativedelta

from pprint import pprint

class paynow_qr_object(object):
    def __init__(self, object_id=None, value=''):
        self.object_id = object_id
        self.value = value
        self.template = []

    @property
    def length(self):
        return len(self.value)

    def __str__(self):
        assert self.object_id is not None
        return f'{self.object_id:02d}{self.length:02d}{self.value}'

class paynow_qr_pfi(paynow_qr_object):
    def __init__(self):
        self.object_id = 0

    @property
    def value(self):
        return '01'

class paynow_qr_poim(paynow_qr_object):
    def __init__(self):
        self.object_id = 1

    @property
    def value(self):
        return '11'

class paynow_qr_info(paynow_qr_object):
    def __init__(self, mobile=None):
        assert mobile != None
        self.object_id=26
        self.uid = paynow_qr_object(object_id=0, value='SG.PAYNOW')
        self.v1 = paynow_qr_object(object_id=1, value='0')
        self.mobile = paynow_qr_object(object_id=2, value=f'+65{mobile}')
        self.v3 = paynow_qr_object(object_id=3, value='1')
        self.expiry = paynow_qr_object(
            object_id=4,
            value=(
                datetime.now() + relativedelta(days=+1)
            ).strftime('%Y%m%d')
        )

    @property
    def value(self):
        objects = []
        objects.append(self.uid)
        objects.append(self.v1)
        objects.append(self.mobile)
        objects.append(self.v3)
        objects.append(self.expiry)
        return ''.join([str(o) for o in objects])

class paynow_qr_code(paynow_qr_object):
    def __init__(self, mobile=None, amount=50, comment='NA'):
        assert mobile is not None
        self.objects = []
        self.objects.append(paynow_qr_pfi())
        self.objects.append(paynow_qr_poim())
        self.objects.append(paynow_qr_info(mobile=mobile))
        self.objects.append(paynow_qr_object(
            object_id=52,
            value='0000'
        ))
        self.objects.append(paynow_qr_object(
            object_id=53,
            value='702'
        ))
        self.objects.append(paynow_qr_object(
            object_id=54,
            value=f'{amount:.2f}'
        ))
        self.objects.append(paynow_qr_object(
            object_id=58,
            value='SG'
        ))
        self.objects.append(paynow_qr_object(
            object_id=59,
            value='NA'
        ))
        self.objects.append(paynow_qr_object(
            object_id=60,
            value='Singapore'
        ))
        self.objects.append(paynow_qr_object(
            object_id=62,
            value=str(paynow_qr_object(
                object_id=1,
                value=comment
            ))
        ))

    def crc16(self, data : bytearray, offset , length):
        if data is None or offset < 0 or offset > len(data)- 1 and offset+length > len(data):
            return 0
        crc = 0xFFFF
        for i in range(0, length):
            crc ^= data[offset + i] << 8
            for j in range(0,8):
                if (crc & 0x8000) > 0:
                    crc =(crc << 1) ^ 0x1021
                else:
                    crc = crc << 1
        return crc & 0xFFFF

    def __str__(self):
        s = ''.join([str(o) for o in self.objects])
        s += '6304'
        s += '{:x}'.format(self.crc16(s.encode('ascii'), 0, len(s))).upper()
        return s
