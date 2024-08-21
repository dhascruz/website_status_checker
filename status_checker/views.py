# Create your views here.
import requests
from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *




def index(request):
    websites = Website.objects.all()
    # rev_cnt=Transactions.objects.filter(status=1).all().count()
    # sal_cnt=Transactions.objects.filter(status=2).all().count()
    # sub_cnt=Transactions.objects.filter(status=3).all().count()
    # sto_cnt=Transactions.objects.filter(status=4).all().count()

    #today = date.today()
    
       

    paginator = Paginator(websites, 2000)
    page = request.GET.get('page')
    try:
        websites = paginator.page(page)
    except PageNotAnInteger:
        websites = paginator.page(1)
    except EmptyPage:
        websites = paginator.page(paginator.num_pages)
    context = {
        'websites': websites,
    }
    return render(request, 'index.html', context)







def check_status(request):
    websites = Website.objects.all()
    for website in websites:
        try:
            response = requests.get(website.url)
            website.status = response.status_code
        except requests.exceptions.RequestException as e:
            website.status = "Error"
        website.save()

    context = {
        'websites': websites,
    }
    return render(request, 'status_list.html', context)

def add_website(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('check_status')
    else:
        form = WebsiteForm()
    return render(request, 'add_website.html', {'form': form})

def edit_website(request, pk):
    website = get_object_or_404(Website, pk=pk)
    if request.method == 'POST':
        form = WebsiteForm(request.POST, instance=website)
        if form.is_valid():
            form.save()
            return redirect('check_status')
    else:
        form = WebsiteForm(instance=website)
    return render(request, 'edit_website.html', {'form': form})

def delete_website(request, pk):
    website = get_object_or_404(Website, pk=pk)
    if request.method == 'POST':
        website.delete()
        return redirect('check_status')
    return render(request, 'delete_website.html', {'website': website})
