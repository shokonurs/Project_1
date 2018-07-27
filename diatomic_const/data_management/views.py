# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import loader
from django.db import connection

from .models import Molecular_state,  Reference_publication, Constant_type, Source_type, Diatomic_constant
from .forms import Molecular_state_form, Reference_publication_form, Reference_publication_from_bib_form, Diatomic_constant_form

@login_required
def index(request):
    table_list = { 
        u'Molecular_states',
        u'Reference_publications',
        # u'Constant_types',
        # u'Source_types',
        u'Diatomic_constants'
    }
    context = { 'table_list': table_list }
    return render(request, 'data_management/index.html', context)

@login_required
def molecular_state_list(request):
    molecular_state_list = Molecular_state.objects.order_by('name')[:]
    context = {	'molecular_state_list': molecular_state_list }
    return render(request, 'data_management/molecular_state_list.html', context)

@login_required
def reference_publication_list(request):
    reference_publication_list = Reference_publication.objects.order_by('reference_publication_tag')[:]
    context = {	'reference_publication_list': reference_publication_list }
    return render(request, 'data_management/reference_publication_list.html', context)

@login_required
def constant_type_list(request):
    constant_type_list = Constant_type.objects.order_by('symbol')[:]
    context = {	'constant_type_list': constant_type_list }
    return render(request, 'data_management/constant_type_list.html', context)

@login_required
def source_type_list(request):
    source_type_list = Source_type.objects.order_by('source_type')[:]
    print source_type_list
    context = {	'source_type_list': source_type_list }
    return render(request, 'data_management/source_type_list.html', context)

@login_required
def diatomic_constant_list(request):
    diatomic_constant_list = Diatomic_constant.objects.order_by('reference_publication')[:]
    context = {	'diatomic_constant_list': diatomic_constant_list }
    return render(request, 'data_management/diatomic_constant_list.html', context)


@login_required
def molecular_state_detail(request, molecular_state_id):
    try:
       molecular_state  = Molecular_state.objects.get(pk=molecular_state_id)
    except Molecular_state.DoesNotExist:
        raise Http404("Molecular state does not exist")
    if request.method == "POST":
	form = Molecular_state_form(request.POST, instance=molecular_state)
        if form.is_valid():
            molecular_state = form.save(commit=False)
            molecular_state.user_entered = request.user
            # molecular_state.date_entered = timezone.now()
            molecular_state.save()
            return redirect('/data_management/Molecular_states/')

    else:
        form = Molecular_state_form(instance=molecular_state)

    context = {
	'molecular_state': molecular_state,
	'form' : form
    }
    return render(request, 'data_management/molecular_state.html', context)


@login_required
def reference_publication_detail(request, reference_publication_id):
    try:
       reference_publication  = Reference_publication.objects.get(pk=reference_publication_id)
    except Reference_publication.DoesNotExist:
        raise Http404("Reference publication does not exist")
    if request.method == "POST":
	form = Reference_publication_form(request.POST, instance=reference_publication)
        if form.is_valid():
            reference_publication = form.save(commit=False)
            reference_publication.user_entered = request.user
            # reference_publication.date_entered = timezone.now()
            reference_publication.save()
            return redirect('/data_management/Reference_publications/')

    else:
        form = Reference_publication_form(instance=reference_publication)

    context = {
	'reference_publication': reference_publication,
	'form' : form
    }
    return render(request, 'data_management/reference_publication.html', context)


@login_required
def diatomic_constant_detail(request, diatomic_constant_id):
    try:
       diatomic_constant  = Diatomic_constant.objects.get(pk=diatomic_constant_id)
    except diatomic_constant.DoesNotExist:
        raise Http404("Diatomic constant does not exist")
    if request.method == "POST":
	form = Diatomic_constant_form(request.POST, instance=diatomic_constant)
        if form.is_valid():
            diatomic_constant = form.save(commit=False)
            diatomic_constant.user_entered = request.user
            # diatomic_constant.date_entered = timezone.now()
            diatomic_constant.save()
            return redirect('/data_management/Diatomic_constants/')

    else:
        form = Diatomic_constant_form(instance=diatomic_constant)

    context = {
	'diatomic_constant': diatomic_constant,
	'form' : form
    }
    return render(request, 'data_management/diatomic_constant.html', context)


@login_required
def molecular_state_new(request):
    if request.method == "POST":
	form = Molecular_state_form(request.POST)
        if form.is_valid():
            molecular_state = form.save(commit=False)
            molecular_state.user_entered = request.user
            # molecular_state.date_entered = timezone.now()
            molecular_state.save()
            return redirect('/data_management/Molecular_states/')

    else:
        form = Molecular_state_form()

    context = {
	'form' : form
    }
    return render(request, 'data_management/molecular_state.html', context)


@login_required
def reference_publication_new(request):
    if request.method == "POST":
	form = Reference_publication_form(request.POST)
        if form.is_valid():
            reference_publication = form.save(commit=False)
            reference_publication.user_entered = request.user
            # reference_publication.date_entered = timezone.now()
            reference_publication.save()
            return redirect('/data_management/Reference_publications/')

    else:
        form = Reference_publication_form()

    context = {
	'form' : form
    }
    return render(request, 'data_management/reference_publication.html', context)


@login_required
def reference_publication_new_from_bib(request):
    if request.method == "POST":
	form = Reference_publication_from_bib_form(request.POST)
        if form.is_valid():            
            form.save()
            return redirect('/data_management/Reference_publications/')

    else:
        form = Reference_publication_from_bib_form()

    context = {
	'form' : form
    }
    return render(request, 'data_management/reference_from_bib.html', context)



@login_required
def diatomic_constant_new(request):
    if request.method == "POST":
	form = Diatomic_constant_form(request.POST)
        if form.is_valid():
            diatomic_constant = form.save(commit=False)
            diatomic_constant.user_entered = request.user
            # diatomic_constant.date_entered = timezone.now()
            diatomic_constant.save()
            return redirect('/data_management/Diatomic_constants/')

    else:
        form = Diatomic_constant_form()

    context = {
	'form' : form
    }
    return render(request, 'data_management/diatomic_constant.html', context)
