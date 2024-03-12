from django.shortcuts import render

def my_view(request):
    # Your view logic goes here
    context = {
        'title': 'My Page Title',  # Example context data
    }
    return render(request, 'index.html', context)
