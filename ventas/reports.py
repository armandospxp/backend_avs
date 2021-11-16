import os
import pdb
from datetime import timezone

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from ventas.models import Venta, DetalleVenta


def link_callback(uri, rel):
    """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def imprimir_factura_venta(request, id_venta):
    template_path = 'ventas/venta.html'

    venta = Venta.objects.get(id_venta=id_venta)
    detalle_venta = venta.id_detalle_venta.all()
    context = {
        'venta': venta,
        'detalle_venta': detalle_venta,
        'request': request,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=factura.pdf'
    template = get_template(template_path)
    html = template.render(context)

    # se crea el pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse('Tuvimos problemas <pre>' + html + '</pre>')
    return response
