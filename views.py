from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pro_site.models import *
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import collections
import datetime

models_list = [Pv14, Oi13, Pv13, Oi12, Pv12, Oi11, Pv11, Oi10, Pv10, Oi09, Pv09, Oi08, Pv08,
               Oi07, Pv07, Oi06, Pv06, Oi05, Pv05, Oi04, Pv04, Oi03, Pv03, Oi02, Pv02, Oi01, Pv01,
               Oi00, Pv00, Oi99, Pv99, Oi98, Pv98, Oi97, Pv97]


def excel_export(request):
    import xlwt
    ciclo = request.GET.get('ciclo')
    ddr = request.GET.get('ddr')
    caders = request.GET.get('caders')
    municipios = request.GET.get('municipios')
    ejidos = request.GET.get('ejidos')
    page = request.GET.get('page')
    nombre_propietario = request.GET.get('nombre_propietario')
    nombre_productor = request.GET.get('nombre_productor')
    s_apoyo = request.GET.get('s_apoyo')
    se_min = request.GET.get('se_min')
    se_max = request.GET.get('se_max')
    st_min = request.GET.get('st_min')
    st_max = request.GET.get('st_max')
    medio_pago = request.GET.get("medio_dp")
    book      = xlwt.Workbook(encoding       = 'utf8')
    sheet     = book.add_sheet('untitled')
    model = models_list[0]

    model = models_list[int(ciclo)]
    predios = model.objects.all()


    if ddr:
        ddr = Ddr.objects.get(id=ddr)
        predios = predios.filter(ddr_n=ddr.numero)
        if caders:
            caders = Cader.objects.get(id=caders)
            predios = predios.filter(cader_n=caders.numero)
            if municipios:
                municipios = Municipio.objects.get(id=municipios)
                predios = predios.filter(municipio_n=municipios.numero)
                if ejidos:
                    ejidos = Ejido.objects.get(id=ejidos)
                    predios = predios.filter(ejido_n=ejidos.numero)
    if nombre_propietario:
        predios = predios.filter(nombre_propietario__icontains=nombre_propietario)
    if nombre_productor:
        predios = predios.filter(nombre_del_productor__icontains=nombre_productor)
    if s_apoyo:
        predios = predios.filter(situacion_del_incentivo__icontains=s_apoyo)
    if se_min:
        predios = predios.filter(superficie_elegible__gte=se_min)
    if se_max:
        predios = predios.filter(superficie_elegible__lt=se_max)
    if st_min:
        st_min = int(st_min)
        predios = predios.filter(superficie_total__gte=st_min)
    if st_max:
        st_max = int(st_max)
        predios = predios.filter(superficie_total__lt=st_max)
    if medio_pago:
        predios = predios.filter(medio_de_pago=medio_pago)
    values_list = list()
    values_list = predios.values_list()
    for row, rowdata in enumerate(values_list):
        for col, val in enumerate(rowdata[1:]):
            sheet.write((row+1), col, val)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=report.xls'
    book.save(response)
    return response

def is_in_group(user_, group_):
    if user_:
        return user_.groups.filter(name=group_).count() > 0
    return False


def capturas_fun(request, a, ciclo):
    model = models_list[int(ciclo)]
    predios = model.objects.filter(status_pago=a)
    odpago = predios.filter(medio_de_pago='ORD').distinct('evento_de_pago')
    return odpago


