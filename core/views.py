from django.shortcuts import render, HttpResponse

# Create your views here.
def hello(request, nome, idade):
    return HttpResponse("<h1>Hello {}! You are {}</h1>".format(nome, idade))

def sum(request, num1, num2):
    return HttpResponse("<h1>The sum of {} and {} equals {}</h1>".format(num1, num2, num1 + num2))

def subtraction(request, num1, num2):
    return HttpResponse("<h1>The difference of {} and {} equals {}</h1>".format(num1, num2, num1 - num2))

def multiply(request, num1, num2):
    return HttpResponse("<h1>The product of {} and {} equals {}</h1>".format(num1, num2, num1 * num2))

def divide(request, num1, num2):
    return HttpResponse("<h1>The quotient of {} and {} equals {}</h1>".format(num1, num2, num1 / num2))