# -*- coding: utf-8 -*-

def get_luck(uid, date):
    from binascii import crc32, unhexlify
    seed = uid + date.year + date.month + date.day + (date.hour + 1) // 2
    width = seed.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % seed)
    luck_level = crc32(s) % 5 + 1
    luck_text = u'当前人品：{}{}'.format(u'★' * luck_level, u'☆' * (5 - luck_level))
    return luck_text