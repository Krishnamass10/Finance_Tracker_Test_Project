from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from apps.transactions.models import Transaction

from .utils import (
    export_transactions_excel,
    export_transactions_pdf
)


@login_required
def reports_view(request):

    month = request.GET.get('month')

    transactions = []

    total_income = 0
    total_expense = 0
    balance = 0

    if month:

        transactions = Transaction.objects.filter(
            user=request.user,
            date__month=month
        )

        total_income = transactions.filter(
            transaction_type='income'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        total_expense = transactions.filter(
            transaction_type='expense'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        balance = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'selected_month': month,
    }

    return render(
        request,
        'reports.html',
        context
    )


@login_required
def export_excel(request):

    month = request.GET.get('month')

    return export_transactions_excel(
        request.user,
        month
    )


@login_required
def export_pdf(request):

    month = request.GET.get('month')

    return export_transactions_pdf(
        request.user,
        month
    )