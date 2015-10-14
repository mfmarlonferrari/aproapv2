from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'aproap.views.index', name='index'),
    url(r'^login/$', 'aproap.views.custom_login', name='verifLogin'),
    url(r'^login2/$', 'django.contrib.auth.views.login', {'template_name':'login.html'}),
    url(r'^cadastrar/$', 'aproap.views.cadastrar', name='cadastrar'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login2/'}),
    url(r'^salvar_usuario/$', 'aproap.views.salvaUsuario', name='salvaUsuario'),
    url(r'^projeto/(?P<slug>[\w-]+)/sintese/$', 'aproap.views.sinteseQi', name='sinteseQi'),
    url(r'^contato/$', 'aproap.views.contato', name='contato'),
    url(r'^envia_email/$', 'aproap.views.enviaEmail', name='email'),
    url(r'^cronograma/(?P<usuario>[\w-]+)/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/$', 'aproap.views.cronograma',
        name='cronograma'),
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
    url(r'^salva_texto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.salvaTexto',
        name='salva_texto'),
    url(r'^salva_texto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/editando/(?P<id>[0-9]+)/$',
        'aproap.views.atualizaTexto', name='atualiza_texto'),
    url(r'^projeto/(?P<slug>[\w-]+)/conhecimento_previo/$', 'aproap.views.conhecimentoPrevio',
        name='conhecimentoPrevio'),
    url(r'^salvar_conhecimento/(?P<pk>[0-9]+)/$', 'aproap.views.salvarConhecimento', name='salvar_conhecimento'),
    url(r'^participar_projeto/(?P<slug>[\w-]+)/$', 'aproap.views.participarProjeto', name='participar_projeto'),
    url(r'^precisa_ajuda/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.precisaAjuda',
        name='precisa_ajuda'),
    url(r'^projeto/(?P<slug>[\w-]+)/unidades/$', 'aproap.views.unidadesInvestigacao', name='unidades'),
    url(r'^projeto/(?P<slug>[\w-]+)/unidade/(?P<unidade>[0-9]+)/$', 'aproap.views.unidadesInvestigacao',
        name='unidades'),
    url(r'^projeto/(?P<slug>[\w-]+)/unidade/(?P<unidade>[0-9]+)/detalhes/$', 'aproap.views.detalhesUnidade',
        name='detalhesUnidade'),
    url(r'^projeto/(?P<slug>[\w-]+)/unidade/(?P<unidade>[0-9]+)/item/(?P<itemslug>[\w-]+)/$',
        'aproap.views.detalhesItem', name='detalhesItem'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/elementos_textuais/$',
        'aproap.views.elementosTextuais', name='elementosTextuais'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/elementos_textuais/editor/$',
        'aproap.views.redator', name='redator'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/elementos_textuais/editando/(?P<id>[0-9]+)/$',
        'aproap.views.modoEdicao', name='modoEdicao'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/elementos_textuais/visualizando/(?P<id>[0-9]+)/$',
        'aproap.views.modoLeitura', name='modoLeitura'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/mapas_conceituais/editor/$',
        'aproap.views.mapa', name='mapa'),
    url(r'^projeto/(?P<slug>[\w-]+)/(?P<itemslug>[\w-]+)/sintese/$',
        'aproap.views.mostraSintese', name='mostraSintese'),
    url(r'^areaDeTrabalho/(?P<pk>[0-9]+)/(?P<id>[0-9]+)/$', 'aproap.views.areaDeTrabalho', name='area'),
    url(r'^inserir_tarefa/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.insereTarefa',
        name='inserirTarefa'),
    url(r'^inserir_item/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/$', 'aproap.views.insereItem', name='inserirItem'),
    url(r'^vincular_tarefa/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/(?P<slugtarefa>[\w-]+)/$',
        'aproap.views.vincularTarefa', name='vincularTarefa'),
    url(r'^inserir_elementoTextual/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$',
        'aproap.views.salvarElementoTextual', name='salvarElementoTextual'),
    url(r'^postar_conversa/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.postarConversa',
        name='postar_conversa'),
    url(r'^vincular_tarefaDocumento/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/(?P<idDoc>[0-9]+)/$',
        'aproap.views.vinculaDocItem', name='vincularTarefaDoc'),
    url(r'^concluir_item/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.concluirItem',
        name='concluirItem'),
    url(r'^concluir_unidade/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/$', 'aproap.views.concluirItem', name='concluirItem'),
    url(r'^salvar_mapa/(?P<slug>[\w-]+)/(?P<unidade>[0-9]+)/(?P<itemslug>[\w-]+)/$', 'aproap.views.salvaMapa',
        name='salvaMapa'),
    url(r'^forum/(?P<slug>[\w-]+)/$', 'aproap.views.forum', name='forum'),
    url(r'^salvar_postagem/(?P<slug>[\w-]+)/$', 'aproap.views.salvaPost', name='salva_post'),
    url(r'^salvar_resposta/(?P<slug>[\w-]+)/(?P<postagemId>[0-9]+)/$', 'aproap.views.salvaResposta',
        name='salva_resposta'),


)
