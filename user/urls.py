from django.urls import path
from user import views
 
urlpatterns = [
    path('user/list/', views.UserListView.as_view(), name='user_list'),
    path('user/create/', views.UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]


urlpatterns = [
    path('users/', views.UserListCreateAPIView.as_view(), name='user_list_create'),
    path('users/<int:pk>', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user_retrieve_update_destroy'),
]


