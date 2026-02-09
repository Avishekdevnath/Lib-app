from django.db import models
from django.contrib.auth.models import timezone
from datetime import timedelta

# Create your models here.

class Author(models.Model):
    name= models.CharField(max_length=100)
    biography = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author=models.ForeignKey(Author, on_delete=models.CASCADE,related_name='books')
    category=models.CharField(max_length=100,blank=True)    
    availability_status=models.BooleanField(default=True)
    total_copies= models.PositiveIntegerField(default=1)
    available_copies= models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title
    
class Member(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    membership_date=models.DateField(default=timezone.now)  

    def __str__(self):
        return self.name   
    
class BorrowRecord(models.Model):
    STATUS_CHOICES = (
        ('Borrowed','Borrowed'),
        ('Returned','Returned'),
        ('Overdue','Overdue'),
    )    
    book= models.ForeignKey(Book,on_delete=models.CASCADE,related_name='borrows'),
    member= models.ForeignKey(Member,on_delete=models.CASCADE,related_name='borrow_records'),
    borrow_date=models.DateTimeField(default=timezone.now),
    return_date=models.DateTimeField(blank=True,null=True),
    due_date=models.DateTimeField(),
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Borrowed')

    def __str__(self):
        return f"{self.member.name} borrowed {self.book.title}"