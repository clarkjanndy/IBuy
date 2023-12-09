from django.contrib import messages
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from backend.permissions import IsAdminOrReadOnly
from backend.serializers import CategorySerializer, UniformSerializer, UniformImageSerializer
from backend.models import Category, Uniform, UniformImage

__all__ = ['CategoryListCreate', 'CategoryById', 'UniformListCreate', 'UniformById', 'UniformImageListCreate', 'UniformImageById']

class CategoryListCreate(ListCreateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        
        messages.success(request, f"Category {data.get('name')} created successfully!")
        return Response({
            "status": "success", 
            "data": data
        })
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
class CategoryById(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Category.objects.all()
    lookup_field='pk'
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        
        messages.success(request, "Category updated succesfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })

class UniformListCreate(ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Uniform.objects.all()
    serializer_class = UniformSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        messages.success(request, "Uniform created successfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
class UniformById(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Uniform.objects.all()
    lookup_field='pk'
    serializer_class = UniformSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        
        messages.success(request, "Uniform updated succesfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })

class UniformImageListCreate(ListCreateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = UniformImage.objects.all()
    serializer_class = UniformImageSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        uniform = get_object_or_404(Uniform, pk = kwargs['pk'])
        
        serializer = self.serializer_class(data = data)
        serializer.is_valid()
        serializer.save(uniform = uniform)

        messages.success(request, "Image uploaded successfully!")
        return Response({
            "status": "success", 
            "data": serializer.data
        })
    
    def get(self, request, *args, **kwargs):
        uniform = get_object_or_404(Uniform, pk = kwargs['pk'])
        query = self.get_queryset().filter(uniform = uniform)
        serializer = self.serializer_class(query, many = True)
        return Response({
            "status": "success", 
            "data": serializer.data
        })
    
class UniformImageById(GenericAPIView):
    permission_classes = (IsAdminUser, )
    queryset = UniformImage.objects.all()
    serializer_class = UniformImageSerializer

    def get(self, request, *args, **kwargs):
        uniform = get_object_or_404(UniformImage, uniform = kwargs['uniform_pk'], pk = kwargs['pk'])
        serializer = self.serializer_class(uniform)
        return Response({
            "status": "success", 
            "data": serializer.data
        })

    def delete(self, request, *args, **kwargs):
        uniform = get_object_or_404(UniformImage, uniform = kwargs['uniform_pk'], pk = kwargs['pk'])
        uniform.delete()

        msg = 'Image deleted succesfully'
        messages.success(request, msg)
        return Response({
            "status": "success", 
            "data": {
                "message": msg
            }
        })
    
 

