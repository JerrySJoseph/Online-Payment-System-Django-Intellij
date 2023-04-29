from django.contrib import admin

# Register your models here.
from .models import TransferRequest,Card,BankAccount

admin.site.register([TransferRequest,Card,BankAccount])