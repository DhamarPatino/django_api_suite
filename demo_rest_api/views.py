from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': True}) # Ejemplo de item inactivo


class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.',
                'message': 'Debe incluir los campos "name" y "email".'}, 
                status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
    
class DemoRestApiItem(APIView):
    def put(self, request, item_id):
        data = request.data
        index = next((i for i, item in enumerate(data_list) if item['id'] == item_id), None)

        if index is None:
            return Response({
                'error': 'Elemento no encontrado.',
                'message': f'No existe un elemento con id "{item_id}".'
            }, status=status.HTTP_404_NOT_FOUND)
        if 'id' not in data or data['id'] != item_id:
            return Response({'error': 'El campo "id" es obligatorio y debe coincidir con el de la URL.'}, status=status.HTTP_400_BAD_REQUEST)

        updated_item = {
            'id': item_id,
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'is_active': data.get('is_active', True),
        }

        data_list[index] = updated_item
        return Response({'message': 'Elemento reemplazado correctamente.', 'data': updated_item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        item = next((item for item in data_list if item['id'] == item_id), None)
        if item is None:
            return Response({
                'error': 'Elemento no encontrado.',
                'message': f'No se encontró un elemento con id "{item_id}".'
            }, status=status.HTTP_404_NOT_FOUND)
        
        for key in ['name', 'email', 'is_active']:
            if key in request.data:
                item[key] = request.data[key]

        return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        item = next((item for item in data_list if item['id'] == item_id), None)
        if item is None:
            return Response({
                'error': 'Elemento no encontrado.',
                'message': f'No se pudo eliminar. El ID "{item_id}" no corresponde a ningún elemento.'
            }, status=status.HTTP_404_NOT_FOUND)

        item['is_active'] = False
        return Response({
            'message': 'Elemento eliminado lógicamente.',
            'data': item
        }, status=status.HTTP_200_OK)