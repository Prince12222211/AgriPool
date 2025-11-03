from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def transporter_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'transporter_profile'):
            return function(request, *args, **kwargs)
        messages.error(request, 'Access denied. Transporter account required.')
        return redirect('accounts:dashboard')
    return wrap

def farmer_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'farmer_profile'):
            return function(request, *args, **kwargs)
        messages.error(request, 'Access denied. Farmer account required.')
        return redirect('accounts:dashboard')
    return wrap