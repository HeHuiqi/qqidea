import uuid
from django.http import HttpRequest
USER_KEY='blog_uid'
TEN_YEAES = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware:

    def __init__(self,get_response) -> None:
        self.get_response = get_response
    
    
    def __call__(self, request:HttpRequest):
        uid = self.generate_uid(request)
        request.blog_uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY,uid,max_age=TEN_YEAES,httponly=True)
        return response
    def generate_uid(self,request):
        try:
            # 017da1ccd3b142ec9d82a5907c548e0c
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex

        return uid
        