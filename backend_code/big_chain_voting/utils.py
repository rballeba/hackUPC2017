import base64
import qrcode
import uuid

def to_url(q):
    base64_q = base64.urlsafe_b64encode(q['question'])
    return '-'.join([q['orgid'], base64_q, str(q['date'])])

def from_url(url):
    id_, q, d = url.split('-')
    return {
        'question': base64.urlsafe_b64encode(q),
        'date': d,
        'orgid': id_,
    }

def url_to_qr(text, filename=None):
    if not filename:
        filename = uuid.uuid4().hex + '.png'
    img = qrcode.make(text)
    img.save(filename)
    return filename


