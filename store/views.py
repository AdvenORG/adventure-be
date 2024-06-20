from django.db.models.deletion import ProtectedError
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import exception_handler

from app_utils.serializers import CategorySerializer, ProductSerializer

from .models import Category, Product


class CustomViewSetMixin:
    def format_response(self, status_code, message, data=None):
        formatted_response = {
            "statusCode": status_code,
            "message": message,
            "data": data,
        }
        return Response(formatted_response, status=status_code)

    def handle_exception(self, exc):
        response = exception_handler(exc, self.get_exception_handler_context())

        if response is not None:
            response.data = {
                "statusCode": response.status_code,
                "message": str(exc),
            }
        else:
            response = self.format_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
            )

        return response


class ProductViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
    CustomViewSetMixin,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        data = self.get_serializer(
            self.queryset, many=True, context={"request": request}
        ).data
        return self.format_response(status.HTTP_200_OK, "Get success", data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self.format_response(status.HTTP_200_OK, "Get success", response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self.format_response(status.HTTP_200_OK, "Update success", response.data)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return self.format_response(
            status.HTTP_200_OK, "Partial update success", response.data
        )

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return self.format_response(status.HTTP_200_OK, "Delete success", response.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.format_response(
            status.HTTP_201_CREATED, "Creation success", serializer.data
        )

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            # You can perform additional operations with the saved instance here if needed
        except Exception as e:
            print("Error saving instance:", e)
            # You can handle the error as needed, like raising an exception or logging it


class CategoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
    CustomViewSetMixin,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        data = self.get_serializer(
            self.queryset, many=True, context={"request": request}
        ).data
        return self.format_response(status.HTTP_200_OK, "Get success", data)

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return self.format_response(
                status.HTTP_200_OK, "Delete success", response.data
            )
        except ProtectedError as e:
            protected_objects = e.protected_objects
            error_message = f"Cannot delete the category because it is referenced by {len(protected_objects)} product(s)."
            return self.format_response(status.HTTP_400_BAD_REQUEST, error_message)
