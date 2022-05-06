from django.shortcuts import render
import requests

# Create your views here.
def frontpage(request):
    response = requests.post('http://wm_slicer_cura:5555/cura', json={"one": 1})
    print(response.text)
    return render(request,'core/frontpage.html')

def checkout(request):
    return render(request,'core/checkout.html')

