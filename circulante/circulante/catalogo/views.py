# coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.forms.models import inlineformset_factory
from django.utils.http import urlquote

from .models import Publicacao, Credito

from .forms import PublicacaoModelForm

from isbn import validatedISBN10

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
    
    
    
def catalogar(request):
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
    if request.method == "POST":
        formulario = PublicacaoModelForm(request.POST)
        if formulario.is_valid():
            publicacao = formulario.save()
            formset = CreditoInlineFormSet(request.POST, instance=publicacao)
            formset.save()
            titulo = formulario.cleaned_data['titulo']
            return HttpResponseRedirect(reverse('busca')+'?q='+ urlquote(titulo) )
            # Do something.
    else:
        formulario = PublicacaoModelForm()
        formset = CreditoInlineFormSet()
    return render(request, 'catalogo/catalogar.html', 
        {'formulario': formulario, 
         'formset': formset})    
    
    
    
        
def editar(request, pk):
    pub = get_object_or_404(Publicacao, pk=pk)
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
     
    if request.method == 'POST':
         formulario = PublicacaoModelForm(request.POST, instance=pub)
         formset = CreditoInlineFormSet(request.POST, instance=pub)
         if formulario.is_valid() and formset.is_valid():
             formulario.save()
             formset.save()
             titulo = formulario.cleaned_data['titulo']
             return HttpResponseRedirect(reverse('busca')+'?q=' + urlquote(titulo) )
    else:
         formulario = PublicacaoModelForm(instance=pub)
         formset = CreditoInlineFormSet(instance=pub)
         

    return render(request, 'catalogo/catalogar.html', 
        {'formulario': formulario, 
         'formset': formset})    
         
         
         
         
     
     
    
    