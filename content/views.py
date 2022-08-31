from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TimeSet, Time_name
from user.models import User
from datetime import datetime
import time
import schedule


class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")
        user = User.objects.filter(email = email).first()

        if user is None:
            return render(request, "user/login.html")

        current = datetime.now().time()
        current_time = current.replace(microsecond=0).isoformat()
        current_sec = (int(current.hour)+9)*360 + int(current.minute)*60 + int(current.second)
        print(current_sec)


        firsttimeset = TimeSet.objects.filter(user_id=user.id, timearea_id='1').first()
        secondtimeset = TimeSet.objects.filter(user_id=user.id, timearea_id='2').first()
        thirdtimeset = TimeSet.objects.filter(user_id=user.id, timearea_id='3').first()
        time_name =  Time_name.objects.filter(user_id=user.id).first()

        first_set = []
        second_set = []
        third_set = []
        first_set.append(dict(time_name = firsttimeset.time_name,
                              time = firsttimeset.time,
                              first_medicine=time_name.first_medicine_name,
                              second_medicine=time_name.second_medicine_name,
                              third_medicine=time_name.third_medicine_name,
                              first_checked = firsttimeset.first_checked,
                              second_checked = firsttimeset.second_checked,
                              third_checked = firsttimeset.third_checked))
        second_set.append(dict(time_name=secondtimeset.time_name,
                               time=secondtimeset.time,
                               first_medicine=time_name.first_medicine_name,
                               second_medicine=time_name.second_medicine_name,
                               third_medicine=time_name.third_medicine_name,
                               first_checked=secondtimeset.first_checked,
                               second_checked=secondtimeset.second_checked,
                               third_checked=secondtimeset.third_checked))
        third_set.append(dict(time_name=thirdtimeset.time_name,
                              time=thirdtimeset.time,
                              first_medicine=time_name.first_medicine_name,
                              second_medicine=time_name.second_medicine_name,
                              third_medicine=time_name.third_medicine_name,
                              first_checked=thirdtimeset.first_checked,
                              second_checked=thirdtimeset.second_checked,
                              third_checked=thirdtimeset.third_checked))
        # 메인 페이지에 섭취중인 약만 보이게 하기
        if firsttimeset.first_checked == False:
            for item in first_set:
                del(item['first_medicine'])
        if firsttimeset.second_checked == False:
            for item in first_set:
                del(item['second_medicine'])
        if firsttimeset.third_checked == False:
            for item in first_set:
                del(item['third_medicine'])

        # 메인 페이지에 섭취중인 약만 보이게 하기
        if secondtimeset.first_checked == False:
            for item in second_set:
                del (item['first_medicine'])
        if secondtimeset.second_checked == False:
            for item in second_set:
                del (item['second_medicine'])
        if secondtimeset.third_checked == False:
            for item in second_set:
                del (item['third_medicine'])

        # 메인 페이지에 섭취중인 약만 보이게 하기
        if thirdtimeset.first_checked == False:
            for item in third_set:
                del (item['first_medicine'])
        if thirdtimeset.second_checked == False:
            for item in third_set:
                del (item['second_medicine'])
        if thirdtimeset.third_checked == False:
            for item in third_set:
                del (item['third_medicine'])


        # 현재시간값 받아오기, 3개의 시간 받아오기, 현재시간하고 각각의 시간 비교해서 True, False 값 변수로 받아서 CONTExt 에 추가하기
        # 시간 split(':')으로 가져와서 시간 분을 초로 바꾸고 비교하기

        t = time.localtime()
        nowTime = time.strftime("%H:%M:%S", t)
        nowtime_list = nowTime.split(':')
        now_seconds = (int(nowtime_list[0]))*3600 + int(nowtime_list[1])*60 + int(nowtime_list[2])+(9*3600)
        first_seconds = (int(firsttimeset.time.strftime('%H'))*3600) +(int(firsttimeset.time.strftime('%M'))*60) + int(firsttimeset.time.strftime('%S'))
        second_seconds = (int(secondtimeset.time.strftime('%H'))*3600) +(int(secondtimeset.time.strftime('%M'))*60) + int(secondtimeset.time.strftime('%S'))
        third_seconds = (int(thirdtimeset.time.strftime('%H'))*3600) +(int(thirdtimeset.time.strftime('%M'))*60) + int(thirdtimeset.time.strftime('%S'))

        if now_seconds <= first_seconds:
            firstcompare = "show"
        else:
            firstcompare = "hide"

        if now_seconds <= second_seconds:
            secondcompare = "show"
        else:
            secondcompare = "hide"

        if now_seconds <= third_seconds:
            thirdcompare = "show"
        else:
            thirdcompare = "hide"






        return render(request, "medicine_project/main.html", context=dict(first_set=first_set, second_set=second_set,
                                                                          third_set=third_set, firstcompare=firstcompare,
                                                                          secondcompare=secondcompare, thirdcompare=thirdcompare,
                                                                          first_seconds=first_seconds, second_seconds=second_seconds,
                                                                          third_seconds=third_seconds, now_seconds=now_seconds,
                                                                          current_time=current_time))
    def reload(self, request):
        schedule.every().day.at().do()