def capturas(request):
    user = request.user
    a = 0
    data_0 = models_list[0].objects.filter(medio_de_pago='ORD')
    data_1 = models_list[2].objects.filter(medio_de_pago='ORD')
    data_2 = models_list[4].objects.filter(medio_de_pago='ORD')
    if is_in_group(user, 'delegacion'):
        data_0 = data_0.filter(status_pago=a).distinct('evento_de_pago')
        data_1 = data_1.filter(status_pago=a).distinct('evento_de_pago')
        data_2 = data_2.filter(status_pago=a).distinct('evento_de_pago')
        if request.POST:
            odpago_0 = request.POST.getlist('odpago_0')
            odpago_1 = request.POST.getlist('odpago_1')
            odpago_2 = request.POST.getlist('odpago_2')
            for odp in odpago_0:
                odpago0 = data_0.filter(evento_de_pago=odp)
                odpago0.update(status_pago=1)
            for odp in odpago_1:
                odpago1 = data_1.filter(evento_de_pago=odp)
                odpago1.update(status_pago=1)
            for odp in odpago_2:
                odpago2 = data_2.filter(evento_de_pago=odp)
                odpago2.update(status_pago=1)
        return render(request, 'capturas.html', {'odpago_0': data_0, 'odpago_1': data_1, 'odpago_2': data_2})
    elif is_in_group(user, 'administrativo'):
        distritos = Ddr.objects.all()
        data0 = {}
        data1 = {}
        data2 = {}
        data_0 = data_0.filter(status_pago=1)
        data_1 = data_1.filter(status_pago=1)
        data_2 = data_2.filter(status_pago=1)
        for district in distritos:
            buf = data_0.filter(ddr__startswith=district.numero).distinct('evento_de_pago')
            if len(buf) > 0:
                data0.update({buf[0].ddr: buf})
            buf = data_1.filter(ddr__startswith=district.numero).distinct('evento_de_pago')
            if len(buf) > 0:
                data1.update({buf[0].ddr: buf})
            buf = data_2.filter(ddr__startswith=district.numero).distinct('evento_de_pago')
            if len(buf) > 0:
                data2.update({buf[0].ddr: buf})
            data0 = collections.OrderedDict(sorted(data0.items()))
            data1 = collections.OrderedDict(sorted(data1.items()))
            data2 = collections.OrderedDict(sorted(data2.items()))
        if request.POST:
            odpago_0 = request.POST.getlist('odpago_0')
            odpago_1 = request.POST.getlist('odpago_1')
            odpago_2 = request.POST.getlist('odpago_2')
            for odp in odpago_0:
                evento, ddr = odp.split(';')
                num, name = ddr.split('-')
                odpago0 = data_0.filter(evento_de_pago=evento, ddr__startswith=num)
                odpago0.update(status_pago=2)
            for odp in odpago_1:
                evento, ddr = odp.split(';')
                num, name = ddr.split('-')
                odpago1 = data_1.filter(evento_de_pago=evento, ddr__startswith=num)
                odpago1.update(status_pago=2)
            for odp in odpago_2:
                evento, ddr = odp.split(';')
                num, name = ddr.split('-')
                odpago2 = data_2.filter(evento_de_pago=evento, ddr__startswith=num)
                odpago2.update(status_pago=2)
            return redirect('/capturas/')
        return render(request, 'capturas_admin.html', {'data0': data0, 'data1': data1, 'data2': data2})
    elif is_in_group(user, 'distritos'):
        ddrG = user.groups.filter(name__contains='ddr')[0].name
        ddr, num = ddrG.split('_')
        ddr_ = Ddr.objects.get(numero=num)
        ddr = ddr_.nombre
        caders = Cader.objects.filter(ddr_id=ddr_.id)
        data0 = {}
        data1 = {}
        data2 = {}
        data_0 = data_0.filter(status_pago=2, ddr__startswith=num)
        data_1 = data_1.filter(status_pago=2, ddr__startswith=num)
        data_2 = data_2.filter(status_pago=2, ddr__startswith=num)
        for cader in caders:
            buf = data_0.filter(cader__startswith=cader.numero).distinct('evento_de_pago')
            if len(buf):
                data0.update({buf[0].cader: buf})
            buf = data_1.filter(cader__startswith=cader.numero).distinct('evento_de_pago')
            if len(buf) > 0:
                data1.update({buf[0].cader: buf})
            buf = data_2.filter(cader__startswith=cader.numero).distinct('evento_de_pago')
            if len(buf) > 0:
                data2.update({buf[0].cader: buf})
        if request.POST:
            odpago_0 = request.POST.getlist('odpago_0')
            odpago_1 = request.POST.getlist('odpago_1')
            odpago_2 = request.POST.getlist('odpago_2')
            for odp in odpago_0:
                evento, ddr = odp.split(';')
                num, name = ddr.split('-')
                odpago0 = data_0.filter(evento_de_pago=evento)
                odpago0.update(status_pago=3, entrega_a_cader=datetime.datetime.now())
            for odp in odpago_1:
                evento, ddr = odp.split(';')
                num, name = ddr.split('-')
                odpago1 = data_1.filter(evento_de_pago=evento)
                odpago1.update(status_pago=3, entrega_a_cader=datetime.datetime.now())
            for odp in odpago_2:
                evento, ddr = odp.split(';')
                num, name = ddr.split('-')
                odpago2 = data_2.filter(evento_de_pago=evento)
                odpago2.update(status_pago=3, entrega_a_cader=datetime.datetime.now())
            return redirect('/capturas/')
        return render(request, 'capturas_ddr.html',
                      {'distrito': ddr.capitalize(), 'data0': data0, 'data1': data1, 'data2': data2})
    elif is_in_group(user, 'cader'):
        caderG = user.groups.filter(name__contains='cader_')[0].name
        name, num = caderG.split('_')
        cader = Cader.objects.get(id=num)
        data_0 = data_0.filter(status_pago=3, cader__startswith=cader.numero)
        data_1 = data_1.filter(status_pago=3, cader__startswith=cader.numero)
        data_2 = data_2.filter(status_pago=3, cader__startswith=cader.numero)
        return render(request, 'capturas_cader.html',
                      {'cader': cader.nombre, 'data_0': data_0, 'data_1': data_1, 'data_2': data_2})
    else:
        return HttpResponse("Usted no esta autorizado")
        #data.update({'odpago_pv14':data_pv14})
        #return render(request, 'capturas.html', data)


