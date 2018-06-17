from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, FileResponse
import json
import django_rq
from .tasks import create_pdf
from django.conf import settings
from .models import Printer, Check
# Create your views here.


@require_POST
@csrf_exempt
def create_checks(request):
    order = json.loads(request.body.decode())
    printers = Printer.objects.filter(point_id=order['order']['point_id'])

    if not printers.exists():
        return JsonResponse({'error': 'Для данной точки не настроено ни одного принтера'}, status=400)

    if Check.objects.filter(order__order__id=order['order']['id']):
        return JsonResponse({'error': 'Для данного заказа уже созданы чеки'}, status=400)

    # queue = django_rq.get_queue('default')
    for printer in printers:
        check = Check.objects.create(printer_id=printer, type=printer.check_type, order=order, status='NW')
        # queue.enqueue(create_pdf, check)
        create_pdf(check)
    return JsonResponse({'ok': 'Чеки успешно созданы'}, status=200)


def new_checks(request):
    api_key = request.GET['api_key']
    try:
        printer = Printer.objects.get(api_key=api_key)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Ошибка авторизации'})

    checks = Check.objects.filter(printer_id=printer, status='RN')
    result = {
        'checks': [
            {
                'id': check.id,
                'url': '{}/check/?order_id={}&api_key={}&format=pdf'.format(settings.HOST, check.order['order']['id'], printer.api_key)
            } for check in checks
        ]
    }

    return JsonResponse(result, status=200)


def check(request):
    order_id = request.GET['order_id']
    format = request.GET['format']
    api_key = request.GET['api_key']

    try:
        printer = Printer.objects.get(api_key=api_key)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Ошибка авторизация'}, status=401)

    try:
        check = Check.objects.get(order__order__id=int(order_id), printer_id=printer)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Для данного заказа нет чеков'}, status=400)

    if format == 'pdf' and check.status == 'NW':
        return JsonResponse({'error': 'Для данного заказа не сгерерирован чек в формате PDF'}, status=400)

    if format == 'pdf':
        check.status = 'PR'
        check.save()
        return FileResponse(open(check.pdf_file.path, 'rb'), content_type='application/pdf')

    if format == 'html':
        if check.type == 'CL':
            template = 'client_check.html'
        else:
            template = 'kitchen_check.html'
        return render(request, template, {'check': check.order['order']}, content_type='text/html')

