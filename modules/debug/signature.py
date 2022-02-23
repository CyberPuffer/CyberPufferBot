def check_signature(text, magic):
    from base64 import b64encode
    magic_enc = b64encode(magic, altchars=b'-_').decode('ASCII')
    return text.find(magic_enc)


def decode_signature(text, pos):
    from base64 import b64decode
    from re import subn
    xargs_length_enc = text[pos-16:pos-14] + '=='
    xargs_length = int.from_bytes(
        b64decode(xargs_length_enc, altchars=b'-_'), 'big')
    signature = text[pos-16:pos+96+xargs_length]
    signature_regex = '(["\']{3})' + signature + '\\1|#' + signature
    code, result = subn(signature_regex, '', text, count=1)
    return (code, signature, result)


def verify_signature(code, pubkey, signature):
    from base64 import b64decode
    from uuid import UUID
    from nacl.signing import VerifyKey
    from hashlib import sha3_512
    from datetime import datetime
    from nacl.exceptions import BadSignatureError
    chksum = sha3_512()
    frag_a = b64decode(signature[:24], altchars=b'-_')
    frag_b = b64decode(signature[24:112], altchars=b'-_')
    flags = frag_a[1]
    cmd = frag_b[64]
    args = frag_b[65]
    chksum.update(frag_a[:2] + frag_b[64:])

    id = UUID(bytes=frag_a[2:18])
    magic = id.node.to_bytes(6,'big')
    time = datetime.fromtimestamp((id.time - 0x01b21dd213814000)*100/1e9)
    chksum.update(id.bytes)

    xargs = b64decode(signature[112:], altchars=b'-_')
    chksum.update(xargs)

    chksum.update(code.encode("utf-8"))
    verify_sig = frag_b[:64]
    verify_key = VerifyKey(pubkey)
    try:
        verify_key.verify(chksum.digest(), verify_sig)
        return {'valid': True,  'code': code,
                'flags': flags, 'cmd': cmd,
                'args': args,   'id': id,
                'time': time,   'magic': magic,
                'xargs': xargs}
    except BadSignatureError:
        return {'valid': False}
