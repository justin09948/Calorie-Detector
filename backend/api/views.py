from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ML.main import caloriesCount

class PredictCalView(APIView):
    def post(self, request):
        image_file = request.FILES['image']
        result = caloriesCount(image_file)
        return Response(result)
