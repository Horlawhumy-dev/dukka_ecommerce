from django.contrib import admin

from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):

    list_display = ('user_involved', 'internal_reference', 'transaction_type', 'date')

    list_display_links = ["user_involved"]


admin.site.register(Transaction, TransactionAdmin)