from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.timezone import make_aware
from django.http import JsonResponse
from .models import Message
from datetime import datetime
from .openai import OpenAiCli


def index(request):
    messageList = Message.objects.order_by('timestamp')
    context = {'message_list': messageList}
    return render(request, 'chatgpt_proxy/index.html', context)


def chat(request):
    return render(request, 'chatgpt_proxy/chat.html')


def send(request):
    sendContent = request.POST['message_send_input']
    sendTimeStamp = make_aware(datetime.now())
    latestMessageList = Message.objects.order_by('-timestamp')[:10][::-1]
    messages = [{'role': m.role, 'content': m.content} for m in latestMessageList]
    messages.append({'role': 'user', 'content': sendContent})
    cli = OpenAiCli()
    replyContent = cli.chat(messages)
    replyTimeStamp = make_aware(datetime.now())
    sendMessage = Message.objects.create(timestamp=sendTimeStamp, role='user', content=sendContent)
    sendMessage.save()
    replyMessage = Message.objects.create(timestamp=replyTimeStamp, role='assistant', content=replyContent)
    replyMessage.save()
    return HttpResponseRedirect('/chatgpt_proxy/')


def jsChatHist(request):
    messageList = Message.objects.order_by('timestamp')
    messages = [{'role': m.role, 'content': m.content, 'timestamp': m.timestamp} for m in messageList]
    return JsonResponse(messages, safe=False)


def jsChatSend(request):
    sendContent = request.POST['messageInput']
    sendTimeStamp = make_aware(datetime.now())
    latestMessageList = Message.objects.order_by('-timestamp')[:10][::-1]
    messages = [{'role': m.role, 'content': m.content} for m in latestMessageList]
    messages.append({'role': 'user', 'content': sendContent})
    cli = OpenAiCli()
    replyContent = cli.chat(messages)
    replyTimeStamp = make_aware(datetime.now())
    sendMessage = Message.objects.create(timestamp=sendTimeStamp, role='user', content=sendContent)
    sendMessage.save()
    replyMessage = Message.objects.create(timestamp=replyTimeStamp, role='assistant', content=replyContent)
    replyMessage.save()
    return JsonResponse({'Ret': 'OK'})
