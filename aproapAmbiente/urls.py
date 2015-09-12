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
    url(r'^cronograma/(?P<usuario>[\w-]+)/$', 'aproap.views.cronograma', name='cronograma'),
    url(r'^showcronograma/$', 'aproap.views.showcronograma', name='showcronograma'),
    url(r'^salvacronograma/$', 'aproap.views.salvaCronograma', name='salvacronograma'),
    url(r'^vincular/(?P<id>[0-9]+)/(?P<unidade>[0-9]+)/(?P<pk>[0-9]+)/$', 'aproap.views.vincularItem', name='vincular'),
    url(r'^espacos/$', 'aproap.views.listagem', name='listagem'),
    url(r'^salvar_espaco/$', 'aproap.views.salvarEspaco', name='salvar_espaco'),
    url(r'^projeto/(?P<slug>[\w-]+)/ideias/$', 'aproap.views.inserirIdeia', name='ideias'),
    url(r'^salvar_ideia/(?P<pk>[0-9]+)/$', 'aproap.views.salvarIdeia', name='salvar_ideia'),
    url(r'^lobby/(?P<slug>[\w-]+)/$', 'aproap.views.lobbyProjeto', name='lobby'),
    url(r'^terminar_etapa1/(?P<pk>[0-9]+)/$', 'aproap.views.terminaEtapa1', name='terminar_etapa1'),
    url(r'^terminar_etapa2/(?P<pk>[0-9]+)/$', 'aproap.views.terminaEtapa2', name='terminar_etapa2'),
    url(r'^terminar_etapa3/(?P<pk>[0-9]+)/$', 'aproap.views.terminaEtapa3', name='terminar_etapa3'),
    url(r'^projeto/(?P<slug>[\w-]+)/votar/$', 'aproap.views.votarIdeia', name='votar'),
    url(r'^fechar_voto/$', 'aproap.views.fecharVoto', name='fechar_voto'),
    url(r'^salva_texto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.salvaTexto', name='salva_texto'),
    url(r'^salva_texto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/editando/(?P<id>[0-9]+)/$', 'aproap.views.atualizaTexto', name='atualiza_texto'),
    url(r'^projeto/(?P<slug>[\w-]+)/conhecimento_previo/$', 'aproap.views.conhecimentoPrevio', name='conhecimentoPrevio'),
    url(r'^salvar_conhecimento/(?P<pk>[0-9]+)/$', 'aproap.views.salvarConhecimento', name='salvar_conhecimento'),
    url(r'^participar_projeto/(?P<slug>[\w-]+)/$', 'aproap.views.participarProjeto', name='participar_projeto'),
    url(r'^precisa_ajuda/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.precisaAjuda', name='precisa_ajuda'),
    url(r'^projeto/(?P<slug>[\w-]+)/unidades/$', 'aproap.views.unidadesInvestigacao', name='unidades'),
    url(r'^projeto/(?P<slug>[\w-]+)/unidade/(?P<unidade>[0-9]+)/$', 'aproap.views.unidadesInvestigacao', name='unidades'),
    url(r'^projeto/(?P<slug>[\w-]+)/unidade/(?P<unidade>[0-9]+)/detalhes/$', 'aproap.views.detalhesUnidade', name='detalhesUnidade'),
    url(r'^projeto/(?P<slug>[\w-]+)/unidade/(?P<unidade>[0-9]+)/item/(?P<itemslug>[\w-]+)/$', 'aproap.views.detalhesItem', name='detalhesItem'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/elementos_textuais/$', 'aproap.views.elementosTextuais', name='elementosTextuais'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/elementos_textuais/editor/$', 'aproap.views.redator', name='redator'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/elementos_textuais/editando/(?P<id>[0-9]+)/$', 'aproap.views.modoEdicao', name='modoEdicao'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/elementos_textuais/visualizando/(?P<id>[0-9]+)/$', 'aproap.views.modoLeitura', name='modoLeitura'),
    url(r'^areaDeTrabalho/(?P<pk>[0-9]+)/(?P<id>[0-9]+)/$', 'aproap.views.areaDeTrabalho', name='area'),
    url(r'^inserir_tarefa/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.insereTarefa', name='inserirTarefa'),
     url(r'^inserir_item/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/$', 'aproap.views.insereItem', name='inserirItem'),
    url(r'^vincular_tarefa/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/(?P<slugtarefa>[\w-]+)/$', 'aproap.views.vincularTarefa', name='vincularTarefa'),
    url(r'^inserir_elementoTextual/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.salvarElementoTextual', name='salvarElementoTextual'),
)
