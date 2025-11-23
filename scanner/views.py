from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

def index(request):
    return render(request, "scanner/index.html")

@staff_member_required
def purchase_offline(request):
    return render(request, "scanner/purchase.html")