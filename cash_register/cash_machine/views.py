from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ItemSerializer
from .models import Item


class ItemView(APIView):

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response({'items': serializer.data})

    def post(self, request):
        item = request.data.get('item')
        serializer = ItemSerializer(data=item)
        if serializer.is_valid(raise_exception=True):
            item_saved = serializer.save()
        return Response({"success": f"item '{item_saved.title}' created successfully"})

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
