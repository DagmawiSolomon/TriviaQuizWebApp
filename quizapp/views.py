from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .models import Quiz, Questions, Answer, Result
from django.core.paginator import Paginator
import datetime
import time

# create your views here.

def home(request):
    quiz = Quiz.objects.get(active=True, completed=False)
    # for q in quiz.question.all():
    #     print(q)
    start = quiz.start_date
    end = quiz.end_date
    start_month = start.strftime("%b")
    start_day = start.strftime("%d")
    start_year = start.strftime("%y")
    start_hour = start.strftime("%H")
    start_minute = start.strftime("%M")
    start_second = start.strftime("%S")
    end_month = end.strftime("%b")
    end_day = end.strftime("%d")
    end_year = end.strftime("%y")
    end_hour = end.strftime("%H")
    end_minute = end.strftime("%M")
    end_second = end.strftime("%S")
    if request.user.is_authenticated:
        result = Result.objects.get(user=request.user, quiz=quiz)
    else:
         result = ''
    context = {"quiz": quiz, "start_month": start_month, "start_day": start_day, "start_year": start_year,
               "start_hour": start_hour, "start_minute": start_minute, "start_second": start_second,
               "end_day": end_day, "end_year": end_year, "end_month": end_month,
               "end_hour": end_hour, "end_minute": end_minute, "end_second": end_second, "result":result}
    return render(request, "quizapp/home.html", context)


def quiz(request, pk):
    quiz = Quiz.objects.get(id=pk, active=True, completed=False)
    question = Questions.objects.filter(quiz=quiz)
    time_allowed = quiz.time_allowed
    paginator = Paginator(question, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    result_qs = Result.objects.filter(quiz = quiz, user = request.user)
    if result_qs.exists():
        print(result_qs)
    else:
        result = Result(user=request.user, quiz=quiz, score=0)
        result.save()
    if request.method == "POST":
        answer_inputted = request.POST.get("choice")
        print(request.POST.get("response-time"), "response_time")
        if request.POST.get("input") == "Finish":
            answer = Answer.objects.filter(text=answer_inputted)
            if answer[1].correct:
                print(answer[1], "answer2")
                r = Result.objects.get(user=request.user, quiz=quiz)
                print(r.score, "before")
                r.score += 100
                r.points += 1
                print(r.points, "----------------")
                r.save()
                print(r.score, "after")
            elif not answer[1].correct:
                r = Result.objects.get(user=request.user, quiz=quiz)
                r.score += 0
                r.save()
            else:
                r = Result.objects.get(user=request.user, quiz=quiz)
                r.score += 0
                r.save()
                print("none")
            set_result_tocompleted = Result.objects.get(user=request.user, quiz=quiz)
            set_result_tocompleted.completed = True
            set_result_tocompleted.save()
            return redirect("/result")
        else:
            if answer_inputted != None:
                answer = Answer.objects.filter(text=answer_inputted)
                print(answer)
                if answer[0].correct:
                    r = Result.objects.get(user = request.user, quiz = quiz)
                    r.score += 100
                    r.points += 1
                    r.save()
                elif not answer[0].correct:
                    print("wrong")
                    r = Result.objects.get(user=request.user, quiz=quiz)
                    r.score += 0
                    print(r.points)
                    r.save()
                else:
                    print("none")
                    r = Result.objects.get(user=request.user, quiz=quiz)
                    r.score += 0
                    r.save()
                results = Result.objects.get(user = request.user, quiz = quiz)
                results_qset = results.score
                context = {"time_allowed": time_allowed, "page_obj": page_obj, "answer": answer, "result": results_qset, 'res' : results}
                return render(request, "quizapp/quiz.html", context)

            else:
                HttpResponse(answer_inputted)
                results = Result.objects.get(user=request.user, quiz=quiz)
                results_qset = results.score
                context = {"time_allowed": time_allowed, "page_obj": page_obj,"result": results_qset , "res": results}
                return render(request, "quizapp/quiz.html", context)
    else:
        results = Result.objects.get(user=request.user, quiz=quiz)
        results_qset = results.score
        context = {"quiz": quiz, "page_obj": page_obj, "time_allowed": time_allowed, "result": results_qset, "res": results}
        return render(request, "quizapp/quiz.html", context)


def result(request):
    quiz = Quiz.objects.get(active=True, completed=False)
    questions = Questions.objects.filter(quiz=quiz)
    q_count = questions.count()
    result = Result.objects.get(user=request.user, quiz=quiz)
    results = result.score
    point = result.points
    context = {"result": results, "point": point, "q_count":q_count}
    return render(request, "quizapp/result.html", context)


def leaderboard(request):
    context = {}
    return render(request, "quizapp/statistics.html", context)

