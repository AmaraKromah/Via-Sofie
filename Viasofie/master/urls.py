from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),  # bij home url doorverwijzen naar index
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^verkoper/$', views.VerkoperView.as_view(), name='verkoper'),
    url(r'^advice/$', views.AdviceView.as_view(), name='advice'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^loggedin/$', views.Loggedin.as_view(), name='loggedin'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^resetpassword/passwordsent/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^resetpassword/$', auth_views.password_reset, name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^panden/$', views.PandenView.as_view(), name='panden'),
    url(r'^pand/(?P<pk>[0-9]+)/$', views.PandDetail.as_view(), name='pand_detail'),
    url(r'partner/$', views.PartnerView.as_view(), name='partner'),
]