class Add(APIView):
    def get(self, request):

        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")
        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, "user/login.html")
        timeset_list = TimeSet.objects.filter(user_id=user.id).all()
        time_name =  Time_name.objects.filter(user_id=user.id).first()
        firstmedicine = time_name.first_medicine_name
        secondmedicine = time_name.second_medicine_name
        thirdmedicine = time_name.third_medicine_name

        first_time_list = []
        second_time_list = []
        third_time_list = []

        for time in timeset_list:
            if time.timearea_id == 1:
                first_name=time.time_name
                first_time=time.time.isoformat()
                if time.first_checked == True:
                    f_first_checked = True
                else:
                    f_first_checked = False

                if time.second_checked == True:
                    f_second_checked = True
                else:
                    f_second_checked = False

                if time.third_checked == True:
                    f_third_checked = True
                else:
                    f_third_checked = False

                first_time_list.append(dict(
                    first=f_first_checked,
                    second=f_second_checked,
                    third=f_third_checked,
                    firstname=first_name,
                    firsttime=first_time,
                    firstmedicine=firstmedicine,
                    secondmedicine = secondmedicine,
                    thirdmedicine=thirdmedicine

                ))

# ------------------------------------------------------------------------------------------------------
            elif time.timearea_id == 2:
                second_name = time.time_name
                second_time = time.time.isoformat()
                if time.first_checked == True:
                    s_first_checked = True
                else:
                    s_first_checked = False

                if time.second_checked == True:
                    s_second_checked = True
                else:
                    s_second_checked = False

                if time.third_checked == True:
                    s_third_checked = True
                else:
                    s_third_checked = False

                second_time_list.append(dict(
                    first=s_first_checked,
                    second=s_second_checked,
                    third=s_third_checked,
                    secondname=second_name,
                    secondtime=second_time,
                    firstmedicine=firstmedicine,
                    secondmedicine=secondmedicine,
                    thirdmedicine=thirdmedicine

                ))


# ------------------------------------------------------------------------------------------------------
            elif time.timearea_id == 3:
                third_name = time.time_name
                third_time = time.time.isoformat()
                if time.first_checked == True:
                    t_first_checked = True
                else:
                    t_first_checked = False

                if time.second_checked == True:
                    t_second_checked = True
                else:
                    t_second_checked = False

                if time.third_checked == True:
                    t_third_checked = True
                else:
                    t_third_checked = False

                third_time_list.append(dict(
                    first=t_first_checked,
                    second=t_second_checked,
                    third=t_third_checked,
                    thirdname=third_name,
                    thirdtime=third_time,
                    firstmedicine=firstmedicine,
                    secondmedicine=secondmedicine,
                    thirdmedicine=thirdmedicine

                ))
# ------------------------------------------------------------------------------------------------------




        return render(request, "content/addtime.html", context=dict(firsttimes=first_time_list, secondtimes=second_time_list, thirdtimes=third_time_list, timeset = timeset_list))



class UploadSet(APIView):
    def post(self, request):
        button_text = request.data.get('button_text', None)
        b_id = request.data.get('b_id', None)


        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")
        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, "user/login.html")

        firsttimeset = TimeSet.objects.filter(user_id=user.id, timearea_id='1').first()
        secondtimeset = TimeSet.objects.filter(user_id=user.id, timearea_id='2').first()
        thirdtimeset = TimeSet.objects.filter(user_id=user.id, timearea_id='3').first()


        if button_text == 'btn-secondary':
            is_checked = True
        else:
            is_checked = False
# 약 버튼 유무에따라 데이터 저장 ------------------------------------------------------------------------------
        if b_id == 'one_first':
            firsttimeset.first_checked = is_checked
            firsttimeset.save()
        if b_id == 'one_second':
            firsttimeset.second_checked = is_checked
            firsttimeset.save()
        if b_id == 'one_third':
            firsttimeset.third_checked = is_checked
            firsttimeset.save()
 #------------------------------------------------------------------------------------------------------

        if b_id == 'two_first':
            secondtimeset.first_checked = is_checked
            secondtimeset.save()
        if b_id == 'two_second':
            secondtimeset.second_checked = is_checked
            secondtimeset.save()
        if b_id == 'two_third':
            secondtimeset.third_checked = is_checked
            secondtimeset.save()

 #------------------------------------------------------------------------------------------------------

        if b_id == 'three_first':
            thirdtimeset.first_checked = is_checked
            thirdtimeset.save()
        if b_id == 'three_second':
            thirdtimeset.second_checked = is_checked
            thirdtimeset.save()
        if b_id == 'three_third':
            thirdtimeset.third_checked = is_checked
            thirdtimeset.save()

        return Response(status=200)


class Medicine(APIView):

    def post(self, request):

        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")
        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html", None)
        first_name = request.data.get("first_name", None)
        second_name = request.data.get("second_name", None)
        third_name = request.data.get("third_name", None)

        first_t_name = request.data.get("first_t_name", None)
        second_t_name = request.data.get("second_t_name", None)
        third_t_name = request.data.get("third_t_name", None)

        first_time = request.data.get("first_time", None)
        second_time = request.data.get("second_time", None)
        third_time = request.data.get("third_time", None)

        time_name =  Time_name.objects.filter(user_id=user.id).first()

        firsttimeset = TimeSet.objects.filter(user_id=user.id, timearea_id='1').first()
        secondtimeset = TimeSet.objects.filter(user_id=user.id, timearea_id='2').first()
        thirdtimeset = TimeSet.objects.filter(user_id=user.id, timearea_id='3').first()


# 약 이름 설정 --------------------------------------------------------------------------------

        time_name.first_medicine_name = first_name
        time_name.second_medicine_name = second_name
        time_name.third_medicine_name = third_name

        time_name.save()

        firsttimeset.time_name = first_t_name
        firsttimeset.time = first_time
        firsttimeset.save()

        secondtimeset.time_name = second_t_name
        secondtimeset.time = second_time
        secondtimeset.save()

        thirdtimeset.time_name = third_t_name
        thirdtimeset.time = third_time
        thirdtimeset.save()

#-----------------------------------------------------------------------------------------------




        return Response(status=200)