@csrf_exempt
def get_cartography_data(request):
    if request.POST:
        modelo = request.POST.get('model_')
        user = request.user
        m_id = request.POST.get('id')
        if modelo == 'cader':
            data_m = Cader.objects.filter(ddr_id=m_id)
            if is_in_group(user, "cader"):
                caderG = user.groups.filter(name__contains='cader_')[0].name
                name, num = caderG.split('_')
                cader = Cader.objects.get(id=num)
                data_m = data_m.filter(id = num)
        elif modelo == 'municipio':
            data_m = Municipio.objects.filter(cader_id=m_id)
        elif modelo == 'ejido':
            data_m = Ejido.objects.filter(municipio_id=m_id)
        else:
            data_m = ""
        data = serializers.serialize("json", data_m)
        return HttpResponse(data, mimetype="application/javascript")
    return HttpResponse("Hello World")


#@csrf_exempt
#def obtener_ejidos(request):
    #if request.POST:
        #municipio_id = request.POST.get('municipio_id')
        #ejido = Ejido.objects.filter(municipio_id=municipio_id)
        #data_m = serializers.serialize("json", ejido, fields=('id', 'nombre'))
        #return HttpResponse(data_m, mimetype="application/javascript")
    #return HttpResponse("Hello World")


#@csrf_exempt
#def obtener_municipios(request):
    #if request.POST:
        #cader_id = request.POST.get('cader_id')
        #municipio = Municipio.objects.filter(cader_id=cader_id)
        #data_m = serializers.serialize("json", municipio, fields=('id', 'nombre'))
        #return HttpResponse(data_m, mimetype="application/javascript")
    #return HttpResponse("Hello World")


#@csrf_exempt
#def obtener_caders(request):
    #if request.POST:
        #ddr_id = request.POST.get('ddr_id')
        #caders = Cader.objects.filter(ddr_id=ddr_id)
        #data = serializers.serialize("json", caders, fields=('id', 'nombre'))
        #return HttpResponse(data, mimetype="application/javascript")
    #return HttpResponse("Hello World")


def home(request):
    titulo = "Pagina de inicio"
    return render(request, 'home.html', {'titulo': titulo})


@csrf_exempt
@login_required(login_url='/login')
def distrito(request):
    user = request.user
    ciclos = []
    i = 0
    for model in models_list:
        ciclos.append([i, model._meta.verbose_name.title()])
        i = i + 1
    ddrs = Ddr.objects.all()
    if is_in_group(user, "distritos"):
        distrito = user.groups.filter(name__contains="ddr_")[0].name
        buf, num = distrito.split('_')
        ddrs = ddrs.filter(numero=int(num))
    if is_in_group(user, "cader"):
        caderG = user.groups.filter(name__contains='cader_')[0].name
        name, num = caderG.split('_')
        cader = Cader.objects.get(id=num)
        ddrs=ddrs.filter(id=cader.ddr_id)
    return render(request, "distrito.html", {'ddrs': ddrs, 'ciclos': ciclos})


