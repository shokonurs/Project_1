# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Molecular_state, Reference_publication, Constant_type, Source_type, Diatomic_constant, Preferred_set,Electronic_symmetry, New_data

# Register your models here.

admin.site.register(Molecular_state)
admin.site.register(Reference_publication)
admin.site.register(Constant_type)
admin.site.register(Source_type)
admin.site.register(Diatomic_constant)
admin.site.register(Preferred_set)
admin.site.register(Electronic_symmetry)
admin.site.register(New_data)
