from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import timedelta
from .models import Author, Book, Member, BorrowRecord
from .serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowRecordSerializer

# Create your views here.

class AuthorViewSet(ModelViewSet):
    """
    Manage Author. 
    - Only Librarian can Access this endpoint.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes=[IsAdminUser]

class BookViewSet(ModelViewSet):
    """
    Manage library books. 
    - Librarians: Full access.
    - Members: View only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

class MemberViewSet(ModelViewSet):
    """
    This end point Manage Member. 
    - Only Librarian can Access this endpoint.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]

class BorrowRecordViewSet(ModelViewSet):
    """
    Manage Borrow Records. 
    - Only Librarian can Access this endpoint with full access.
    """
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAdminUser]

class BorrowView(APIView):
    """
    Manage Borrowing of Books. 
    - Any type users can Access this endpoint.
    """
    permission_classes = [IsAuthenticated]

    def post(self,request):
        book_id=request.data.get('book_id')  
        member_id=request.data.get('member_id')
        try:
            book=Book.objects.get(id=book_id)
            member=Member.objects.get(id=member_id) 

            if book.available_copies < 1:
                return Response({"error" : "No books Available"})
            
            book.available_copies -= 1
            book.save()
            record=BorrowRecord.objects.create(
                book=book,
                member=member,
                due_date=timezone.now() + timedelta(days=14),
                status='Borrowed'
            )
            return Response(BorrowRecordSerializer(record).data,status=status.HTTP_201_CREATED)
        except (Book.DoesNotExist,Member.DoesNotExist):
            return Response({"error":"Book or member not found"})
        
class ReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        try:
            record=BorrowRecord.objects.get(id=pk,return_date__isnull=True)
            record.return_date=timezone.now()
            record.status='Returned'
            record.save()
            book=record.book
            book.available_copies += 1
            book.save()
            return Response({"status":"Book returned Successfully"})
        
        except BorrowRecord.DoesNotExist:
            return Response({"error":"Invalid borrow record"})
        
    