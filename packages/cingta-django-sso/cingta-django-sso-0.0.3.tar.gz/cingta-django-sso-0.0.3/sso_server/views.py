#coding=utf-8
'''
class Consumer(models.Model):
    application_name = ""
    public_key = ""
    private_key = ""
'''
from _io import StringIO
import datetime
import hashlib
import json
import os
import time
import traceback

from django.apps.registry import apps
from django.conf.urls import url
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.http.response import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from djconnect.models import Provider
from djconnect.sync import provider_for_django, SyncConsumer

from sso_server.models import Consumer, Token, SSO_TOKEN_EXPIRE
from sso_server.utils import getdefault


#########################################
#客户端的sso代码
#########################################
class Client:
    
    def __init__(self,server_url,public_key,private_key):
        self.server_url = server_url
        self.public_key = public_key
        self.private_key = private_key
        self.consumer = SyncConsumer(self.server_url, self.public_key, self.private_key)
    
    def can_connect_sso(self,request):
        print("inner:", request.POST.get("ct"), request.COOKIES.get("cingta-django-sso"))
        if not (request.POST.get("ct") or request.COOKIES.get("cingta-django-sso")):
            return False
        else:
            try:
                cookie = request.POST.get("ct") or request.COOKIES.get("cingta-django-sso")
                token = Token.objects.get(access_token=cookie)
                if token.ip:
                    if 'HTTP_X_FORWARDED_FOR' in request.META:
                        ip =  request.META['HTTP_X_FORWARDED_FOR']
                    else:
                        ip = request.META['REMOTE_ADDR']
                    if token.ip == ip:
                        return True
                return False
            except Exception as e:
                return False
        return True
    
    def request_token(self, ip, username, password):
        url = '/request_token/'
        check_code = self.consumer.consume(url, {
            "username": username,
            "password": password,
            "ip": ip,
            })
        return check_code
    
    def login_token(self,request_token,username,password):
        url = '/login_token/'
        if not request_token:
            return
        return self.consumer.consume(url, {
            "check_code": request_token.get("check_code"),
            "id": request_token.get("id"),
            "username": username,
            "password": password
        }).get("result")  
    
    def verify_token(self,request):
        token = request.POST.get("ct") or request.COOKIES.get("cingta-django-sso")
        url = '/verify_token/'
        return self.consumer.consume(url,{"access-token":token})
    
    def center_operate_user(self, appname:str, user_info:dict, user_filter:dict, method="create"):
        url = '/center_operate_user/'
        return self.consumer.consume(url, {
            "app_name": appname,
            "user_info": user_info,
            "user_filter": user_filter,
            "method": method
        })
    
    def single_operate_user(self, kwargs:dict):
        url = "/single_operate_user/"
        return self.consumer.consume(url, {
            "user_appname": kwargs.get("user_appname"),
            "user_modelname": kwargs.get("user_modelname"),
            "user_info": kwargs.get("user_info"),
            "user_filter": kwargs.get("user_filter"),
            "method": kwargs.get("method")
        })
    
    ######################################################################
    #login逻辑
    #####################################################################
    
    def sso_token_login(self, user_model, request) -> object or None:
        try:
            verify_info = self.verify_token(request)
            if verify_info:
                user = user_model.objects.get(username=verify_info)
                login(request, user)
                return user
        except:
            return
        
    def generate_token(self, request, username, password) -> str or None:
        if username and password and username.endswith("@cingta.com"): #cingta用户才进行单点登录
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip =  request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            if not ip:
                return
            try:
                check_code = self.request_token(ip, username, password)
                sso_token = self.login_token(check_code, username, password)
                return sso_token
            except:
                return
        
class ClientSSOOperation:
    def __init__(self, user_model):
        self.user_model = user_model
    
    @property
    def token_logout(self):
        username = getattr(self.user_model, "username")
        if not username:
            raise AttributeError("User Model don't has username field")
        Token.objects.filter(username=username).delete()
        

####################################
#服务端代码
####################################

def token_generate():
    timestamp = int(time.time())
    return timestamp

