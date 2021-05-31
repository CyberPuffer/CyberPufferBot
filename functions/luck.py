from binascii import crc32, unhexlify

def get_luck(uid, date):
    seed = uid + date.year + date.month + date.day
    width = seed.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % seed)
    luck_level = crc32(s) % 5 + 1
    luck_text = '今日人品：{}{}'.format('★' * luck_level, '☆' * (5 - luck_level))
    return luck_text