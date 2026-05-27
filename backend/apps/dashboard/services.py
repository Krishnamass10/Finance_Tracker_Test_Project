from django.db.models import Sum
from apps.transactions.models import Transaction


def get_dashboard_data(user):

    income = Transaction.objects.filter(
        user=user,
        transaction_type='income'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    expense = Transaction.objects.filter(
        user=user,
        transaction_type='expense'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance = income - expense

    recent_transactions = Transaction.objects.filter(
        user=user
    ).order_by('-date')[:5]

    expense_categories = Transaction.objects.filter(
        user=user,
        transaction_type='expense'
    ).values('category').annotate(
        total=Sum('amount')
    )

    context = {
        'income': income,
        'expense': expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'expense_categories': expense_categories,
    }

    return context