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
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

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
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    def get_object(self, id):
        # CORREGIDO: Usar data_list en lugar de demo_data
        for item in data_list:
            if item["id"] == id:
                return item
        return None

    def get(self, request, id):
        """Obtener un elemento específico por ID"""
        item = self.get_object(id)
        if not item:
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # Solo devolver si está activo
        if not item.get('is_active', False):
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(item, status=status.HTTP_200_OK)

    def put(self, request, id):
        item = self.get_object(id)
        if not item or not item.get('is_active', False):
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        
        # Validación de campos requeridos
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validación de email
        if not data['email'] or '@' not in data['email']:
            return Response({'error': 'Email inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Preservar el ID original y is_active
        original_id = item['id']
        original_is_active = item['is_active']
        
        # Reemplazar completamente excepto el ID y is_active
        item.clear()
        item.update(data)
        item['id'] = original_id
        item['is_active'] = original_is_active
        
        return Response({"message": "Elemento actualizado completamente", "data": item}, status=status.HTTP_200_OK)

    def patch(self, request, id):
        item = self.get_object(id)
        if not item or not item.get('is_active', False):
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        
        # Validación de email si se proporciona
        if 'email' in data and (not data['email'] or '@' not in data['email']):
            return Response({'error': 'Email inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar parcialmente (no permitir cambiar id ni is_active)
        for k, v in data.items():
            if k not in ['id', 'is_active']:
                item[k] = v
                
        return Response({"message": "Elemento actualizado parcialmente", "data": item}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        item = self.get_object(id)
        if not item or not item.get('is_active', False):
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # CORREGIDO: Usar 'is_active' en lugar de 'active' para consistencia
        item["is_active"] = False  # Eliminación lógica
        return Response({"message": "Elemento eliminado lógicamente"}, status=status.HTTP_200_OK)