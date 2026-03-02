from django.http import HttpResponse

def home(request):
    return HttpResponse("BerAuto backend fut. Admin: /admin/")