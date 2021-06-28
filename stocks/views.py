from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm

# Create your views here.


def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']

        # pk_d813fd46de154bfb98f61e53739bb493
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_d813fd46de154bfb98f61e53739bb493")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."


        diction= {'api': api}
        return render(request, 'stocks/home.html', context=diction) 

        


    else:
        diction= {'ticker': "Enter a Ticker Symbol Above..."}
        return render(request, 'stocks/home.html', context=diction)





def about(request):
    diction= {}
    return render(request, 'stocks/about.html', context=diction) 


def add_stock(request):
    import requests
    import json
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added"))
            return redirect('add_stock') 

    else:
        ticker = Stock.objects.all() 
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_d813fd46de154bfb98f61e53739bb493")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        diction= {'ticker': ticker, 'output': output}
        return render(request, 'stocks/add_stock.html', context=diction) 


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect('delete_stock') 

def delete_stock(request):
    ticker = Stock.objects.all() 
    diction= {'ticker': ticker}
    return render(request, 'stocks/delete_stock.html', context=diction) 


