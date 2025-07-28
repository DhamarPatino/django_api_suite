from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

# Create your views here.

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "votes"  # Cambia este nombre según tu colección en Firebase

    def get(self, request):
        # Referencia a la colección
        ref = db.reference(self.collection_name)

        # Obtiene todos los elementos de la colección
        data = ref.get()

        # Convierte el dict a lista, o lista vacía si no hay datos
        items = list(data.values()) if data else []

        # Devuelve un arreglo JSON
        return Response(items, status=status.HTTP_200_OK)

    def post(self, request):
        # Obtiene los datos del cuerpo de la solicitud
        data = request.data.copy()

        # Obtiene la fecha y hora actual y la formatea en español
        now = datetime.now()
        am_pm = "a. m." if now.strftime("%p") == "AM" else "p. m."
        timestamp = now.strftime(f"%d/%m/%Y, %I:%M:%S {am_pm}").lower()

        # Añade el timestamp al objeto
        data["timestamp"] = timestamp

        # Referencia a la colección
        ref = db.reference(self.collection_name)

        # Guarda el objeto y obtiene el ID generado
        new_obj = ref.push(data)
        obj_id = new_obj.key

        # Devuelve el ID y el estado 201 Created
        return Response({"id": obj_id}, status=status.HTTP_201_CREATED)
