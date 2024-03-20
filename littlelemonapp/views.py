
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from django.contrib.auth.models import  User,Group
from  .serializers import UserSignupSerializer,UserLoginSerializer,MenuitemsSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import BasePermission
from .models import Menuitem
from django.shortcuts import get_object_or_404


class DenyAccessPermission(BasePermission):
    def has_permission(self, request, view):
        # Deny access for POST, PUT, PATCH, and DELETE methods
        return request.method not in ['POST', 'PUT', 'PATCH', 'DELETE']





#view for creating user or SignUp
class  RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class= UserSignupSerializer
    
    def post(self,request,*args,**kwargs):
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
         # Extract user data from the request
        if not password:
            return Response({'email Is Necssecery'},status=status.HTTP_206_PARTIAL_CONTENT)
            

        if not email:
            return Response({'email Is Necssecery'},status=status.HTTP_206_PARTIAL_CONTENT)
        if not first_name:
            return Response({'First_ name'},status=status.HTTP_206_PARTIAL_CONTENT)
        #checking if Neccery data Is Availeble if not return status 206 partial Content

         
       
        

        serializer = self.get_serializer(data=request.data) 
        #Retriving the serialised in to serailiser Variable 

        if serializer.is_valid():
            user= serializer.save()
            #saving the data in to database


            user = User.objects.get(username=serializer.data['username'])
            #getting the data from data base for create object 
            tocken_obj = Token.objects.create(user=user)
            #tocken is created for the user return the token
            group = Group.objects.get(name='Customer')
            user.groups.add(group)


            return Response({'data': serializer.data,'token': str(tocken_obj) ,'Group ': str(group)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class SingleUserView(RetrieveAPIView):

    serializer_class= UserSignupSerializer
    permission_classes = [IsAuthenticated]



    def get(self, request, *args, **kwargs):

        token = request.headers.get('Authorization', '').split(' ')[1]   #tacking the tocken from request 
        try:
            token_obj = Token.objects.get(key=token)    #geting the tocken object 
            user = token_obj.user                       #geting the user that assigned for the tocken
            return Response({'username': user.username, 'email': user.email  , "First Name": user.first_name})
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=400)
    



class LoginUserView(CreateAPIView):
    queryset = User.objects.all()  # Make sure to import User model
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        
        username = request.data.get('username')# Retrieve username and password from request data
        password = request.data.get('password')
        
        if not username or not password:# Check if username and password are provided
            return Response({'error': 'Username or password is missing'}, status=status.HTTP_400_BAD_REQUEST)
      
        user = authenticate(username=username, password=password)  # Authenticate user
        if user is not None:
            existing_token = user.auth_token if hasattr(user, 'auth_token') else None# Check if the user already has an existing token          
            if existing_token:# Check if the user already has an existing token
                existing_token.delete()
            new_token = Token.objects.create(user=user)# Generate a new token for the user
            
            user.auth_token = new_token# If an existing token is found, replace it with the new token
            user.save()# Save the new token to the user
            # Return a success response with the token
            return Response({'token': new_token.key}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

class groupmixin:
    def get_user_group(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization', '').split(' ')[1]  
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            if user.groups.filter(name='deliverycrew').exists():
                return 'deliverycrew'
            elif user.groups.filter(name='Manger').exists():
                return 'Manger'
            elif user.groups.filter(name='Customer').exists():
                return 'Customer'
            else:
                return None
        except (Token.DoesNotExist, IndexError):
            return None
        
            

class MenuItemView(groupmixin,ListAPIView,CreateAPIView,UpdateAPIView):
    queryset  =    Menuitem.objects.all()
    serializer_class =MenuitemsSerializer

    def get_permissions(self):
        if self.get_user_group(self.request) == 'Manger':
            return [IsAuthenticated()]

        else:
            return [DenyAccessPermission(),IsAuthenticated()]
        
    
        
    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        price = request.data.get('price')
        category = request.data.get('category')

        # Check if all required data is provided
        if not (title and price and category):
            return Response({'error': 'Please provide all necessary data'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self,request,*args, **kwargs):
        try: 
            id = request.data.get('id')
            item = get_object_or_404(Menuitem, id=id)  # Retrieve single object or return 404 if not found
        
        except id.ObjectDoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuitemsSerializer(instance=item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         

    def patch(self, request, *args, **kwargs):
        try: 
            id = request.data.get('id')
            item = get_object_or_404(Menuitem, id=id)  # Retrieve single object or return 404 if not found
        
        except id.ObjectDoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuitemsSerializer(instance=item, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class MenuSingleSerch(groupmixin,ListAPIView):
    serializer_class = MenuitemsSerializer 
    def get_permissions(self):
        if self.get_user_group(self.request) == 'Manger':
            return [IsAuthenticated()]

        else:
            return [DenyAccessPermission(),IsAuthenticated()]
    def get_queryset(self):
        item_name = self.request.query_params.get('itemName')
        if item_name:
            try:
                item = Menuitem.objects.filter(title__iexact=item_name)
                return item
            except Menuitem.DoesNotExist:
                return Menuitem.objects.none()         
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        


class ManagerUsers(groupmixin,ListAPIView,CreateAPIView,DestroyAPIView):
    serializer_class = UserSerializer


    def get_permissions(self):
        if self.get_user_group(self.request) == 'Manger':
            return [IsAuthenticated()]
        else:
            return [DenyAccessPermission()]

    def list(self, request, *args, **kwargs):
        try:
           Manager = Group.objects.get(name='Manger')
           manager_users = User.objects.filter(groups=Manager)
           serialized_manager_users = UserSerializer(manager_users, many=True)
        except Group.DoesNotExist:
            return Response({'message': 'Manager group not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized_manager_users.data)
    

    def post(self,request,*args, **kwargs):
        username = request.data.get('username')
        if not username:
             return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)  
        try:
            user = User.objects.get(username=username)   
            manager_group, created = Group.objects.get_or_create(name='Manger')
            user.groups.clear()  
            user.groups.add(manager_group)
            return Response({'message': f'User "{username}" assigned to manager group successfully'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': f'User "{username}" does not exist'}, status=status.HTTP_404_NOT_FOUND)
           

    def delete(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(pk=user_id)
            manager_group = Group.objects.get(name='Manager')
            
            if manager_group in user.groups.all():
                user.groups.remove(manager_group)
                return Response({'message': f'User "{user}" removed from Manager group'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f'User "{user}" is not in the Manager group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'error': 'Manager group does not exist'}, status=status.HTTP_404_NOT_FOUND)





class DeliveryCrewUsers(ListAPIView,CreateAPIView,DestroyAPIView):
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        try:
           DeliveryCrew = Group.objects.get(name='Delivery-Crew')
           DeliveryCrew_users = User.objects.filter(groups=DeliveryCrew)
           serialized_DeliveryCrew = UserSerializer(DeliveryCrew_users, many=True)
        except Group.DoesNotExist:
            return Response({'message': 'Manager group not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized_DeliveryCrew.data)

    def post(self, request, *args, **kwargs):
        userName = request.data.get('username')
       
        if not userName:
            return Response({'error': 'Username or ID is required to do the Action'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username = userName)
            DeliveryCrew = Group.objects.get(name='Delivery-Crew')
            user.groups.add(DeliveryCrew)
            return Response({'message': f'User "{userName}" assigned to Delivery-Crew group successfully'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': f'User "{userName}" does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    
    def delete(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
            delivery_group = Group.objects.get(name='Delivery-Crew')
            
            if delivery_group in user.groups.all():
                user.groups.remove(delivery_group)
                return Response({'message': f'User "{user}" deleted from Delivery-Crew group'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f'User "{user}" is not in the Delivery-Crew group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist for that ID'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'error': 'Delivery-Crew group does not exist'}, status=status.HTTP_404_NOT_FOUND)

     

        


    
   
        
    



        
            
            


    

    


        
      
        
        