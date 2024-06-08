from functools import wraps
from rest_framework.response import Response

def require_fields(required_fields):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            missing_fields = [field for field in required_fields if field not in request.data]
            if missing_fields:
                return Response({
                    'code': 400,
                    'message': f"The following fields are required: {', '.join(missing_fields)}."
                }, status=400)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def validate_fields(validators):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            for field, validator in validators.items():
                value = request.data.get(field)
                if value and not validator(value):
                    return Response({
                        'code': 400,
                        'message': f"{field} is not valid."
                    }, status=400)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator