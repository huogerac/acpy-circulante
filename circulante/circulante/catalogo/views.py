# coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.forms.models import inlineformset_factory
from django.utils.http import urlquote

from django.views.decorators.http import require_http_methods


from .models import Publicacao, Credito
from .forms import PublicacaoModelForm

from isbn import validatedISBN10
from httpdecorator import http_method

def busca(request):
    erros = []
    pubs = []
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            erros.append(u'Digite um termo para a busca.')
            
        #elif len(q) > 80:
        #    erros.append(u'Entre no mínimo com 80 caracteres.')
            
        else:
            isbn = validatedISBN10(q)
            if isbn:
                pubs = Publicacao.objects.filter(id_padrao=isbn)
            else:
                pubs = Publicacao.objects.filter(titulo__icontains=q)
            
    return render(request, 'catalogo/busca.html', 
                  {"erros": erros, "publicacoes": pubs, "q": q})

    
    
    
def catalogar_form_sem_creditos(request):
    if request.method == 'POST':
        #bound form
        formulario = PublicacaoModelForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            #dicionário com todas as informações do form
            titulo = formulario.cleaned_data['titulo']
            return HttpResponseRedirect(reverse('busca') + '?q=' + titulo )
    else:
        formulario = PublicacaoModelForm()
        
    return render(request, 'catalogo/catalogar.html',
                  {'formulario': formulario})
    



    
def pagina_catalogar(request, form_pub, form_cred):
    return render(request, 'catalogo/catalogar.html', 
        {'formulario': form_pub, 'formset': form_cred})
    
def pagina_busca(titulo):        
    return HttpResponseRedirect(reverse('busca')+'?q='+ urlquote(titulo) )


  

    
@http_method('get')
def catalogar(request):
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
    form_pub = PublicacaoModelForm()
    form_cred = CreditoInlineFormSet()
    return pagina_catalogar(request, form_pub, form_cred)


@http_method('post')
def catalogar(request):
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
    form_pub = PublicacaoModelForm(request.POST)
    form_cred = CreditoInlineFormSet()
    if not create_publicacao(request, form_pub):
        return pagina_catalogar(request, form_pub, form_cred)
    return pagina_busca(form_pub.cleaned_data['titulo'])


@http_method('post')
def editar(request, pk):
    pub = get_object_or_404(Publicacao, pk=pk)
    
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
    form_pub = PublicacaoModelForm(request.POST, instance=pub)
    form_cred = CreditoInlineFormSet(request.POST, instance=pub)
    if not update_publicacao(pub, form_pub, form_cred):
        return pagina_catalogar(request, form_pub, form_cred)
    return pagina_busca(form_pub.cleaned_data['titulo'])


@http_method('get')
def editar(request, pk):
    pub = get_object_or_404(Publicacao, pk=pk)
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
    form_pub = PublicacaoModelForm(instance=pub)
    form_cred = CreditoInlineFormSet(instance=pub)
    return pagina_catalogar(request, form_pub, form_cred)

    
def create_publicacao(request, form_pub):
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
    
    if not form_pub.is_valid():
        return False
    
    pub = form_pub.save()
    form_cred = CreditoInlineFormSet(request.POST, instance=pub)
    form_cred.save()
    
    return True

def update_publicacao(pub, form_pub, form_cred):
    if not form_pub.is_valid() or not form_cred.is_valid():
        return False
     
    form_pub.save()
    form_cred.save()

    return True    