from django.shortcuts import render,redirect
from django.views.generic import TemplateView

# Create your views here.

from .forms import CommentForm

class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self,requset,*args,**kwargs):
        comment_form = CommentForm(requset.POST)
        target = requset.POST.get('target')
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            suc = True
            return redirect(target)
        else:
            suc = False
        context = {
            'succeed':suc,
            'form':comment_form,
            'target':target
        }
        return self.render_to_response(context=context)
