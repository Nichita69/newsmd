# from django.contrib.auth.models import User
# from rest_framework.generics import GenericAPIView, ListAPIView
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
#
# from apps.users.serializers import UserSerializer
#
# class RegisterUserView(GenericAPIView):
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)
#     authentication_classes = ()
#
#     def post(self,request,*args,**kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         validated_data = serializer.validated_data
#         user = User.objects.create(
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             username=validated_data['username'],
#             is_superuser=True,
#             is_staff=True
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return Response(UserSerializer(user).data)
#
#
# class UsersListView(ListAPIView, GenericAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = User.objects.all()
#
#
# class UsersItemView(GenericAPIView):
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)
#     authentication_classes = ()
#     queryset = User.objects.all()
