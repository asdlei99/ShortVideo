# -*- coding: utf-8 -*-
# @Time    : 3/20/18 7:56 AM
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : test.py
# @Software: PyCharm

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from video.models import VideoItem, Category, Likes
from video.forms import MediaItemUploadForm
from account.views import register

def index(request):
    template = 'video/video_index.html'

    media_items = VideoItem.objects.all()

    #print(len(media_items))
    context = {
        'media_items' : media_items,
    }

    return render(request, template, context = context)


def test_upload(request):
    template = 'video/upload.html'
    upload_media_form = MediaItemUploadForm()
    if request.method == 'POST':
        upload_media_form = MediaItemUploadForm(request.POST, request.FILES)

        if upload_media_form.is_valid():
            video = request.FILES.get('video', None)

            if video:
                media_item = VideoItem(video = video)
                media_item.save()
                return HttpResponseRedirect(reverse('video:index'))

    context = {
        'upload_media_form' : upload_media_form,
    }

    return render(request, template, context)

def test_register(request):
    template = 'user/register.html'
    if request.method == 'POST':
        return register(request)

    return render(request, template)

def test_login(request):
    template = 'user/login.html'

    return render(request, template)


def videoDetail(request, vid):
    '''视频详情页'''
    # 获取视频分类作为菜单数据
    menu_list = Category.objects.all()
    # 获取视频数据
    id = int(vid)
    video = VideoItem.objects.get(id=id)
    try:
        video.viewed()
    except Exception as e:
        print(e)

    # 获取点赞数
    try:
        likes = Likes.objects.filter(video=video).count()
    except Exception as e:
        likes = 0

    return render(request, 'video/video_detail.html')

