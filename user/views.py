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
                               time_name = "์์นจ",
                               first_checked=True,
                               second_checked=True,
                               third_checked=True,
                               time = "09:00:00",
                               timearea_id=1)
        TimeSet.objects.create(user_id=user_id,
                               time_name="์ ์ฌ",
                               first_checked=True,
                               second_checked=True,
                               third_checked=True,
                               time="12:00:00",
                               timearea_id=2)
        TimeSet.objects.create(user_id=user_id,
                               time_name="์ ๋",
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
            return Response(status=404, data=dict(message="ํ์์ ๋ณด๊ฐ ์๋ชป๋์์ต๋๋ค."))

        if user.check_password(password):
            # Todo ๋ก๊ทธ์ธ์ ํ๋ค. ์ธ์ ๋๋ ์ฟ ํค์ ๋ฃ๋๋ค.
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=404, data=dict(message="ํ์์ ๋ณด๊ฐ ์๋ชป๋์์ต๋๋ค."))

class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")