@login_required(login_url='/login')
def predio(request, folio, secuencial):
    list_predios = []
    for model in models_list:
        buffer_ = model.objects.filter(predio=folio, secuencial=secuencial)
        if buffer_:
            list_predios.append([model._meta.verbose_name.title(), buffer_])
    titulo = "Predio: " + folio + " - " + secuencial
    return render(request, 'predio.html',
                  {'titulo': titulo,
                   'list_predios': list_predios})

@login_required(login_url='/login')
def propietario(request, curp):
    list_predios = []
    titulo = ""
    exist = False
    for model in models_list:
        if curp:
            buffer_ = model.objects.filter(curp=curp)
            if len(buffer_) > 0:
                exist = True
                titulo = "Propietario: " + buffer_[0].nombre_propietario
                list_predios.append([model._meta.verbose_name.title(), buffer_])
        else:
            exist = False
    if exist == False:
        titulo = "Error"
        list_predios = None
    return render(request, 'propietario.html',
                  {'titulo': titulo,
                   'list_predios': list_predios})

@login_required(login_url='/login')
def productor(request, c_productor):
    list_predios = []
    titulo = ""
    exist = False
    if c_productor:
        for model in models_list:
            buffer_ = model.objects.filter(curp_productor=c_productor)
            if len(buffer_) > 0:
                exist = True
                titulo = "Productor: " + buffer_[0].nombre_del_productor
                list_predios.append([model._meta.verbose_name.title(), buffer_])
    if exist == False:
        titulo = "Error"
        list_predios = None
    return render(request, 'productor.html',
                  {'titulo': titulo,
                   'list_predios': list_predios})


@login_required(login_url='/login')
def nombre_propietario(request):
    titulo = "Nombre del propietario"
    if request.POST:
        nombre = request.POST.get('nombre')
        predios_list = []
        for model in models_list:
            predios_list.append(model.objects.filter(nombre_propietario__icontains=nombre))
        propietarios = []
        set_propietarios = set()
        error = ""
        for predios in range(0, len(predios_list)):
            for predio in predios_list[predios]:
                if predio.curp not in set_propietarios:
                    propietarios.append(predio)
                set_propietarios.add(predio.curp)
        if len(propietarios) < 1:
            error = "Nombre no encontrado"
        return render(request, 'n_propietario.html',
                      {
                          'propietarios': propietarios, 'error': error
                      })
    return render(request, 'n_propietario.html', {'titulo': titulo})


@login_required(login_url='/login')
def nombre_productor(request):
    titulo = "Nombre del productor"
    if request.POST:
        nombre = request.POST.get('nombre')
        ciclos = request.POST.get('ciclos')
        predios_list = []
        for model in models_list:
            predios_list.append(model.objects.filter(nombre_del_productor__icontains=nombre))
        productores = []
        set_productores = set()
        error = ""
        for predios in range(0, len(predios_list)):
            for predio in predios_list[predios]:
                if predio.curp_productor not in set_productores:
                    productores.append(predio)
                set_productores.add(predio.curp_productor)
        if len(productores) < 1:
            error = "Nombre no encontrado"
        return render(request, 'n_productor.html',
                      {
                          'productores': productores, 'error': error
                      })
    return render(request, 'n_productor.html', {'titulo': titulo})


@login_required(login_url='/login')
def f_productor(request):
    titulo = "Folio del productor"
    if request.POST:
        folio = request.POST.get('folio')
        predios_list = []
        for model in models_list:
            predios_list.append(model.objects.filter(productor__icontains=folio))
        productores = []
        set_productores = set()
        error = ""
        for predios in range(0, len(predios_list)):
            for predio in predios_list[predios]:
                if predio.productor not in set_productores:
                    productores.append(predio)
                set_productores.add(predio.productor)
        if len(productores) < 1:
            error = "Nombre no encontrado"
        return render(request, 'f_productor.html',
                      {
                          'productores': productores, 'error': error
                      })
    return render(request, 'f_productor.html', {'titulo': titulo})


@login_required(login_url='/login')
def f_doc_legal(request):
    titulo = "Folio del documento legal"
    if request.POST:
        folio = request.POST.get('folio')
        predios = []
        for model in models_list:
			predios_list = model.objects.filter(folio_del_documento_legal__icontains=folio)
			if len(predios_list) > 0:
				for predio in predios_list:
					predios.append(predio)
				return render(request, 'f_doc_legal.html', {'titulo':titulo, 'predios':predios })
    return render(request, 'f_doc_legal.html', {'titulo': titulo})


