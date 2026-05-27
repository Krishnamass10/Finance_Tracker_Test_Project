from django.db.models import Sum

from apps.transactions.models import Transaction


def get_chatbot_response(user, message):

    message = message.lower()

    # Food Expense

    if 'food' in message:

        total_food = Transaction.objects.filter(
            user=user,
            category='food',
            transaction_type='expense'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        return (
            f"You spent ₹ {total_food} on food."
        )

    # Highest Expense Category

    elif 'highest expense' in message:

        expenses = Transaction.objects.filter(
            user=user,
            transaction_type='expense'
        ).values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')

        if expenses:

            highest = expenses[0]

            return (
                f"Your highest expense category is "
                f"{highest['category']} "
                f"with ₹ {highest['total']}."
            )

        return "No expense data found."

    # Savings Advice

    elif 'save' in message:

        food_expense = Transaction.objects.filter(
            user=user,
            category='food',
            transaction_type='expense'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        if food_expense > 5000:

            return (
                "You can reduce food delivery "
                "expenses to improve savings."
            )

        return (
            "Your spending looks balanced this month."
        )

    # Total Expense

    elif 'total expense' in message:

        total = Transaction.objects.filter(
            user=user,
            transaction_type='expense'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        return f"Your total expense is ₹ {total}."

    # Total Income

    elif 'total income' in message:

        total = Transaction.objects.filter(
            user=user,
            transaction_type='income'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        return f"Your total income is ₹ {total}."

    return (
        "Sorry, I didn't understand your question."
    )