from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.http import HttpResponse, FileResponse

from .serializers import ItemSerializer
from .models import Item, Receipt
from collections import Counter
from datetime import datetime
import pdfkit
import qrcode

def make_pdf(html):
    # нужно установить wkhtmltopdf.exe что бы конвертировать в .pdf
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    return pdfkit.from_string(html, False, configuration=config)

def get_html(id_list, products, receipt):
    data = list()
    c = Counter(id_list)
    summ = 0
    for product in products:
        summ += product.price * c[product.pk]
        data.append(dict({
            'title': product.title,
            'cost': summ,
            'counter': c[product.pk]
        }))
    return render_to_string('cash_receipt.html',
                            {'items': data, 'summ': summ, 'date': receipt.datetime.strftime("%d-%m-%Y %H:%M")})

def make_qr(input_data):
    print(input_data)
    qr = qrcode.QRCode(
        version=2,
        box_size=50,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    return qr.make_image(fill='black', back_color='white')

class ItemView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response({'items': serializer.data})

    def post(self, request):
        id_list = request.data.get('items')
        obj = Receipt(data=id_list, datetime=datetime.now())
        obj.save()
        img = make_qr(f'http://127.0.0.1:8000/api/get_receipt/{obj.pk}')
        img.save('qrcode001.png')
        return FileResponse(open('qrcode001.png', 'rb'))

    def put(self, request, pk):
        saved_item = get_object_or_404(Item.objects.all(), pk=pk)
        data = request.data.get('item')
        serializer = ItemSerializer(instance=saved_item, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            item_saved = serializer.save()
        return Response({"success": f"item {item_saved.title} updated successfully"})

    def delete(self, request, pk):
        item = get_object_or_404(Item.objects.all(), pk=pk)
        item.delete()
        return Response({"message": f"item with id {pk} has been deleted."})


class ReceiptView(APIView):
    def get(self, request, pk):
        receipt = get_object_or_404(Receipt.objects.all(), pk=pk)
        id_list = receipt.data
        products = Item.objects.filter(pk__in=id_list)
        html = get_html(id_list, products, receipt)
        pdf = make_pdf(html)
        response = HttpResponse(pdf, content_type='application/pdf')
        return response
