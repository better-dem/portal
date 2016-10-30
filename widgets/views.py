from django.shortcuts import render
from django.http import HttpResponse
from .forms import SimpleTestWidgetForm
import os
import sys

# Create your views here.
def demo_map(request):
    return render(request,
                  'widgets/demo_map.html',
                  {'api_key' : os.environ["GOOGLE_MAPS_API_KEY"]})

def demo_poly_mark(request):
    return render(request,
                  'widgets/demo_poly_mark.html',
                  {'api_key' : os.environ["GOOGLE_MAPS_API_KEY"]})

def simple_test_widget(request):
    if request.method == 'POST':
        form = SimpleTestWidgetForm(request.POST)
        if form.is_valid():
            sys.stderr.write("valid form")
            sys.stderr.write(str(form.cleaned_data))
            sys.stderr.flush()
            return HttpResponse("Form is Valid")
        else:
            sys.stderr.write("invalid form")
            sys.stderr.write(str(form.cleaned_data))
            sys.stderr.flush()
            return render(request, 'widgets/simple_test_widget.html', {'form': form})
    else:
        form = SimpleTestWidgetForm()
        return render(request, 'widgets/simple_test_widget.html', {'form': form})
