from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import ListView
from .models import Answer
from help_services.forms import ContactForm
from .forms import UserQuestionForm

def about(request):
    return render(request, "help_services/about.html")

def delivery(request):
    return render(request, "help_services/delivery.html")

def contact(request):
    return render(request, "help_services/contact.html")

class AnswerViews(FormView):
    template_name = "help_services/answer.html"
    form_class = UserQuestionForm
    context_object_name = "answers"
    success_url = reverse_lazy('answer')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = Answer.objects.exclude(text='').exclude(text__isnull=True)
        context['answers'] = answers
        return context

class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'help_services/feedback.html'
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('about')

def basket(request):
    return render(request, "help_services/basket.html")

