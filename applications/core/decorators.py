from django.shortcuts import redirect


def check_profile_status(list_of_fields, redirect_name='personal-page', check_type=True):
    def wrapper_f(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                for field in list_of_fields:
                    if check_type:
                        if getattr(request.user.profile, field):
                            return redirect(redirect_name)
                    else:
                        if not getattr(request.user.profile, field):
                            return redirect(redirect_name)
            else:
                return redirect('main-page')
            return func(request, *args, **kwargs)
        return wrapper
    return wrapper_f


def access_to_immatrikulation_page(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.profile.summer_holidays_start or not request.user.profile.summer_holidays_end:
            return redirect('personal-page')
        return func(request, *args, **kwargs)
    return wrapper


def superuser_access_forbidden(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('/admin/')
        return func(request, *args, **kwargs)
    return wrapper
