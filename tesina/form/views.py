from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Document, Field, CompiledDoc, CompiledField
from .forms import *
from xhtml2pdf import pisa
from io import BytesIO
import os
import re
import datetime
import xlsxwriter
import csv
import xlwt


def index(request):
    template = 'form/index.html'
    for document in Document.objects.all():
        if document.date is None:
            document.delete()
    if request.method == 'GET':
        ricerca = request.GET.get('search', '')
        ordine = request.GET.get('order', '')
        if 'nameup' == ordine:
            documents_list = Document.objects.filter(titolo__contains=ricerca).order_by('-titolo', '-date')
        elif 'namedown' == ordine:
            documents_list = Document.objects.filter(titolo__contains=ricerca).order_by('titolo', '-date')
        elif 'dataup' == ordine:
            documents_list = Document.objects.filter(titolo__contains=ricerca).order_by('-date', 'titolo')
        elif 'datadown' == ordine:
            documents_list = Document.objects.filter(titolo__contains=ricerca).order_by('date', 'titolo')
        else:
            documents_list = Document.objects.filter(titolo__contains=ricerca).order_by('titolo', '-date')
        paginator = Paginator(documents_list, 15, allow_empty_first_page=True)
        page = request.GET.get('page')
        documents = paginator.get_page(page)
        page_list = [i for i in range(1, paginator.num_pages + 1)]
        context = {'documents': documents, 'page_list': page_list}
        return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse('form:index'))


def detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == 'POST':
        compiled_doc = CompiledDoc(document=document, date=datetime.datetime.now())
        compiled_doc.save()
        fields = Field.objects.filter(document=document)
        for field in fields:
            comp_field = CompiledField(field=field, content=request.POST.get(field.name, 'off'),
                                       compiled_doc=compiled_doc, name=field.name)
            comp_field.save()
        return HttpResponseRedirect(reverse('form:submit', args=(document_id,)))
    template = 'form/detail.html'
    namelist = []
    create_input(document, 'textarea', 80, namelist, True)
    create_input(document, 'field', 7, namelist, True)
    find_input(document, namelist, 'checkbox', '<input.*?type="checkbox".*?/>')
    find_input(document, namelist, 'radiobutton', '<input.*?type="radio".*?/>')
    find_input(document, namelist, 'select', '<select.*?</select>')
    context = {'document': document}
    return render(request, template, context)


def create_input(document, fieldtype, us, namelist=None, save=False):
    if namelist is None:
        namelist = []
    name = ''
    n = 1
    field_match = re.search(r'_{' + str(us) + '}_*', str(document.content))
    while field_match is not None:
        inputtype = 'text'

        # Trova e/o assegna nome
        name_match = re.search(r'\[.*?\]', str(document.content)[field_match.end():])
        if name_match is not None and name_match.start() == 0:
            name = findname(name_match)
            inputtype = findtype(name_match)
            document.content = re.sub(r'\[.*?\]', "", str(document.content), 1)
        if not checkname(name, namelist):
            if save is True:
                name = fieldtype + str(n)
                namelist.append(name)
                n = n + 1
            else:
                name = fieldtype

        # crea field
        if save:
            try:
                field = Field.objects.get(document=document, name=name)
            except ObjectDoesNotExist:
                field = Field(document=document, name=name)
            field.save()

        if fieldtype == 'textarea':
            document.content = re.sub(r'_{80}_*', '<textarea name="' + str(name) +
                                      '" class="form-control" rows="5" cols="100" /></textarea>', str(document.content),
                                      1)
        else:
            if inputtype == 'testo':
                document.content = re.sub(r'_{7}_*', '<input type="text" name="' + str(name) +
                                          '" maxlength="100" class="form-control" />', str(document.content), 1)
            elif inputtype == 'obbligatorio':
                document.content = re.sub(r'_{7}_*', '<input type="text" name="' + str(name) +
                                          '" maxlength="100" class="form-control" required />', str(document.content), 1
                                          )
            elif inputtype == 'numero':
                document.content = re.sub(r'_{7}_*', '<input type="number" name="' + str(name) +
                                          '" maxlength="100" class="form-control" />', str(document.content), 1)
            elif inputtype == 'data':
                document.content = re.sub(r'_{7}_*', '<input type="date" name="' + str(name) +
                                          '" maxlength="100" class="form-control" />', str(document.content), 1)
            elif inputtype == 'email':
                document.content = re.sub(r'_{7}_*', '<input type="email" name="' + str(name) +
                                          '" maxlength="100" class="form-control" />', str(document.content), 1)
            else:
                document.content = re.sub(r'_{7}_*', '<input type="text" name="' + str(name) +
                                          '" maxlength="100" class="form-control" />', str(document.content), 1)

        # nuova ricerca
        field_match = re.search(r'_{' + str(us) + '}_*', str(document.content))
    return document


def findname(match):
    virgola_match = re.search(r',', match.group())
    if virgola_match is None:
        return match.group()[1:-1]
    name_match = re.search(r'\[.*?,', match.group())
    if name_match is not None:
        return name_match.group()[1:-1]
    return ""


def findtype(match):
    virgola_match = re.search(r',', match.group())
    if virgola_match is None:
        return ""
    type_match = re.search(r',.*?\]', match.group())
    if type_match is not None:
        return type_match.group()[1:-1]
    return ""


