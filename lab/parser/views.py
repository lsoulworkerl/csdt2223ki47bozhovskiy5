from .models import Data
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .services import parser

class ParserView(CreateView):
    model = Data
    template_name = 'parser\detail.html'
    fields = ('input',)

    def get_success_url(self):
        return reverse('result', kwargs={'slug': self.object.input})

    def form_valid(self, form):
        try:
            result = Data.objects.get(input=form.instance.input).output
            return HttpResponseRedirect(reverse('result', kwargs={'slug': form.instance.input}))
        except:
            form.instance.output = parser(str(form.instance.input))
            form.save()

        return super().form_valid(form)


class ResultView(DetailView):
    model = Data
    template_name = 'parser/result.html'
    slug_field = "input"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        