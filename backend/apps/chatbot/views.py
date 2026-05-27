from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .engine import get_chatbot_response


@login_required
def chatbot_page(request):

    return render(
        request,
        'chatbot.html'
    )


@login_required
def chatbot_api(request):

    if request.method == 'POST':

        message = request.POST.get('message')

        response = get_chatbot_response(
            request.user,
            message
        )

        return JsonResponse({
            'response': response
        })

    return JsonResponse({
        'response': 'Invalid request'
    })