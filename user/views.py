from django.forms import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from content.models import TimeSet, Time_name
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.exceptions import ValidationError
import json

class Idcheck(APIView):
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response(status=404)
        else:
            return Response(status=200)




class Join(APIView):
    def get(self, request):

        return render(request, "user/join.html")

    def post(self, request):
        email = request.data.get("email", None)
        name = request.data.get("name", None)
        password = request.data.get("password", None)


        User.objects.create(email=email,
                            name=name,
                            password=make_password(password)
                            )

        user = User.objects.filter(email = email).first()
        user_id = user.id
        Time_name.objects.create(user_id = user_id,)
        TimeSet.objects.create(user_id = user_id,
                               time_name = "아침",
                               first_checked=True,
                               second_checked=True,
                               third_checked=True,
                               time = "09:00:00",
                               timearea_id=1)
        TimeSet.objects.create(user_id=user_id,
                               time_name="점심",
                               first_checked=True,
                               second_checked=True,
                               third_checked=True,
                               time="12:00:00",
                               timearea_id=2)
        TimeSet.objects.create(user_id=user_id,
                               time_name="저녁",
                               first_checked=True,
                               second_checked=True,
                               third_checked=True,
                               time="18:00:00",
                               timearea_id=3)

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # Todo 로그인을 했다. 세션 또는 쿠키에 넣는다.
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")