from django.urls import path
from .views import RegisterUserView,SingleUserView,LoginUserView,MenuItemView,MenuSingleSerch,ManagerUsers,DeliveryCrewUsers


urlpatterns = [
path('users',RegisterUserView.as_view(),name= 'register'),
path('users/users/me',SingleUserView.as_view(),name ='user'),
path('token/login',LoginUserView.as_view(),name='login'),
path('menu-items',MenuItemView.as_view(),name ="menu"),
path('menu-items/', MenuSingleSerch.as_view(), name="menusingle"),
path('groups/manager/users',ManagerUsers.as_view(),name="managerusers"),
path('groups/delivery-crew/users',DeliveryCrewUsers.as_view(),name="Delivery-Crew")

]