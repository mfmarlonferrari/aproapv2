from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aproapAmbiente.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'aproap.views.index', name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'}),
    url(r'^cadastrar/$', 'aproap.views.cadastrar', name='cadastrar'),
    url(r'^espacos/$', 'aproap.views.listagem', name='listagem'),
    url(r'^salvar_espaco/$', 'aproap.views.salvarEspaco', name='salvar_espaco'),
    url(r'^ideias/(?P<pk>[0-9]+)/$', 'aproap.views.inserirIdeia', name='ideias'),
    url(r'^salvar_ideia/(?P<pk>[0-9]+)/$', 'aproap.views.salvarIdeia', name='salvar_ideia'),
    url(r'^lobby/(?P<pk>[0-9]+)/$', 'aproap.views.lobbyProjeto', name='lobby'),
    url(r'^terminar_etapa1/(?P<pk>[0-9]+)/$', 'aproap.views.terminaEtapa1', name='terminar_etapa1'),
    url(r'^terminar_etapa2/(?P<pk>[0-9]+)/$', 'aproap.views.terminaEtapa2', name='terminar_etapa2'),
    url(r'^terminar_etapa3/(?P<pk>[0-9]+)/$', 'aproap.views.terminaEtapa3', name='terminar_etapa3'),
    url(r'^votar/(?P<pk>[0-9]+)/$', 'aproap.views.votarIdeia', name='votar'),
    url(r'^fechar_voto/$', 'aproap.views.fecharVoto', name='fechar_voto'),
    url(r'^conhecimentoPrevio/(?P<pk>[0-9]+)/$', 'aproap.views.conhecimentoPrevio', name='conhecimentoPrevio'),
    url(r'^salvar_conhecimento/(?P<pk>[0-9]+)/$', 'aproap.views.salvarConhecimento', name='salvar_conhecimento'),
    url(r'^participar_projeto/(?P<pk>[0-9]+)/$', 'aproap.views.participarProjeto', name='participar_projeto'),
    url(r'^unidades/(?P<pk>[0-9]+)/$', 'aproap.views.unidadesInvestigacao', name='unidades'),
    url(r'^unidades/(?P<pk>[0-9]+)/(?P<unidade>[0-9]+)$', 'aproap.views.unidadesInvestigacao', name='unidades'),
    url(r'^detalhes_unidade/(?P<pk>[0-9]+)/(?P<unidade>[0-9]+)/$', 'aproap.views.detalhesUnidade', name='detalhesUnidade'),
    url(r'^areaDeTrabalho/(?P<pk>[0-9]+)/(?P<id>[0-9]+)/$', 'aproap.views.areaDeTrabalho', name='area'),
)
