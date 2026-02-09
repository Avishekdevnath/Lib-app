from django.urls import path, include
from rest_framework.routers import DefaultRouter
from library.views import AuthorViewSet, BookViewSet, MemberViewSet, BorrowRecordViewSet, BorrowView, ReturnView

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
router.register('members', MemberViewSet)
router.register('borrow-records', BorrowRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('borrow/', BorrowView.as_view()),
    path('return/<int:pk>/', ReturnView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]