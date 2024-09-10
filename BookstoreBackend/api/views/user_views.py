from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Users

def user_list(request):
    if request.method == 'GET':
        users = Users.objects.all()
        users_data = [{
            'id': user.userid,
            'username': user.username,
            'email': user.email
        } for user in users]
        return JsonResponse(users_data, safe=False)

def user_detail(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(Users, pk=user_id)
        return JsonResponse({
            'id': user.userid,
            'username': user.username,
            'email': user.email,
            'first_name': user.firstname,
            'last_name': user.lastname,
        })
