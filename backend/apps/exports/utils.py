import openpyxl

from io import BytesIO

from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from apps.transactions.models import Transaction


def export_transactions_excel(user, month):

    transactions = Transaction.objects.filter(
        user=user,
        date__month=month
    )

    workbook = openpyxl.Workbook()

    worksheet = workbook.active

    worksheet.title = 'Finance Report'

    headers = [
        'Type',
        'Category',
        'Amount',
        'Description',
        'Date'
    ]

    worksheet.append(headers)

    for transaction in transactions:

        worksheet.append([
            transaction.transaction_type,
            transaction.category,
            float(transaction.amount),
            transaction.description,
            str(transaction.date),
        ])

    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = (
        'attachment; filename=finance_report.xlsx'
    )

    return response


def export_transactions_pdf(user, month):

    transactions = Transaction.objects.filter(
        user=user,
        date__month=month
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename=finance_report.pdf'
    )

    pdf = canvas.Canvas(
        response,
        pagesize=letter
    )

    pdf.setFont("Helvetica", 12)

    y = 750

    pdf.drawString(
        200,
        y,
        f"Finance Report - Month {month}"
    )

    y -= 40

    for transaction in transactions:

        text = (
            f"{transaction.date} | "
            f"{transaction.transaction_type} | "
            f"{transaction.category} | "
            f"₹ {transaction.amount}"
        )

        pdf.drawString(50, y, text)

        y -= 20

        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()

    return response