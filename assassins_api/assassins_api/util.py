from django.http import HttpResponse
from django.template import Context, loader

def return_html(page,data):
  # Load the template myblog/templates/index.html
  template = loader.get_template(page)
  context = Context(data)
  return HttpResponse(template.render(context))