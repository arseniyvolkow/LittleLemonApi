from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, status
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Cart
from .serializers import *
from .premissions import IsManager, IsDeliveryCrew
from django.db.models import Sum
from datetime import datetime
from .pagination import *
# Create your views here.


class MenuItemsList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    ordering_fields=['price']
    pagination_class = LargeResultsSetPagination
    search_fields=['category__title']

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        return [permission() for permission in permission_classes]



class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        return [permission() for permission in permission_classes]


class CategriesItems(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        return [permission() for permission in permission_classes]


class ManagerListView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer

    def post(self, request):
        permission_classes = [IsManager]
        try:
            username = request.data['username']
            user = get_object_or_404(User, username=username)
            manager = Group.objects.get(name='Manager')
            manager.user_set.add(user)
            return Response({"message": "Now this user is manager"})
        except:
            return Response({"message": "User is not found"}, status.HTTP_404_NOT_FOUND)
        return [permission() for permission in permission_classes]


@api_view(['DELETE'])
@permission_classes([IsManager])
def removeManagerRole(request, pk):
    if pk:
        user = get_object_or_404(User, id=pk)
        manager = Group.objects.get(name='Manager')
        manager.user_set.remove(user)
        return Response({"message": "Manager role removed"}, status.HTTP_200_OK)
    else:
        return Response({"message": "User is not found"}, status.HTTP_404_NOT_FOUND)


class DeliveryCrewListView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer

    def post(self, request):
        permission_classes = [IsManager]
        try:
            username = request.data['username']
            user = get_object_or_404(User, username=username)
            manager = Group.objects.get(name='Delivery crew')
            manager.user_set.add(user)
            return Response({"message": "Now this user is in Delivery crew"})
        except:
            return Response({"message": "User is not found"}, status.HTTP_404_NOT_FOUND)
        return [permission() for permission in permission_classes]


@api_view(['DELETE'])
@permission_classes([IsManager])
def removeDeliveryCrewRole(request, pk):
    if pk:
        user = get_object_or_404(User, id=pk)
        manager = Group.objects.get(name='Delivery crew')
        manager.user_set.remove(user)
        return Response({"message": "Delivery crew role removed"}, status.HTTP_200_OK)
    else:
        return Response({"message": "User is not found"}, status.HTTP_404_NOT_FOUND)


class ListCartItemsView(generics.ListCreateAPIView):
    serializer_class = CartAddItemsSerializer

    def get_queryset(self, *args, **kwargs):
        cart = Cart.objects.filter(user=self.request.user)
        return cart

    def post(self, request, *arg, **kwargs):
        print(request.data)
        serializer = CartAddItemsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = request.data['menuitem']
        quantity = request.data['quantity']
        menuitem = get_object_or_404(MenuItem, id=id)
        price = menuitem.price * int(quantity)
        print(request.user, menuitem, quantity, menuitem.price, price)
        try:
            Cart.objects.create(user=request.user, menuitem=menuitem,
                                quantity=quantity, unit_price=menuitem.price, price=price)
        except:
            return Response({"message": "Already in cart"}, status.HTTP_409_CONFLICT)
        return Response({"message": "Added to cart"}, status.HTTP_201_CREATED)

    def delete(self, request):
        cartitems = Cart.objects.filter(user=request.user)
        cartitems.delete()
        return Response({"message": "Cart items deleted"}, status.HTTP_200_OK)


class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrdersSerializer

    def get_queryset(self, *args, **kwargs):
        if IsManager:
            queryset = Order.objects.all()
            return queryset
        elif IsDeliveryCrew:
            queryset = Order.objects.filter(delivery_crew=self.request.user)
            return queryset
        else:
            queryset = Order.objects.filter(user=self.request.user)
            return queryset

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET' or 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        return [permission() for permission in permission_classes]

    def post(self, request):
        cart = Cart.objects.filter(user=self.request.user)
        total_price = cart.aggregate(total_price=Sum('price'))['total_price']
        print(total_price)
        try:
            order = Order.objects.create(
                user=self.request.user, status=0, total=total_price, date=datetime.now().date())
            try:
                for item in cart:
                    OrderItem.objects.create(
                        order=order, menuitem=item.menuitem, quantity=item.quantity, unit_price=item.unit_price, price=item.price)
                    item.delete()
                return Response({"message": "Ordered"}, status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_409_CONFLICT)


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdersSerializer
    queryset = Order.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsManager | IsDeliveryCrew]
        elif self.request.method == 'PUT':
            permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsManager| IsAdminUser] 
        return [permission() for permission in permission_classes]

    def put(self, request, pk):
        serializer_class = OrdersPutSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        item = get_object_or_404(Order, id=pk)
        item.delivery_crew = request.data('delivery_crew')
        item.save()
        return Response({"message": "Delivery_crew assigned"}, status.HTTP_202_ACCEPTED)

    def patch(self, request, pk):
        item = get_object_or_404(Order, id=pk)
        item.status = not item.status
        return Response({"message": "Delivery status changed"}, status.HTTP_200_OK)

    def destroy(self, request, pk):
        item = get_object_or_404(Order, id=pk)
        item.delete()
        return Response({"message": "Order deleted"}, status.HTTP_204_NO_CONTENT)
