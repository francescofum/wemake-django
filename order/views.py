from django.shortcuts import render

# Create your views here.

def checkout(request):
    '''
        Main entry point for checkout
    '''

    if(request.method == 'GET'):
        context = {
            # 'vendor':vendor,
            # 'printers':printers
        }        
        return render(request,'checkout.html', context)