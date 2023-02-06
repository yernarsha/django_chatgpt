from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator

import openai

from .models import QandA

# Create your views here.

def home(request):
    if request.method == "POST":
        question = request.POST['question']
        past_responses = request.POST['past_responses']

        openai.api_key = "YOUR API KEY"
        openai.Model.list()

        try:
#            response = openai.Completion.create(engine="ada", prompt=question)
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=question,
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            print(response)
            response = (response['choices'][0]['text']).strip()
#            response = "That's the way I like it"

            if "johnmccartney" in past_responses:
                past_responses = response
            else:
                past_responses = f"{past_responses}<br/><br/>{response}"

            record = QandA(question=question, answer=response)
            record.save()

            return render(request, "bot/home.html",
                           {'question': question, "response": response, "past_responses": past_responses})
        except Exception as e:
            return render(request, "bot/home.html", 
                          {'question': question, "response": e, "past_responses": e})
    
    else:
        return render(request, "bot/home.html", {})

def qa(request):
    p = Paginator(QandA.objects.all(), 4)
    page = request.GET.get('page')
    pages = p.get_page(page)

    nums = "a" * pages.paginator.num_pages

    return render(request, 'bot/qa.html', {'pages': pages, 'nums': nums})

def delete_q(request, q_id):
    q = QandA.objects.get(pk=q_id)
    q.delete()
    messages.success(request, "Deleted")

    return redirect('qa')
