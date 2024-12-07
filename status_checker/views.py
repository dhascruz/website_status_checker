# Create your views here.
import csv
import requests
from celery import shared_task
from django.utils.timezone import now
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from io import StringIO


from background_task import background



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



# 



def check_status(request):
    websites = Website.objects.all()
    # for website in websites:
    #     try:
    #         check_website_status(website.id)
    #         #response = requests.get(website.url)
    #         #website.status = response.status_code
    #     except requests.exceptions.RequestException as e:
    #         website.status = "Error"
    #     website.save()

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

def test_web(request, pk):
    print("dhas")



def check_website(request, pk):

    website = get_object_or_404(Website, pk=pk)
    
    try:
        website = Website.objects.get(id=pk)
        response = requests.head(website.url, timeout=10)  # Use HEAD request for quick status check
        if response.status_code == 200:
            website.status = 'Up'
        else:
            website.status = f'Down ({response.status_code})'
    except requests.RequestException:
        website.status = 'Down (Error)'
    except Website.DoesNotExist:
        return 'Website not found'
    website.last_checked = now()
    website.save()


    return redirect('check_status')


# View to handle CSV upload and bulk import
def bulk_import_view(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # Save the file temporarily
        fs = FileSystemStorage()
        file_path = fs.save(csv_file.name, csv_file)
        file_url = fs.url(file_path)

        # Parse the file and bulk import
        to_create = []
        errors = []

        with open(fs.path(file_path), newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get('name')
                url = row.get('url')

                if not name or not url:
                    errors.append(f"Missing data in row: {row}")
                    continue
                else:
                    to_create.append(Website(name=name, url=url))

                # #if check_status(url):
                 
                # else:
                #     errors.append(f"Invalid URL in row: {row}")

        # Bulk create all valid records
        Website.objects.bulk_create(to_create)

        # Return the result as JSON
        return JsonResponse({
            'message': f"Imported {len(to_create)} records successfully.",
            'errors': errors
        })

    return render(request, 'bulk_import.html')



#@shared_task

def check_website_status(website_id):
    try:
        website = Website.objects.get(id=website_id)
        response = requests.head(website.url, timeout=10)  # Use HEAD request for quick status check
        if response.status_code == 200:
            website.status = 'Up'
        else:
            website.status = f'Down ({response.status_code})'
    except requests.RequestException:
        website.status = 'Down (Error)'
    except Website.DoesNotExist:
        return 'Website not found'
    website.last_checked = now()
    website.save()
    return f"Checked {website.url}: {website.status}"


@background(schedule=60) 
def check_all_websites():
    websites = Website.objects.all()
    for website in websites:
        try:
            website = Website.objects.get(id=website.id)
            response = requests.head(website.url, timeout=10)  # Use HEAD request for quick status check
            if response.status_code == 200:
                website.status = 'Up'
            else:
                website.status = f'Down ({response.status_code})'
        except requests.RequestException:
            website.status = 'Down (Error)'
        except Website.DoesNotExist:
            return 'Website not found'
        website.last_checked = now()
        website.save()

