from rest_framework import serializers
from django.contrib.auth.models import User,Group
from .models import Menuitem

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])  # Use set_password method on the user object
        user.save()
        return user
    
    def createSuperUser(self,validated_data):
        pass





class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model =User
        fields =['username' , 'password']



class MenuitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menuitem
        fields =['id' ,'title', 'price' , 'category']





class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']






class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)  

    class Meta:
        model =User
        fields =['id' ,'username', 'email', 'first_name', 'last_name','groups']