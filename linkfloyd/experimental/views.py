from django.views.generic import FormView
from linkfloyd.experimental.forms import GetImagesForm
from linkfloyd.utils import CustomHTMLParser


class GetImages(FormView):
    template_name = 'experimental/get_images.html'
    form_class = GetImagesForm

    def form_valid(self, form):
        url = form.cleaned_data.get('url')
        min_size = form.cleaned_data.get('min_size')
        p = CustomHTMLParser(url, min_size)

        # update context
        context = self.get_context_data(form=form)
        context.update({
            'images': list(p.get_images())
        })

        # and show response
        return self.render_to_response(self.get_context_data(form=form))
