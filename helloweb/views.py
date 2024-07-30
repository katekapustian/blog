from django.shortcuts import render
from django.http import HttpResponse


def func():
    return "test func"


# Create your views here.
def index(request):
    number = 100
    title = "Main page"
    context = {"title": title}
    return render(request, "helloweb/index.html", context)

#     return HttpResponse(f"""
#            <h1>Hello from Django!</h1>
#            <h2>Number is {number}</h2>
#            <h2>func {func()}</h2>
#            <a href= "django"> Django</a>
# """)


def django(request):
    return HttpResponse(f"""
               <h1>Hello from Django!</h1>
               <a href= "django">Django</a>
    """)
