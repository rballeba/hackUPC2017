import base64

def to_url(q):
    base64_q = base64.b64encode(bytes(q['question'], 'utf-8')).decode('utf-8')
    return '-'.join([q['orgid'], base64_q, str(q['date'])])

def from_url(url):
    id_, q, d = url.split('-')
    return {
        'question': base64.b64decode(bytes(q, 'utf-8')).decode('utf-8'),
        'date': d,
        'orgid': id_,
    }