@login_required(login_url='/login')
def f_predio(request):
    titulo = "Folio de predio"
    if request.POST:
        folio = request.POST.get('predio')
        folio = folio.split('-')
        predio = None
        if len(folio) == 2:
            for model in models_list:
                predio = model.objects.filter(predio=folio[0].strip(), secuencial=folio[1].strip())
                if len(predio) > 0:
                    return render(request, 'f_predio.html',
                                  {
                                      'titulo': titulo,
                                      'predio':predio[0]
                                  })
            errors = "No se encontro el folio"
            return render(request, 'f_error.html', {'errors': errors})
        else:
            errors = "Formato incorrecto del folio a buscar"
            return render(request, 'f_error.html', {'errors': errors})
    return render(request, 'f_predio.html', {'titulo': titulo})


@login_required(login_url='/login')
def f_tramite(request):
    titulo = "Folio del tramite"
    if request.POST:
        folio = request.POST.get('tramite')
        predio = None
        for model in models_list:
            try:
                predio = model.objects.get(folio_tramite__icontains=folio)
                return render(request, 'f_solicitud.html',
                              {
                                  'titulo': titulo,
                                  'predio':predio
                              })
            except:
                errors = "No se encontro el folio"
                return render(request, 'f_solicitud.html', {'titulo': folio, 'errors': errors})
    return render(request, 'f_solicitud.html', {'titulo': titulo})


@csrf_exempt
def paginate(request):
    if request.is_ajax():
        model = models_list[0]
        ciclo = request.POST.get('ciclo')
        ddr = request.POST.get('ddr')
        caders = request.POST.get('caders')
        municipios = request.POST.get('municipios')
        ejidos = request.POST.get('ejidos')
        page = request.POST.get('page')
        nombre_propietario = request.POST.get('nombre_propietario')
        nombre_productor = request.POST.get('nombre_productor')
        s_apoyo = request.POST.get('s_apoyo')
        se_min = request.POST.get('se_min')
        se_max = request.POST.get('se_max')
        st_min = request.POST.get('st_min')
        st_max = request.POST.get('st_max')
        medio_pago = request.POST.get("medio_dp")

        if ciclo:
            model = models_list[int(ciclo)]
        predios = model.objects.all()
        if ddr:
            ddr = Ddr.objects.get(id=ddr)
            predios = predios.filter(ddr_n=ddr.numero)
            if caders:
                caders = Cader.objects.get(id=caders)
                predios = predios.filter(cader_n=caders.numero)
                if municipios:
                    municipios = Municipio.objects.get(id=municipios)
                    predios = predios.filter(municipio_n=municipios.numero)
                    if ejidos:
                        ejidos = Ejido.objects.get(id=ejidos)
                        predios = predios.filter(ejido_n=ejidos.numero)
        if nombre_propietario:
            predios = predios.filter(nombre_propietario__icontains=nombre_propietario)
        if nombre_productor:
            predios = predios.filter(nombre_del_productor__icontains=nombre_productor)
        if s_apoyo:
            predios = predios.filter(situacion_del_incentivo__icontains=s_apoyo)
        if se_min:
            predios = predios.filter(superficie_elegible__gte=int(se_min))
        if se_max:
            predios = predios.filter(superficie_elegible__lt=int(se_max))
        if st_min:
            st_min = int(st_min)
            predios = predios.filter(superficie_total__gte=int(st_min))
        if st_max:
            st_max = int(st_max)
            predios = predios.filter(superficie_total__lt=int(st_max))
        if medio_pago:
            predios = predios.filter(medio_de_pago=medio_pago)
        paginator = Paginator(predios, 100)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        data_t = {}
        data_t.update({"has_next": items.has_next()})
        data_t.update({"has_previous": items.has_previous()})
        data_t.update({"num_pages": paginator.num_pages})
        data_t.update({"total": paginator.count})
        myjson = []
        predios = items.object_list.values_list('ddr', 'cader', 'municipio', 'ejido', 'nombre_del_productor',
                                                'curp_productor', 'folio_tramite', 'predio', 'secuencial',
                                                'cuenta_folio_cheque_referencia_op', 'superficie_elegible',
                                                'status_pago', 'evento_de_pago')
        for p in predios:
            myjson.append(p)
        data_t.update({"items": myjson})
        data = json.dumps(data_t)
        return HttpResponse(data, mimetype="application/javascript")
    return HttpResponse(":)")