class BaseProvider(Provider):
#     max_age = 60 * 24 * 60
    def __init__(self):
        self.token_timeout = datetime.timedelta(seconds=SSO_TOKEN_EXPIRE)
        self.check_code_timeout = 60 #认证时间间隔

    def get_private_key(self,public_key):
        try:
            self.consumer = Consumer.objects.get(public_key=public_key)
        except Consumer.DoesNotExist:
            return None
        return self.consumer.private_key
    
class BroadCastProvider(BaseProvider):
    def center_deliver(self, data):
        app_name = data.get("app_name")
        user_info = data.get("user_info")
        user_filter = data.get("user_filter")
        method = data.get("method")
        
        current_consumer = Consumer.objects.get(name=app_name)
        other_consumers = Consumer.objects.exclude(name=app_name)
        
        for o_consumer in other_consumers:
            public_key = current_consumer.public_key
            private_key = current_consumer.private_key
            server_host = o_consumer.server_host
            _client = Client(server_host, public_key, private_key)
            print(1)
            print("single_operate_user",o_consumer.id, server_host, public_key, private_key)
            _client.single_operate_user({
                "user_appname": o_consumer.user_appname,
                "user_modelname": o_consumer.user_modelname,
                "user_filter": user_filter,
                "user_info": user_info,
                "method": method
            })
    
    def single_deliver(self, data):
        user_info = data.get("user_info")
        method = data.get("method")
        user_filter = data.get("user_filter")
        user_model = data.get("user_model")
         
        if method == 'update':
            user_model.objects.filter(**user_filter).update(**user_info)
        if method == "delete":
            user_model.objects.filter(**user_filter).delete()
        if method == "create":
            user_info["password"] = getdefault()
            user_model.objects.create_user(**user_info)
    
    def user_session_logout(self, user):
        all_sessions = Session.objects.all().filter(expire_date__gte=datetime.datetime.now())
        for ss in all_sessions:
            decoded_info = ss.get_decoded()
            if decoded_info:
                _auth_user_id = decoded_info.get("_auth_user_id")
                _auth_pk = ss.pk
                if user.id == _auth_user_id:
                    Session.objects.filter(id=_auth_pk).delete()

class RequestTokenProvider(BaseProvider):
    #@cap_exception
    def provide(self,data):
        user = authenticate(username=data.get("username"), password=data.get('password'))
        if user:
            token = token_generate()
            db_token = Token.objects.create(
                consumer = self.consumer,
                request_token = token,
                username = data.get("username"),
                ip = data.get("ip")
            )
            return {"check_code":token,"id":db_token.id}
        else:
            return None

class VerificationProvider(BaseProvider):
    #@cap_exception
    def provide(self, data):
        token = data.get('access-token')
        db_token = Token.objects.get(access_token=token)
        delta = timezone.now() - db_token.timestamp
        if delta > self.token_timeout:
            return False
        else:
            db_token.refresh()
            return db_token.username
            
    def token_not_bound(self):
        return HttpResponseForbidden("Invalid token")

class LoginTokenProvider(BaseProvider):
    #@cap_exception
    def provide(self,data):
        if not data:
            return
        if int(data["check_code"]) + self.check_code_timeout < int(time.time()):
            return
        username = data.get("username")
        token = Token.objects.get(id=data.get("id"))
        access_token = hashlib.md5((token.ip+username+str(time.time())).encode("utf-8")).hexdigest()
        token.access_token = access_token
        token.save()
        return {"result" : access_token}
        
class CenterOperateUserProvider(BroadCastProvider):
    #@cap_exception
    def provide(self, data):
        '''
        {
            user_info: dict,
            app_name: str,
            method: [create、update、delete]
        }
        '''
        try:
            app_name = data.get("app_name")
            user_info = data.get("user_info")
            user_filter = data.get("user_filter")
            method = data.get("method")
            print(app_name, user_info, user_filter, method)
            current_consumer = Consumer.objects.get(name=app_name)
            print(current_consumer)
            user_appname = current_consumer.user_appname
            user_modelname = current_consumer.user_modelname
            user_model = apps.get_model(user_appname, user_modelname)
            print(user_model)
            if method == "logout":
                current_user = user_model.objects.get(**user_filter)
                print(current_user)
                Token.objects.filter(username=current_user.username).delete()
                self.user_session_logout(current_user)
#             else:
#                 if method == 'update':
#                     user_model.objects.filter(**user_filter).update(**user_info)
#                 if method == "delete":
#                     user_model.objects.filter(**user_filter).delete()
#                 if method == "create":
#                     user_model.objects.create(**user_info)
            
#             data["current_consumer"] = current_consumer
            self.center_deliver(data)  
        except:
            fp = StringIO()
            traceback.print_exc(file=fp)
            msg = fp.getvalue()
            with open("sso_error.log", "a+", encoding="utf-8") as f:
                f.write(msg)
                f.write(os.linesep)
                
            
class SingleOperateUserProvider(BroadCastProvider):
    #@cap_exception
    def provide(self, data):
        '''
        {
            user_appname: str,
            user_modelame: str,
            user_info: dict
            user_filter: dict
            method: [create、update、delete]
        }
        '''
        try:
            user_appname = data.get("user_appname")
            user_modelname = data.get("user_modelname")
            method = data.get("method")
            user_filter = data.get("user_filter")
            print(user_appname, user_modelname)
            user_model = apps.get_model(user_appname, user_modelname)
            
            if method == "logout":
                current_user = user_model.objects.get(**user_filter)
                self.user_session_logout(current_user)
            else:
                data["user_model"] = user_model
                self.single_deliver(data)
        except:
            fp = StringIO()
            traceback.print_exc(file=fp)
            msg = fp.getvalue()
            with open("sso_error.log", "a+", encoding="utf-8") as f:
                f.write(msg)
                f.write(os.linesep)
                
def localize_sso_server_cookie(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    print(request.POST.get("ct"), ip)
    if (
        request.COOKIES.get("cingta-django-sso") or 
        request.POST.get("ct")
    ) and ip:
        token = request.POST.get("ct") or request.COOKIES.get("cingta-django-sso")
        print("token:", token)
        if token:
            token_db = Token.objects.filter(access_token=token, ip=ip).first()
            print("token_db", token_db)
            if token_db:
#                 token.access_token = hashlib.md5((token.ip+token.access_token+str(time.time())).encode("utf-8")).hexdigest()
#                 token.save()
                resp = HttpResponse(json.dumps({"state":0, "data":token}), content_type="application/json")
                resp.set_cookie("cingta-django-sso", token, httponly=True) #, domain=request.META.get("HTTP_ORIGIN")
                resp['Access-Control-Allow-Headers'] = '*'
                resp['Access-Control-Allow-Origin'] = request.META.get("HTTP_ORIGIN")
                resp['Access-Control-Allow-Credentials'] = "true"
                resp['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
                return resp
    resp = HttpResponse(json.dumps({"state":1}), content_type="application/json")
    resp['Access-Control-Allow-Headers'] = '*'
    resp['Access-Control-Allow-Origin'] = request.META.get("HTTP_ORIGIN")
    resp['Access-Control-Allow-Credentials'] = "true"
    resp['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    return resp
            
class Server(object):
    #登录逻辑
    request_token_provider = RequestTokenProvider
    verification_provider = VerificationProvider
    login_provider = LoginTokenProvider
    #用户新增、删除、更新等逻辑
    center_operate_user_provider = CenterOperateUserProvider
    single_operate_user_provider = SingleOperateUserProvider
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def check_token_timeout(self):
        delta = timezone.now() - self.token.timestamp
        if delta > self.server.token_timeout:
            self.token.delete()
            return False
        else:
            return True

    def get_urls(self):
        return [
            url(r'^request_token/$', provider_for_django(self.request_token_provider()), name='simple-sso-request-token'),
            url(r'^verify_token/$', provider_for_django(self.verification_provider()), name='verify_token'),
            url(r'^login_token/$', provider_for_django(self.login_provider()), name='login_token'),
            
            url(r'^center_operate_user/$', provider_for_django(self.center_operate_user_provider())),
            url(r'^single_operate_user/$', provider_for_django(self.single_operate_user_provider())),
            
            url(r'^localize_sso_server_cookie/$', localize_sso_server_cookie, name='localize_sso_server_cookie'),
        ]
