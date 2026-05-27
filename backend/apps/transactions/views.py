from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Transaction
from .forms import TransactionForm


@login_required
def transaction_list(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')

    context = {
        'transactions': transactions
    }

    return render(request, 'transactions.html', context)


@login_required
def add_transaction(request):

    if request.method == 'POST':

        form = TransactionForm(request.POST)

        if form.is_valid():

            transaction = form.save(commit=False)

            transaction.user = request.user

            transaction.save()

            return redirect('transactions')

    else:
        form = TransactionForm()

    context = {
        'form': form
    }

    return render(request, 'add_transaction.html', context)


@login_required
def edit_transaction(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user
    )

    if request.method == 'POST':

        form = TransactionForm(
            request.POST,
            instance=transaction
        )

        if form.is_valid():
            form.save()
            return redirect('transactions')

    else:
        form = TransactionForm(instance=transaction)

    context = {
        'form': form
    }

    return render(request, 'edit_transaction.html', context)


@login_required
def delete_transaction(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user
    )

    transaction.delete()

    return redirect('transactions')