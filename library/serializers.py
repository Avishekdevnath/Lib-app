from rest_framework import serializers
from .models import Author, Book, Member, BorrowRecord

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'



class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), source='author', write_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = '__all__'
        

class MemberSerializer(serializers.ModelSerializer):
    borrows = BorrowRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = '__all__'

