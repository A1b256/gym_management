#products/views.py

from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from .serializers import ProductSerializer
from .models import GymProducts
from user_auth.models import CustomUserRegistration
from rest_framework.parsers import FormParser, MultiPartParser
from gym_details.models import GymDetails
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='get',
    operation_description="Fetch products with optional filters. You can filter by gym_id, admin_id, and product_id.",
    manual_parameters=[
        openapi.Parameter('gym_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='uuid', description='Gym ID (UUID)'),
        openapi.Parameter('admin', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='uuid', description='Admin ID (UUID)'),
        openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='uuid', description='Product ID (UUID)'),
    ],
    responses={
        200: openapi.Response(
            description="Successful response",
            examples={
                "application/json": [
                    {
                        "id": "product-id",
                        "name": "Product Name",
                        "type": "Product Type",
                        "desc": "Product Description",
                        "image": "http://example.com/image.jpg",
                        "reviews": "Product Reviews",
                        "stock": 100,
                        "price": "19.99",
                        "stripe_price_id": "stripe-price-id",
                        "stripe_product_id": "stripe-product-id",
                        "gym": "gym-id",
                        "admin": "admin-id"
                    }
                ]
            }
        ),
        400: "Bad Request",
        404: "Not Found"
    }
)
@swagger_auto_schema(
    method='post',
    operation_description="Add a new product. Requires Admin ID and Gym ID.",
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Product name', required=True),
        openapi.Parameter('type', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Product type', required=True),
        openapi.Parameter('desc', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Product description', required=True),
        openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Product image', required=True),
        openapi.Parameter('reviews', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Product reviews', required=True),
        openapi.Parameter('stock', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='Product stock', required=True),
        openapi.Parameter('price', openapi.IN_FORM, type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Product price', required=True),
        openapi.Parameter('gym_id', openapi.IN_FORM, type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='Gym ID (UUID)', required=True),
        openapi.Parameter('admin', openapi.IN_FORM, type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='Admin ID (UUID)', required=True),
    ],
    responses={
        201: openapi.Response(description='Product added successfully'),
        400: openapi.Response(description='Bad Request'),
    }
)
@swagger_auto_schema(
    method='put',
    operation_description="Update an existing product. Requires Admin ID, Gym ID, and Product ID.",
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Product name'),
        openapi.Parameter('type', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Product type'),
        openapi.Parameter('desc', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Product description'),
        openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Product image'),
        openapi.Parameter('reviews', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Product reviews'),
        openapi.Parameter('stock', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='Product stock'),
        openapi.Parameter('price', openapi.IN_FORM, type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Product price'),
        openapi.Parameter('admin', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Admin ID', required=True),
        openapi.Parameter('gym_id', openapi.IN_FORM, type=openapi.TYPE_STRING, format='uuid', description='Gym ID (UUID)', required=True),
        openapi.Parameter('product_id', openapi.IN_FORM, type=openapi.TYPE_STRING, format='uuid', description='Product ID (UUID)', required=True),
    ],
    responses={
        200: openapi.Response(description='Product updated successfully'),
        400: openapi.Response(description='Bad Request'),
        404: openapi.Response(description='Not Found'),
    }
)
@swagger_auto_schema(
    method='delete',
    operation_description="Delete a product. Requires Admin ID, Gym ID, and Product ID.",
    manual_parameters=[
        openapi.Parameter('admin', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='uuid', description='Admin ID (UUID)'),
        openapi.Parameter('gym_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='uuid', description='Gym ID (UUID)'),
        openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='uuid', description='Product ID (UUID)'),
    ],
    responses={
        204: openapi.Response(description='Product deleted successfully'),
        400: openapi.Response(description='Bad Request'),
        404: openapi.Response(description='Not Found'),
    }
)
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([FormParser, MultiPartParser])
def manage_products(request):
    try:
        if request.method == "GET":
            gym_id = request.query_params.get('gym_id')
            admin_id = request.query_params.get('admin')
            product_id = request.query_params.get('product_id')

            if gym_id and not GymDetails.objects.filter(id=gym_id).exists():
                return Response({"error": "Gym ID not found"}, status=status.HTTP_404_NOT_FOUND)

            if admin_id and not CustomUserRegistration.objects.filter(id=admin_id, is_staff=True).exists():
                return Response({"error": "Admin ID not found or not an admin user"}, status=status.HTTP_404_NOT_FOUND)

            if product_id and not GymProducts.objects.filter(id=product_id).exists():
                return Response({"error": "Product ID not found"}, status=status.HTTP_404_NOT_FOUND)

            if product_id:
                product = get_object_or_404(GymProducts, id=product_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)

            if admin_id and gym_id:
                admin = CustomUserRegistration.objects.get(id=admin_id, is_staff=True)
                gym = GymDetails.objects.get(id=gym_id, admin=admin)
                products = get_list_or_404(GymProducts, Gym=gym, admin=admin)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            if gym_id:
                gym = GymDetails.objects.get(id=gym_id)
                products = get_list_or_404(GymProducts, Gym=gym)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            products = GymProducts.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            admin_id = request.data.get('admin')
            gym_id = request.data.get('gym_id')
            if not admin_id or not gym_id:
                return Response({"error": "Admin ID and Gym ID are required"}, status=status.HTTP_400_BAD_REQUEST)

            admin = CustomUserRegistration.objects.get(id=admin_id, is_staff=True)
            gym = GymDetails.objects.get(id=gym_id, admin=admin)

            data = request.data.copy()
            data['Gym'] = gym_id
            serializer = ProductSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product added successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "PUT":
            admin_id = request.data.get('admin')
            gym_id = request.data.get('gym_id')
            product_id = request.data.get('product_id')
            if not admin_id or not gym_id or not product_id:
                return Response({"error": "Admin ID, Gym ID, and Product ID are required"}, status=status.HTTP_400_BAD_REQUEST)

            admin = CustomUserRegistration.objects.get(id=admin_id, is_staff=True)
            gym = GymDetails.objects.get(id=gym_id, admin=admin)
            gym_product = get_object_or_404(GymProducts, admin_id=admin_id, Gym=gym, id=product_id)

            serializer = ProductSerializer(gym_product, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product details updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            admin_id = request.query_params.get('admin')
            gym_id = request.query_params.get('gym_id')
            product_id = request.query_params.get('product_id')

            if not admin_id or not gym_id or not product_id:
                return Response({"error": "Admin ID, Gym ID, and Product ID are required"}, status=status.HTTP_400_BAD_REQUEST)

            admin = CustomUserRegistration.objects.get(id=admin_id, is_staff=True)
            gym = GymDetails.objects.get(id=gym_id, admin=admin)
            gym_product = GymProducts.objects.get(id=product_id, admin=admin, Gym=gym)
            gym_product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except CustomUserRegistration.DoesNotExist:
        return Response({"error": "Admin ID not found or not an admin user"}, status=status.HTTP_404_NOT_FOUND)
    except GymDetails.DoesNotExist:
        return Response({"error": "Gym ID not found for the given admin"}, status=status.HTTP_404_NOT_FOUND)
    except GymProducts.DoesNotExist:
        return Response({"error": "Product ID not found for the given admin and gym"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)