from django.contrib import admin
from accounts.models import Account, Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "balance")
    list_display_links = ("id", "username")
    search_fields = ("username", "id")
    list_per_page = 25


admin.site.register(Account, AccountAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "reciever", "transferredAmount")
    search_fields = ("id", "reciever")
    list_per_page = 25


admin.site.register(Transaction, TransactionAdmin)