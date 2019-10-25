from django.conf import global_settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from user.models import CustomUser
from location.models import Location, Status, VolunteerBase

def generate_pdf(request, slug):
    location = Location.objects.get(slug=slug)
    statuses = location.status.all()
    html = render_to_string('statistic/pdf.html', {'statuses': statuses})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="statistic_{location.name}.pdf"'
    weasyprint.HTML(string=html).write_pdf(
        response
    )
    return response

def
