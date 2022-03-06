from django.urls import path
from .views.folder_views import FoldersView, FolderDetailView
from .views.file_views import FilesView, FileDetailView
from .views.user_views import SignUpView, SignInView, SignOutView, ChangePasswordView

urlpatterns = [
  	# Restful routing
    path('folders/', FoldersView.as_view(), name='folders'),
    path('folders/<int:pk>/', FolderDetailView.as_view(), name='folder_detail'),
    path('files/', FilesView.as_view(), name='files'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file_detail'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('change-pw/', ChangePasswordView.as_view(), name='change-pw')
]