def find_input(document, namelist, typename, match):
    name = ''
    n = 1
    new_content = str(document.content)
    field_match = re.search(match, new_content)
    while field_match is not None:

        # Trova e/o assegna nome
        name_match = re.search(r'name=".*?"', field_match.group())
        if name_match is not None:
            name = name_match.group()[6:-1]
        if not checkname(name, namelist):
            name = typename + str(n)
            namelist.append(name)
            n = n + 1

        # crea field
        try:
            field = Field.objects.get(document=document, name=name)
        except ObjectDoesNotExist:
            field = Field(document=document, name=name)
        field.save()

        # nuova ricerca
        new_content = re.sub(match, '', new_content, 1)
        field_match = re.search(match, new_content)
    return document


def checkname(new_name, namelist):
    if str(new_name) == '':
        return False
    if not str(new_name).isalnum():
        return False
    for name in namelist:
        if str(name) == str(new_name):
            return False
    namelist.append(new_name)
    return True


@login_required
def edit(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document.titolo = form.cleaned_data['titolo']
            document.date = datetime.datetime.now()
            document.content = form.cleaned_data['content']
            document.save()
        return HttpResponseRedirect(reverse('form:edit', args=(document_id,)))
    form = DocumentForm(initial={'titolo': document.titolo, 'content': document.content})
    create_input(document, 'textarea', 80)
    create_input(document, 'field', 7)
    template = 'form/edit.html'
    context = {'document': document, 'form': form}
    return render(request, template, context)


@login_required
def new(request):
    document = Document()
    document.titolo = 'Nuovo documento'
    document.content = ''
    document.save()
    return HttpResponseRedirect(reverse('form:edit', args=(document.id,)))


def create_pdf(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    name = str(document.titolo).replace(' ', '_')
    response = HttpResponse(content_type='form/pdf')
    response['Content-Disposition'] = "filename=" + str(name) + ".pdf"
    myhtml = document.content
    myhtml = re.sub(r'\[.*?\]', "", myhtml)
    myhtml = re.sub(r'<input.*?type="checkbox".*?/>', "[ ]", myhtml)
    myhtml = re.sub(r'<input.*?type="radio".*?/>', "O", myhtml)
    myhtml = re.sub(r'<select.*?</select>', "__________", myhtml)
    pdf = pisa.CreatePDF(myhtml, dest=response, link_callback=link_callback)
    if pdf.err:
        return render(request, 'We had some errors <pre>' + myhtml + '</pre>')
    return response


def link_callback(uri):
    # Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    surl = settings.STATIC_URL
    sroot = settings.STATIC_ROOT
    murl = settings.MEDIA_URL
    mroot = settings.MEDIA_ROOT
    if uri.startswith(murl):
        path = os.path.join(mroot, uri.replace(murl, ""))
    elif uri.startswith(surl):
        path = os.path.join(sroot, uri.replace(surl, ""))
    else:
        return uri
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (surl, murl))
    return path


@login_required
def registrations(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    compiled_docs = CompiledDoc.objects.filter(document=document).order_by('date')
    template = 'form/registrations.html'
    context = {'document': document, 'compiled_docs': compiled_docs}
    return render(request, template, context)


@login_required
def export_xlsx(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    name = str(document.titolo).replace(' ', '_')
    compiled_docs = CompiledDoc.objects.filter(document=document).order_by('date')

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(str(name)[:30])

    bold = workbook.add_format({'bold': True})

    r = 1
    for comp_doc in compiled_docs:
        comp_fields = CompiledField.objects.filter(compiled_doc=comp_doc)
        if compiled_docs[compiled_docs.count() - 1] is comp_doc:
            i = 0
            for comp_filed in comp_fields:
                worksheet.write(0, i, str(comp_filed.name), bold)
                i = i + 1
        c = 0
        for comp_filed in comp_fields:
            worksheet.write(r, c, str(comp_filed.content))
            c = c + 1
        r = r + 1

    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; ' + 'filename=' + str(name)[:30] + '.xlsx'
    return response


@login_required
def export_csv(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    name = str(document.titolo).replace(' ', '_')
    compiled_docs = CompiledDoc.objects.filter(document=document).order_by('date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; ' + 'filename=' + str(name)[:30] + '.csv'
    writer = csv.writer(response)

    for comp_doc in compiled_docs:
        if compiled_docs[compiled_docs.count() - 1] is comp_doc:
            comp_fields = CompiledField.objects.filter(compiled_doc=comp_doc)
            lista = [comp_filed.name for comp_filed in comp_fields]
            writer.writerow(lista)
    writer.writerow([])
    for comp_doc in compiled_docs:
        comp_fields = CompiledField.objects.filter(compiled_doc=comp_doc)
        lista = [comp_filed.content for comp_filed in comp_fields]
        writer.writerow(lista)

    return response


@login_required
def export_xls(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    name = str(document.titolo).replace(' ', '_')
    compiled_docs = CompiledDoc.objects.filter(document=document).order_by('date')

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; ' + 'filename=' + str(name)[:30] + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(str(name)[:30])

    bold = xlwt.XFStyle()
    bold.font.bold = True

    font_style = xlwt.XFStyle()

    r = 1
    for comp_doc in compiled_docs:
        comp_fields = CompiledField.objects.filter(compiled_doc=comp_doc)
        if compiled_docs[compiled_docs.count() - 1] is comp_doc:
            i = 0
            for comp_filed in comp_fields:
                ws.write(0, i, str(comp_filed.name), bold)
                i = i + 1
        c = 0
        for comp_filed in comp_fields:
            ws.write(r, c, str(comp_filed.content), font_style)
            c = c + 1
        r = r + 1

    wb.save(response)

    return response


class SubmitView(generic.DetailView):
    model = Document
    template_name = 'form/submit.html'
