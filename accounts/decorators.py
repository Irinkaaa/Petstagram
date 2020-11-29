from django.shortcuts import redirect


def user_required(ModelClass):
    def decorator(view_func):
        def wrapper(request, pk, *args, **kwargs):
            model_object = ModelClass.objects.get(pk=pk)
            if model_object.user.user_id == request.user.id:
                return view_func(request, pk, *args, **kwargs)
            return redirect('login')
        return wrapper
    return decorator
