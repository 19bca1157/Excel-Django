from django.shortcuts import render, redirect
from .forms import ExcelFileForm
from .models import ExcelFile
import openpyxl
from datetime import datetime

def home(request):
    date_filter = request.GET.get('date', '')
    files = ExcelFile.objects.all()
    if date_filter:
        files = files.filter(uploaded_at__date=datetime.strptime(date_filter, '%Y-%m-%d').date())

    context = {'files': files, 'date_filter': date_filter}
    return render(request, 'uploader/home.html', context)

def upload_file(request):
    if request.method == 'POST':
        form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExcelFileForm()

    return render(request, 'uploader/upload.html', {'form': form})

def view_file(request, file_id):
    file_obj = ExcelFile.objects.get(id=file_id)
    wb = openpyxl.load_workbook(file_obj.file.path)
    sheet = wb.active
    data = [[cell.value for cell in row] for row in sheet.iter_rows()]

    context = {'data': data, 'file': file_obj}
    return render(request, 'uploader/view.html', context)


