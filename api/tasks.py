from django.conf import settings
import requests
import json
import base64
from django.template.loader import render_to_string


def create_pdf(check):
    url = settings.PDF_CONV_URL
    template = 'client_check.html' if check.type == 'CL' else 'kitchen_check.html'

    check_html = render_to_string(template, {'check': check.order['order']})

    contents = base64.b64encode(check_html.encode()).decode('utf-8')

    data = {
        'contents': contents,
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    link = 'pdf/{}_{}.pdf'.format(check.order['order']['id'], check.type)
    with open(settings.MEDIA_URL + link, 'wb') as f:
        f.write(response.content)

    check.status = 'RN'
    check.pdf_file = settings.MEDIA_URL + link
    check.save()


