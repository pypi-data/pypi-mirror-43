from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sepa/exports/$', views.ExportListView.as_view(),
        name='export'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sepa/exports/(?P<id>\d+).xml$', views.DownloadView.as_view(),
        name='download'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sepa/exports/(?P<id>\d+)/orders/$',
        views.OrdersView.as_view(),
        name='orders'),
]
