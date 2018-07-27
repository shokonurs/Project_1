from django.conf.urls import url
from . import views



urlpatterns=[
	url(r'^$', views.index, name='index'),

	# Here i am adding new url pattern to see if it works

	url(r'^files/$', views.files, name='files'), 
    url(r'^molecules_list/$',views.unique_molecules, name='molecules_list'),
   # url(r'^test/$',views.table_for_molecule_debug_1, name='table'),
    url(r'^molecules_list/(?P<molecule_name>[\w\-]+)/$', views.table_for_molecule, name='molecule_details'),
    #url(r'^molecules_list/next/(?P<state_type>[\w\-]+)/$', views.constants, name='constants'),
   # url(r'^molecules_list/(?P<symbol>[\w\-]+)/(?P<state_type>[\w\W]+)/$', views.constants, name='testing'),
    url(r'^main_table/$',views.new_function, name='main_table'),
    url(r'^main_data/$', views.main_data, name='main_data'),
    url(r'^molecules_list/(?P<isotopolog>[\w\W]+)/(?P<paper>[\w\W]+)/$', views.paper_info, name='paper_info'),
]

