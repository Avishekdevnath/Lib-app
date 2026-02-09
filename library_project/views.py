from django.shortcuts import redirect

def root_view(request):
    return redirect('api-root')
