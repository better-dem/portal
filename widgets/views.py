from django.shortcuts import render
from django.http import HttpResponse, Http404
from .forms import SimpleTestWidgetForm
import os
import sys
import json

# def ajax_autocomplete(request):
#     stuff = {'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Deleware', 'Florida', 'Georgia'}
#     if request.is_ajax():
#         sys.stderr.write("Received autocomplete request:"+str(request.body)+"\n")
#         sys.stderr.flush()
#         v = request.body
#         k, v = request.body.split('=')
#         sys.stderr.write("k: "+k+", v: "+v+"\n")
#         sys.stderr.flush()
#         if k.strip() == "query":
#             str_beginning = v.strip().replace('+',' ').lower()
#             # query for objects that begin with str_beginning
#             ans = json.dumps({"query": str_beginning, "suggestions": [i.lower() for i in stuff if i.lower().startswith(str_beginning)]})
#             sys.stderr.write("ans:"+str(ans)+"\n")
#             sys.stderr.flush()
#             return HttpResponse(ans, content_type="application/json")
#         else:
#             return HttpResponse("I can't handle that type of input:"+str(k))
#     else:
#         return HttpResponse("this should be an ajax post")

### The following views are only for testing purposes
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
