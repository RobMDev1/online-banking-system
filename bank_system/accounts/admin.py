from django.contrib import admin
from .models import BankAccount, Loan
from accounts import models
from django.db.models import Sum
from django.utils.timezone import now


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_id', 'email', 'balance', 'has_loan', 'loan_amount', 'loan_percent', 'total_loan_amount')
    search_fields = ('user__username', 'email')
    list_filter = ('has_loan',)
    readonly_fields = ('account_id',)
    list_editable = ('balance', 'has_loan', 'loan_amount', 'loan_percent')

    def total_loan_amount(self, obj):
        total_loan = Loan.objects.filter(user=obj.user, status='approved').aggregate(total=Sum('amount'))['total']
        return total_loan if total_loan else 0.00

    total_loan_amount.admin_order_field = 'total_loan_amount'
    total_loan_amount.short_description = 'Total Loan Amount'

admin.site.register(BankAccount, BankAccountAdmin)


class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'approved_date', 'request_date', 'total_repayable')
    list_filter = ('status',)
    actions = ['approve_loan', 'reject_loan']

    def approve_loan(self, request, queryset):
        for loan in queryset.filter(status='pending'):
            loan.status = 'approved'
            loan.save()

        self.message_user(request, "Selected loans have been approved and accounts updated.")

def reject_loan(self, request, queryset):
    queryset.update(status='rejected')
    self.message_user(request, "Selected loans have been rejected.")


admin.site.register(Loan, LoanAdmin)