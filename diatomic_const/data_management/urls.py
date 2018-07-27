from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Molecular_states/$', views.molecular_state_list, name='Molecular States'),
    url(r'^Reference_publications/$', views.reference_publication_list, name='Reference Publications'),
    url(r'^Constant_types/$', views.constant_type_list, name='Constant Types'),
    url(r'^Source_types/$', views.source_type_list, name='Source Types'),
    url(r'^Diatomic_constants/$', views.diatomic_constant_list, name='Diatomic Constants'),

    url(r'^Molecular_states/(?P<molecular_state_id>[0-9]+)/$', views.molecular_state_detail, name='molecular_state_detail'),
    url(r'^Reference_publications/(?P<reference_publication_id>[0-9]+)/$', views.reference_publication_detail, name='reference_publication_detail'),
    url(r'^Diatomic_constants/(?P<diatomic_constant_id>[0-9]+)/$', views.diatomic_constant_detail, name='diatomic_constant_detail'),

    url(r'^Molecular_states/new/$', views.molecular_state_new, name='Add molecular state'),
    url(r'^Reference_publications/new/$', views.reference_publication_new, name='Add reference publication'),
    url(r'^Reference_publications/new_from_bib/$', views.reference_publication_new_from_bib, name='Add reference publication from BibTeX'),
    url(r'^Diatomic_constants/new/$', views.diatomic_constant_new, name='Add diatomic constant'),
]

