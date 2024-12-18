from django.http import JsonResponse

class AjaxHttpResponse(JsonResponse):
    def __init__(self, status="ok", data={}, **kwargs):
        data["status"] = status
        super().__init__(data, **kwargs)


class AjaxHttpResponseError(JsonResponse):
    def __init__(self, code, message, **kwargs):
        data = {"status": "error", "code": code, "message": message}
        super().__init__(data=data, **kwargs)



def login_required_ajax(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return AjaxHttpResponseError("no_auth", "You are not logged in")
        return view(request, *args, **kwargs)
    return wrapper