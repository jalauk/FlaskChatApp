from flask import request
from app.utils.helper import httpResponse

def validate(schema,query_type="body"):
    def decorator(f):
        def wrapper(*args,**kwargs):
            if query_type == "body":
                data = request.get_json()
            if query_type == "form":
                data = request.form.to_dict()
            if query_type == "query_string":
                data = request.args.to_dict()
            errors = schema.validate(data)
            if errors:
                for error in errors:
                    errors[error] = errors[error][0]
                return httpResponse(311,"Validation Error",{"message":errors})
            return f(*args,**kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator