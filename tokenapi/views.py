from django.shortcuts import render
from django.http import HttpResponse

import datetime
import json

from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Token

def FreeAndDeleteToken():
  for token in Token.objects.exclude(expireTime = None):
    CurrentTime = datetime.datetime.now()
    token.isFree = token.expireTime < CurrentTime
    token.isDeleted = token.deleteTime < CurrentTime
    token.save()       
      

@method_decorator(csrf_exempt, name='dispatch')
def CreateToken(request):
  if request.method == "POST":
    param_json = json.loads(request.body)
    no_of_tokens = param_json['no_of_tokens']
    for i in range(1,int(no_of_tokens)):
      new_token = Token()
      new_token.save()
    response = json.dumps({"success":True, "message_description":"Token created Successfully", "message":101})
    return HttpResponse(response, content_type = 'application/json')
  else:
    response = json.dumps({"success":False, "message_description":"Invalid Request", "error":201})
    return HttpResponse(response, content_type = 'application/json')
  
@method_decorator(csrf_exempt, name='dispatch')  
def AssignToken(request):
  if request.method == "POST":
    FreeAndDeleteToken()
    for token in Token.objects.filter(isFree = True, isDeleted = False):
        now = datetime.datetime.now()
        expireTime = now + datetime.timedelta(minutes=1)
        deleteTime = now + datetime.timedelta(minutes=5)
        token.expireTime = expireTime
        token.deleteTime = deleteTime
        token.save()
        response = json.dumps({"success":True, "message_description":"Token assign Successfully","token":token.id, "message":102})
        return HttpResponse(response, content_type = 'application/json')
    raise Http404("Token not available")


@method_decorator(csrf_exempt, name='dispatch')
def IsAlive(request):
    FreeAndDeleteToken()
    if request.method == "POST":
      FreeAndDeleteToken()
      param_json = json.loads(request.body)
      token = param_json['token']
      tokens = Token.objects.filter(id=token)
      if tokens.count() > 0:
        token = tokens[0]
        if not token.isFree and not token.isDeleted : 
          now = datetime.datetime.now()
          expireTime = now + datetime.timedelta(minutes=1)
          deleteTime = now + datetime.timedelta(minutes=5)
          token.expireTime = expireTime
          token.deleteTime = deleteTime
          token.save()
          response = json.dumps({"success":True, "message_description":"Token updated", "message":103})
          return HttpResponse(response, content_type = 'application/json')
        else :
          response = json.dumps({"success":False, "message_description":"Token Expired", "message":202})
          return HttpResponse(response, content_type = 'application/json')
      else:
        response = json.dumps({"success":False, "message_description":"Invalid Token", "message":203})
        return HttpResponse(response, content_type = 'application/json')
    
    response = json.dumps({"success":False, "message_description":"Invalid Request", "message":201})
    return HttpResponse(response, content_type = 'application/json')
  
@method_decorator(csrf_exempt, name='dispatch')
def UnblockToken(request):
    FreeAndDeleteToken()
    if request.method == "POST":
      FreeAndDeleteToken()
      param_json = json.loads(request.body)
      token = param_json['token']
      tokens = Token.objects.filter(id=token)
      if tokens.count() > 0:
        token = tokens[0]
        if not token.isDeleted:          
          token.isFree = True
          token.expireTime = None
          token.deleteTime = None
          response = json.dumps({"success":True, "message_description":"Token Unblocked", "message":104})
          return HttpResponse(response, content_type = 'application/json')
        else:
          response = json.dumps({"success":False, "message_description":"Token is already deleted from pool", "message":205})
          return HttpResponse(response, content_type = 'application/json')
      else:
          response = json.dumps({"success":False, "message_description":"Invalid Token", "message":203})
          return HttpResponse(response, content_type = 'application/json')
    else:
        response = json.dumps({"success":False, "message_description":"Invalid Request", "message":201})
        return HttpResponse(response, content_type = 'application/json')   
