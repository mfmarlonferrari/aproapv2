from django.shortcuts import render_to_response
from aproap.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max
from django import template
from itertools import chain
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


register = template.Library()

def escreveHistorico(aluno, tarefa, data, slug, link):
    qualProjeto = espacoProjeto.objects.get(slugProjeto=slug)
    registro = historicoAluno.objects.create(aluno=aluno, tarefa=tarefa, data=data,
                                             qualEspaco=qualProjeto, link=link)
    registro.save()


# funcao para verificar se o usuario ja esta logado, se sim, redireciona ao espaco
def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/espacos/")
    else:
        return HttpResponseRedirect("/login2/")


def index(request):
    return render_to_response('index.html', {})


def sinteseQi(request, slug):
    qualEspaco = espacoProjeto.objects.get(slugProjeto=slug)
    projeto = Projeto.objects.get(espaco=qualEspaco)
    conhecimentos = unidadeInvestigacao.objects.filter(qualProjeto=projeto)
    textos = textoProduzido.objects.filter(vinculadoItem__qualProjeto=projeto)
    context = dict(projeto=projeto, conhecimentos=conhecimentos, textos=textos, slug=slug)
    c = RequestContext(request, context)
    return render_to_response('mapaQI.html', c)


def mostraSintese(request, slug, itemslug):
    titulo = 'SINTESE %s' %itemslug
    texto = textoProduzido.objects.get(titulo=titulo)
    context = dict(texto=texto, slug=slug, itemslug=itemslug)
    c = RequestContext(request, context)
    return render_to_response('visualizadorsintese.html', c)


def cadastrar(request):
    context = dict()
    c = RequestContext(request, context)
    return render_to_response('cadastrar.html', c)


@login_required
def salvaUsuario(request):
    try:
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        email = request.POST['email']
        senha = make_password(senha)
        user = User(username=usuario, password=senha, email=email)
        user.is_staff = False
        user.is_superuser = False
        user.save()
    except:
        return HttpResponseRedirect("/cadastrar/")
    return HttpResponseRedirect("/login2/")


def contato(request):
    context = dict()
    c = RequestContext(request, context)
    return render_to_response('contato.html', c)


def enviaEmail(request):
    nome = request.POST['nome']
    mensagem = request.POST['mensagem']
    emailRetorno = request.POST['email']
    salva = mensagemDeContato.objects.create(nome=nome, email=emailRetorno, mensagem=mensagem)
    salva.save()
    return HttpResponseRedirect('/contato/')


@login_required
def forum(request, slug):
    qualProjeto = espacoProjeto.objects.get(slugProjeto=slug)
    postagens = postagem.objects.filter(pertence=qualProjeto)
    respostasAoPost = respostas.objects.filter(forum=postagens)
    context = dict(slug=slug, postagens=postagens, respostas=respostasAoPost)
    c = RequestContext(request, context)
    return render_to_response('forum.html', c)


def salvaPost(request, slug):
    qualProjeto = espacoProjeto.objects.get(slugProjeto=slug)
    texto = request.POST['post']
    post = postagem.objects.create(usuario=request.user.username, texto=texto, pertence=qualProjeto)
    post.save()
    tarefa = 'criou um post no forum'
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/forum/%s/" % slug)

def salvaResposta(request, slug, postagemId):
    qualPost = postagem.objects.get(pk=postagemId)
    texto = request.POST['resposta']
    post = respostas.objects.create(usuario=request.user.username, resposta=texto, forum=qualPost)
    post.save()
    tarefa = 'respondeu um assunto no forum'
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/forum/%s/" % slug)


@login_required
def mapa(request, slug, unidade, itemslug):
    existente = mapaConceitual.objects.filter(pertence=itemslug, usuario=request.user.username)
    contExistente = existente.count()
    # pega o conteudo do mapa
    if contExistente == 1:
        existente = mapaConceitual.objects.get(pertence=itemslug, usuario=request.user.username)
    context = dict(slug=slug, unidade=unidade, itemslug=itemslug, existente=existente,
                   contExistente=contExistente)
    c = RequestContext(request, context)
    return render_to_response('mapaConceitual.html', c)


@login_required
def visualizaMapa(request, slug, unidade, itemslug):
    mapaTexto = mapaConceitual.objects.get(pertence=itemslug)
    context = dict(slug=slug, unidade=unidade, itemslug=itemslug, mapaTexto=mapaTexto)
    c = RequestContext(request, context)
    return render_to_response('mapaConceitual.html', c)


@login_required
def salvaMapa(request, slug, unidade, itemslug):
    #  verifica se ja ha um mapa associado a este usuario e item, se houver havera apenas a atualizacao
    existente = mapaConceitual.objects.filter(pertence=itemslug, usuario=request.user.username)
    contExistente = existente.count()
    texto = request.POST['conceitos']
    if contExistente == 1:
        existente = mapaConceitual.objects.select_for_update().filter(
            pertence=itemslug, usuario=request.user.username).update(conceitosRelacoes=texto)
        tarefa = 'editou seu mapa conceitual sobre %s' %itemslug
        link = 'nada ainda'
        escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    else:
        a = mapaConceitual.objects.create(pertence=itemslug, usuario=request.user.username, conceitosRelacoes=texto)
        a.save()
        tarefa = 'criou seu mapa conceitual sobre %s' %itemslug
        link = 'nada ainda'
        escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/%s/%s/mapas_conceituais/editor/" % (slug, unidade, itemslug))


@login_required
def showcronograma(request):
    # filtra as entradas cujo investigador seja o usuario atual e os prazos nao sejam nulos
    entries = unidadeInvestigacao.objects.filter(investigador=request.user.username, prazo__isnull=False,
                                                 prazoFinal__isnull=False)
    print entries
    json_list = []
    for entry in entries:
        title = entry.conhecimentoPrevio
        print title
        start = entry.prazo.strftime("%Y-%m-%d")
        print start
        end = entry.prazoFinal.strftime("%Y-%m-%d")
        print end
        json_entry = {'start': start, 'end': end, 'title': title}
        json_list.append(json_entry)
    return HttpResponse(json.dumps(json_list), content_type='application/json')


@login_required
def salvaCronograma(request):
    if request.method == 'POST':
        eventsJson = request.POST.get('eventsJson')
        jsonDec = json.loads(eventsJson)
        titulo, dataBruta, dataBrutaFinal = [], [], []
        # percorre os objetos do jsonDec
        for i in range(len(jsonDec)):
            titulo.append(jsonDec[i]['title'])
            # pega a data no formato com hora
            dataBruta.append(jsonDec[i]['start'])
            # se a data final for None, entao a data inicial e final devem ser no mesmo dia
            testeDtFinal = jsonDec[i]['end']
            if testeDtFinal is None:
                # recebe a mesma data de inicio
                dataBrutaFinal.append(jsonDec[i]['start'])
            else:
                # senao recebe a data final que nao esta vazia. Isto ocorre porque ao arrastar o item para
                # o calendario, o javascript nao preenche a data final como sendo a do mesmo dia em caso de tarefas
                # de apenas um dia.
                dataBrutaFinal.append(jsonDec[i]['end'])
        # rotina para formatar a data para salvamento
        dataApenas, dataApenasFinal = [], []
        for i in range(len(dataBruta)):
            # divide a data em dois itens data e hora
            divide = dataBruta[i].split('T')
            divideFinal = dataBrutaFinal[i].split('T')
            # pega apenas o item da data
            dataApenas.append(divide[0])
            dataApenasFinal.append(divideFinal[0])
        response_data = {}
        for i in range(len(titulo)):
            dataFormat = datetime.strptime(dataApenas[i], '%Y-%m-%d').date()
            dataFormatFinal = datetime.strptime(dataApenasFinal[i], '%Y-%m-%d').date()
            atualiza = unidadeInvestigacao.objects.select_for_update().filter(
                conhecimentoPrevio=titulo[i]).update(prazo=dataFormat, prazoFinal=dataFormatFinal)
        response_data['result'] = 'Create post successful!'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def cronograma(request, usuario, slug, unidade):
    itensSemPrazo = unidadeInvestigacao.objects.filter(
        investigador=request.user.username, prazo__isnull=True, prazoFinal__isnull=True)
    context = dict(itensSemPrazo=itensSemPrazo, slug=slug, unidade=unidade)
    c = RequestContext(request, context)
    return render_to_response('cronograma.html', c)


@login_required
def vincularItem(request, id, unidade, pk):
    slug = espacoProjeto.objects.get(pk=id).slugProjeto
    item = unidadeInvestigacao.objects.select_for_update().filter(id=pk).update(investigador=request.user.username)
    qualItem = unidadeInvestigacao.objects.get(id=pk).conhecimentoPrevio
    tarefa = 'ficou responsavel pelo item %s' %qualItem
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/detalhes/" % (slug, unidade))


@login_required
def listagem(request):
    espacos = espacoProjeto.objects.all()
    context = dict(espacos=espacos)
    c = RequestContext(request, context)
    return render_to_response('lista.html', c)


@login_required
def inserirIdeia(request, slug):
    projetoId = espacoProjeto.objects.get(slugProjeto=slug)
    espacoId = Projeto.objects.get(espaco=projetoId).id
    dono = request.user.username
    ideias = ideaDeQuestao.objects.filter(usuario=dono, espaco=projetoId)
    context = dict(ideias=ideias, espacoId=espacoId)
    c = RequestContext(request, context)
    return render_to_response('inserirIdeia.html', c)


@login_required
def detalhesUnidade(request, slug, unidade):
    pk = espacoProjeto.objects.get(slugProjeto=slug).id
    idProjeto = Projeto.objects.get(espaco=pk)
    # carrega as mensagens automaticas do usuario
    mensagens = mensagemAssistente.objects.filter(usuario=request.user.username)
    # itens ja completados
    qtdCompletados = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto,
                                                        nomeDoBloco=unidade, status=100).count()
    # quantidade de itens que precisam de ajuda, excluindo os que ja foram completados
    ajuda = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto,
                                               nomeDoBloco=unidade, precisaAjuda='1').exclude(status=100)
    qtdAjuda = ajuda.count()
    # filtra todos os conhecimentos sem investigador vinculado
    pendentes = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade, investigador='')
    qtdPendentes = pendentes.count()
    # filtra todos os conhecimentos cujo investigador exista
    todos = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade).exclude(investigador='')
    # verifica se o usuario possui itens a investigar sem cronograma
    semCronograma = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade,
                                                       investigador=request.user.username, prazo__isnull=True,
                                                       prazoFinal__isnull=True).count()
    # filtra todos os itens do usuario atual
    desteUsuario = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade,
                                                      investigador=request.user.username)
    # calcula o andamento da unidade pela media de andamento dos itens
    somaUnidade = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade).aggregate(
        total=Sum('status'))
    somaUnidadeValor = somaUnidade['total']
    qtdItens = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade).count()
    mediaDaUnidade = somaUnidadeValor / qtdItens
    context = dict(pendentes=pendentes, espacoId=pk, unidade=unidade,
                   qtdPendentes=qtdPendentes, todos=todos, semCronograma=semCronograma, desteUsuario=desteUsuario,
                   mediaDaUnidade=mediaDaUnidade, slug=slug, qtdAjuda=qtdAjuda,
                   ajuda=ajuda, qtdCompletados=qtdCompletados, mensagens=mensagens)
    c = RequestContext(request, context)
    return render_to_response('detalhesUnidade.html', c)


@login_required
def detalhesItem(request, slug, unidade, itemslug):
    item = unidadeInvestigacao.objects.get(slugConhecimento=itemslug).id
    vinculoItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    qualItem = unidadeInvestigacao.objects.get(pk=item).conhecimentoPrevio
    conversas = conversa.objects.filter(qualItem=vinculoItem)
    # quantos documentos associados ao item
    producoes = textoProduzido.objects.filter(vinculadoItem=vinculoItem).count()
    # verifica se o item possui cronograma
    prazoInicial = unidadeInvestigacao.objects.get(pk=item).prazo
    if prazoInicial is None:
        semCronograma = True
    else:
        semCronograma = False
    qualItemId = unidadeInvestigacao.objects.get(pk=item).id
    investigadorPrincipal = unidadeInvestigacao.objects.get(pk=item).investigador
    ajudante = tarefasItem.objects.filter(vinculoConhecimento=qualItemId).exclude(responsavel=investigadorPrincipal)
    ajudante = ajudante.exclude(responsavel='')
    qtdajudantes = ajudante.count()
    tarefasAndamento = tarefasItem.objects.filter(vinculoConhecimento=qualItemId).exclude(responsavel='')
    tarefasPendentes = tarefasItem.objects.filter(vinculoConhecimento=qualItemId, responsavel='')
    qtdTarefasPendentes = tarefasItem.objects.filter(vinculoConhecimento=qualItemId, responsavel='').count()
    # media do progresso
    mediaTarefas = vinculoItem.status
    qtdTarefasFinalizadas = tarefasItem.objects.filter(vinculoConhecimento=qualItemId, status=1).count()
    context = dict(tarefasPendentes=tarefasPendentes, tarefasAndamento=tarefasAndamento,
                   qualItem=qualItemId, item=item, qtdTarefasPendentes=qtdTarefasPendentes,
                   qtdajudantes=qtdajudantes, ajudantes=ajudante, slug=slug, unidade=unidade, itemslug=itemslug,
                   semCronograma=semCronograma, producoes=producoes, vinculoItem=vinculoItem, conversas=conversas,
                   mediaTarefas=mediaTarefas, qtdTarefasFinalizadas=qtdTarefasFinalizadas)
    c = RequestContext(request, context)
    return render_to_response('detalheItem.html', c)


@login_required
def concluirItem(request, slug, unidade, itemslug):
    qualItem = unidadeInvestigacao.objects.select_for_update().filter(slugConhecimento=itemslug).update(status=100)
    # cria um arquivo de texto da sintese
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    titulo = 'SINTESE %s' %itemslug
    texto = ''
    historico = '%s criou a sintese' % request.user.username
    doc = textoProduzido.objects.create(titulo=titulo, vinculadoItem=qualItem, texto=texto, historico=historico,
                                        criador=request.user.username)
    doc.save()
    tarefa = 'concluiu os trabalhos do item %s' %itemslug
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))


@login_required
def postarConversa(request, slug, unidade, itemslug):
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    mensagem = request.POST['mensagem']
    a = conversa.objects.create(usuario=request.user.username, mensagem=mensagem,
                                dataHora=datetime.now(), qualItem=qualItem)
    a.save()
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))


@login_required
def salvarElementoTextual(request, slug, unidade, itemslug):
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    titulo = request.POST['titulo']
    url = request.POST['link']
    subcategoria = request.POST['categoria']
    historico = '%s inseriu "%s"' % (request.user.username, titulo)
    a = elementoTextual.objects.create(vinculadoItem=qualItem, quemEnviou=request.user.username,
                                       titulo=titulo, url=url, subcategoria=subcategoria, historico=historico)
    a.save()
    tarefa = 'criou o elemento textual %s em %s' %(titulo, itemslug)
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/%s/%s/elementos_textuais/" % (slug, unidade, itemslug))


@login_required
def insereTarefa(request, slug, unidade, itemslug):
    titulo = request.POST['titulo']
    categoria = request.POST['categoria']
    slugtarefa = slugify(titulo)
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    qualItemId = qualItem.id
    salva = tarefasItem.objects.create(tarefaDesc=titulo, vinculoConhecimento=qualItem,
                                       categoria=categoria, slugTarefa=slugtarefa)
    salva.save()
    tarefa = 'inseriu a tarefa %s em %s' %(titulo, itemslug)
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    # recalcula o status do item
    # media do progresso
    qtdTarefasGeral = tarefasItem.objects.filter(vinculoConhecimento=qualItemId).count()
    # converte para float para o python nao arredondar valores decimais para zero
    qtdTarefasGeral = float(qtdTarefasGeral)
    qtdTarefasFinalizadas = tarefasItem.objects.filter(vinculoConhecimento=qualItemId, status=1).count()
    qtdTarefasFinalizadas = float(qtdTarefasFinalizadas)
    mediaTarefas = (qtdTarefasFinalizadas / qtdTarefasGeral) * 100
    # converte para int para cortar casas decimais
    mediaTarefas = int(mediaTarefas)
    x = unidadeInvestigacao.objects.select_for_update().filter(slugConhecimento=itemslug).update(status=mediaTarefas)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))


@login_required
def insereItem(request, slug, unidade):
    qualEspaco = espacoProjeto.objects.get(slugProjeto=slug)
    qualProjeto = Projeto.objects.get(espaco=qualEspaco)
    titulo = request.POST['titulo']
    slugconhecimento = slugify(titulo)
    salva = unidadeInvestigacao.objects.create(nomeDoBloco=unidade, qualProjeto=qualProjeto,
                                               conhecimentoPrevio=titulo, slugConhecimento=slugconhecimento)
    salva.save()
    tarefa = 'inseriu o item %s em %s' %(titulo, slug)
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/detalhes/" % (slug, unidade))


@login_required
def vincularTarefa(request, slug, unidade, itemslug, slugtarefa):
    vincItem = tarefasItem.objects.select_for_update().filter(slugTarefa=slugtarefa).update(
        responsavel=request.user.username)
    tarefa = 'ficou responsavel pela tarefa %s em %s' %(slugtarefa, itemslug)
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))


@login_required
def elementosTextuais(request, slug, unidade, itemslug):
    itemId = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    documentos = textoProduzido.objects.filter(vinculadoItem=itemId)
    nomeDoItem = itemId.conhecimentoPrevio
    todos = elementoTextual.objects.filter(vinculadoItem=itemId)
    context = dict(todos=todos, nomeDoItem=nomeDoItem, slug=slug, unidade=unidade,
                   itemslug=itemslug, documentos=documentos)
    c = RequestContext(request, context)
    return render_to_response('elementosTextuais.html', c)


@login_required
def redator(request, slug, unidade, itemslug):
    itemId = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    nomeDoItem = itemId.conhecimentoPrevio
    todos = elementoTextual.objects.filter(vinculadoItem=itemId)
    context = dict(itemId=itemId, nomeDoItem=nomeDoItem, todos=todos, slug=slug, itemslug=itemslug, unidade=unidade)
    c = RequestContext(request, context)
    return render_to_response('edicaotextual.html', c)


@login_required
def modoEdicao(request, slug, unidade, itemslug, id):
    # verifica se o usuario possui direito de editar
    usuarioAtual = request.user.username
    itemId = textoProduzido.objects.get(pk=id)
    if usuarioAtual != itemId.criador:
        return HttpResponseRedirect("/projeto/%s/%s/%s/elementos_textuais/visualizando/%s/" % (slug, unidade,
                                                                                               itemslug, itemId.id))
    else:
        # se possuir direito de editar
        texto = itemId.texto
        qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
        qualItemId = qualItem.id
        nomeDoItem = qualItem.conhecimentoPrevio
        todos = textoProduzido.objects.filter(vinculadoItem=qualItemId)
        todosRef = elementoTextual.objects.filter(vinculadoItem=qualItem)
        tarefasAvincular = tarefasItem.objects.filter(vinculoConhecimento=qualItemId)
        context = dict(itemId=itemId, nomeDoItem=nomeDoItem, todos=todos, todosRef=todosRef, slug=slug,
                       itemslug=itemslug, unidade=unidade, id=id, texto=texto, tarefasAvincular=tarefasAvincular)
        c = RequestContext(request, context)
        return render_to_response('editarDocumento.html', c)


@login_required
def vinculaDocItem(request, slug, unidade, itemslug, idDoc):
    tarefa = request.POST['tarefas']
    qualTarefa = tarefasItem.objects.get(tarefaDesc=tarefa)
    qualDocumento = textoProduzido.objects.get(pk=idDoc)
    a = textoProduzido.objects.select_for_update().filter(pk=idDoc).update(vinculadoTarefa=qualTarefa)
    b = tarefasItem.objects.select_for_update().filter(pk=qualTarefa.id).update(status=1)
    # salva a media no status do Item
    qualItemId = unidadeInvestigacao.objects.get(slugConhecimento=itemslug).id
    # media do progresso
    qtdTarefasGeral = tarefasItem.objects.filter(vinculoConhecimento=qualItemId).count()
    # converte para float para o python nao arredondar valores decimais para zero
    qtdTarefasGeral = float(qtdTarefasGeral)
    qtdTarefasFinalizadas = tarefasItem.objects.filter(vinculoConhecimento=qualItemId, status=1).count()
    qtdTarefasFinalizadas = float(qtdTarefasFinalizadas)
    mediaTarefas = (qtdTarefasFinalizadas / qtdTarefasGeral) * 100
    # converte para int para cortar casas decimais
    mediaTarefas = int(mediaTarefas)
    x = unidadeInvestigacao.objects.select_for_update().filter(slugConhecimento=itemslug).update(status=mediaTarefas)
    documento = qualDocumento.titulo
    tarefa = 'vinculou o texto %s a tarefa %s' %(documento, tarefa)
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/%s/%s/elementos_textuais/visualizando/%s/" % (slug, unidade,
                                                                                           itemslug, qualDocumento.id))


@login_required
def modoLeitura(request, slug, unidade, itemslug, id):
    usuarioAtual = request.user.username
    itemId = textoProduzido.objects.get(pk=id)
    texto = itemId.texto
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    nomeDoItem = qualItem.conhecimentoPrevio
    todos = elementoTextual.objects.filter(vinculadoItem=qualItem)
    context = dict(itemId=itemId, nomeDoItem=nomeDoItem, todos=todos, slug=slug,
                   itemslug=itemslug, unidade=unidade, id=id, texto=texto, usuarioAtual=usuarioAtual)
    c = RequestContext(request, context)
    return render_to_response('visualizadorTextos.html', c)


@login_required
def votarIdeia(request, slug):
    # filtra todas as questoes do espaco de projeto atual
    pk = espacoProjeto.objects.get(slugProjeto=slug).id
    questoes = ideaDeQuestao.objects.filter(espaco=pk)
    # filtra as questoes ja votadas pelo usuario atual
    jaVotadas = votosQuestao.objects.filter(usuario=request.user.username)
    # excluir as questoes que estiverem na lista jaVotadas
    listaQuestoesValidas = questoes.exclude(votosquestao__in=jaVotadas)
    context = dict(questoes=listaQuestoesValidas, idEspaco=pk)
    c = RequestContext(request, context)
    return render_to_response('votarIdeias.html', c)


@login_required
def salvarEspaco(request):
    p = request.POST
    try:
        espaco = p['nomeEspaco']
    except (KeyError):
        return HttpResponseRedirect("/espacos/")
    else:
        # slug do espaco
        slug = slugify(espaco)
        # salva o espaco de projeto
        esp = espacoProjeto.objects.create(nome=espaco, slugProjeto=slug)
        esp.save()
        idEspaco = espacoProjeto.objects.get(nome=espaco)
        # registra um novo projeto ainda sem QI
        proj = Projeto.objects.create(espaco=idEspaco)
        proj.save()
        # vicula o criador do espaco/projeto como participante
        idProjeto = Projeto.objects.get(espaco_id=idEspaco)
        link = "/projeto/%s/ideias" % slug
        part = alunosNoProjeto.objects.create(projeto=idProjeto, aluno=request.user.username, ondeparou=link)
        part.save()
        return HttpResponseRedirect("/espacos/")


@login_required
def salvarIdeia(request, pk):
    id = espacoProjeto.objects.get(id=pk)
    slug = espacoProjeto.objects.get(id=pk).slugProjeto
    p = request.POST
    ideia = p['ideia']
    usuario = request.user.username
    doc = ideaDeQuestao.objects.create(usuario=usuario, texto=ideia, espaco=id)
    doc.save()
    tarefa = 'inseriu a ideia %s' %ideia
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/ideias/" % slug)


@login_required
def lobbyProjeto(request, slug):
    espaco = espacoProjeto.objects.get(slugProjeto=slug)
    idProjeto = Projeto.objects.get(espaco=espaco).id
    totalAlunos = alunosNoProjeto.objects.filter(projeto=idProjeto).count()
    # verifica se o aluno esta neste projeto filtrando uma busca no projeto atual e seu nome de usuario
    estaParticipando = alunosNoProjeto.objects.filter(projeto=idProjeto, aluno=request.user.username).count()
    # tenta pegar o link para onde o aluno vai, se der erro, significa que o aluno nao esta neste projeto
    try:
        link = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username).ondeparou
    except:
        link = "/espacos/"
    etapa = Projeto.objects.get(espaco=idProjeto).etapa
    questaoDeInvestigacao = Projeto.objects.get(espaco=idProjeto).questaoInvestigacao
    context = dict(espaco=espaco, etapa=etapa, pk=slug, totalAlunos=totalAlunos,
                   questaoDeInvestigacao=questaoDeInvestigacao, estaParticipando=estaParticipando, espacoId=slug,
                   link=link)
    c = RequestContext(request, context)
    return render_to_response('status.html', c)


@login_required
def terminaEtapa1(request, pk):
    idProjeto = Projeto.objects.get(espaco=pk)
    slug = espacoProjeto.objects.get(id=idProjeto).slugProjeto
    atualiza = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username)
    atualiza.etapaAtual = 2
    link = '/projeto/%s/votar/' % slug
    atualiza.save()
    # verifica se todos os alunos do projeto estao em status 2
    if alunosNoProjeto.objects.filter(projeto=idProjeto).count() == alunosNoProjeto.objects.filter(projeto=idProjeto,
                                                                                                   etapaAtual=2).count():
        idProjeto.etapa = 2
        idProjeto.save()
        # atualiza o campo ondeparou de todos os alunos do projeto
        a = alunosNoProjeto.objects.filter(projeto=idProjeto).update(ondeparou=link)
        return HttpResponseRedirect("/projeto/%s/votar/" % slug)
    else:
        return HttpResponseRedirect("/espacos/")


@login_required
def terminaEtapa2(request, pk):
    idProjeto = Projeto.objects.get(espaco=pk)
    slug = espacoProjeto.objects.get(pk=pk).slugProjeto
    atualiza = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username)
    atualiza.etapaAtual = 3
    link = '/projeto/%s/conhecimento_previo/' % slug
    atualiza.save()
    # verifica se todos os alunos do projeto estao em status 3
    if alunosNoProjeto.objects.filter(projeto=idProjeto).count() == alunosNoProjeto.objects.filter(projeto=idProjeto,
                                                                                                   etapaAtual=3).count():
        idQuestao = ideaDeQuestao.objects.filter(espaco=pk)
        # Soma todos os votos de uma questao
        somaDosVotos = ideaDeQuestao.objects.filter(espaco=pk).annotate(total=Sum('votosquestao__classificacao'))
        # pegando o maior valor
        maioresValores = somaDosVotos.all().aggregate(maior=Max('total'))
        # variavel contendo o maior valor do dicionario maioresValores
        valorMax = maioresValores.get('maior')
        # pesquisar quais questoes tem o valor maximo dos votos
        questoesMaximas = somaDosVotos.filter(total=valorMax)
        # quantidade de questoes com o valor maximo dos votos
        qtdQuestoesMaximas = questoesMaximas.count()
        # caso a quantidade seja maior que 1 significa que ha empate
        if qtdQuestoesMaximas > 1:
            # atualiza o campo etapaAtual de todos os alunos do projeto, voltando a etapa anterior
            endereco = '/projeto/%s/votar/' % slug
            etapaValida = alunosNoProjeto.objects.filter(projeto=idProjeto).update(etapaAtual=2, ondeparou=endereco)
            for i in questoesMaximas:
                # apaga os registros de votacao anteriores das questoes repetidas para uma nova etapa de votacao
                o = votosQuestao.objects.filter(questao=i).delete()
            return HttpResponseRedirect('/projeto/%s/votar/' % slug)

        # se nao houver projetos duplicados, passe para a etapa 3
        else:
            # salva as questoes e seus votos para log
            for questao in somaDosVotos:
                a = resultadoVotacao.objects.create(questao=questao, totalDeVotosRecebidos=questao.total)
                a.save()
            idProjeto.etapa = 3
            # ordena as questoes por ordem descrescente de mais votadas
            listaDecrescente = somaDosVotos.order_by('-total')
            # preenche a questao de investigacao do projeto com o texto da questao mais votada
            idProjeto.questaoInvestigacao = listaDecrescente[0].texto
            idProjeto.save()
            # atualiza o campo ondeparou de todos os alunos do projeto
            a = alunosNoProjeto.objects.filter(projeto=idProjeto).update(ondeparou=link)
            return HttpResponseRedirect("/lobby/%s/" % slug)
    else:
        return HttpResponseRedirect("/espacos/")


@login_required
def terminaEtapa3(request, pk):
    idProjeto = Projeto.objects.get(espaco=pk)
    slug = espacoProjeto.objects.get(pk=pk).slugProjeto
    atualiza = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username)
    atualiza.etapaAtual = 4
    link = '/projeto/%s/unidades/' % slug
    atualiza.save()
    # verifica se todos os alunos do projeto estao em status 2
    if alunosNoProjeto.objects.filter(projeto=idProjeto).count() == alunosNoProjeto.objects.filter(projeto=idProjeto,
                                                                                                   etapaAtual=4).count():
        idProjeto.etapa = 4
        idProjeto.save()
        # pega as certezas e duvidas do projeto
        qtdCertezas = conhecimento.objects.filter(qualProjeto=idProjeto, certezaOuDuvida='C')
        qtdDuvidas = conhecimento.objects.filter(qualProjeto=idProjeto, certezaOuDuvida='D')
        # une as certezas e duvidas
        uneConhecimento = list(chain(qtdCertezas, qtdDuvidas))
        # forma uma lista com sublista de 4 elementos contendo certezas e duvidas
        f = lambda A, n=4: [A[i:i + n] for i in range(0, len(A), n)]
        separada = f(uneConhecimento)
        for i in range(len(separada)):
            for t in range(len(separada[i])):
                slugCon = slugify(separada[i][t].texto)
                a = unidadeInvestigacao.objects.create(nomeDoBloco=i, qualProjeto=idProjeto,
                                                       conhecimentoPrevio=separada[i][t].texto,
                                                       slugConhecimento=slugCon)
                a.save()
        # atualiza o campo ondeparou de todos os alunos do projeto
        a = alunosNoProjeto.objects.filter(projeto=idProjeto).update(ondeparou=link)
        return HttpResponseRedirect("/lobby/%s/" % slug)
    else:
        return HttpResponseRedirect("/espacos/")


@login_required
def fecharVoto(request):
    if request.method == 'POST':
        idQuestao = request.POST.get('id')
        classificacao = request.POST.get('value')
        response_data = {}
        qualQuestao = ideaDeQuestao.objects.get(id=idQuestao)
        salvando = votosQuestao.objects.create(usuario=request.user.username, questao=qualQuestao,
                                               classificacao=classificacao)
        salvando.save()
        response_data['result'] = 'Create post successful!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required
def conhecimentoPrevio(request, slug):
    #  pesquisa o projeto do espaco atual pk
    pk = espacoProjeto.objects.get(slugProjeto=slug).id
    idProj = Projeto.objects.get(espaco=pk)
    #  filtra as certezas e duvidas que pertencem a este projeto e este usuario
    try:
        certezas = conhecimento.objects.filter(qualProjeto=idProj, usuario=request.user.username, certezaOuDuvida='C')
    except:
        certezas = None
    try:
        duvidas = conhecimento.objects.filter(qualProjeto=idProj, usuario=request.user.username, certezaOuDuvida='D')
    except:
        duvidas = None
    context = dict(certezas=certezas, duvidas=duvidas, espacoId=pk)
    c = RequestContext(request, context)
    return render_to_response('conhecPrevio.html', c)


@login_required
def salvarConhecimento(request, pk):
    #  pesquisa o projeto do espaco atual pk
    idProj = Projeto.objects.get(espaco=pk)
    slug = espacoProjeto.objects.get(pk=pk).slugProjeto
    p = request.POST
    if p['conhecimento']:
        texto = p['conhecimento']
        # se houver uma interrogacao, trata-se de uma duvida
        if "?" in texto:
            certezaOuDuvida = 'D'
        else:
            certezaOuDuvida = 'C'
        conhec = conhecimento.objects.create(usuario=request.user.username, texto=texto, qualProjeto=idProj,
                                             certezaOuDuvida=certezaOuDuvida)
        conhec.save()
        tarefa = 'inseriu o item de conhecimento %s' %texto
        link = 'nada ainda'
        escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
        return HttpResponseRedirect("/projeto/%s/conhecimento_previo/" % slug)
    else:
        return HttpResponseRedirect("/projeto/%s/conhecimento_previo/" % slug)


@login_required
def participarProjeto(request, slug):
    # pesquisa o projeto do espaco atual pk
    espaco = espacoProjeto.objects.get(slugProjeto=slug)
    idProj = Projeto.objects.get(espaco=espaco)
    #verifica onde o projeto esta e situa o aluno
    #se o projeto esta na etapa 1
    if idProj.etapa == 1:
        aluno = alunosNoProjeto.objects.create(aluno=request.user.username, projeto=idProj,
                                           ondeparou="/projeto/%s/ideias/" % slug)
        aluno.save()
    elif idProj.etapa == 2:
        aluno = alunosNoProjeto.objects.create(aluno=request.user.username, projeto=idProj, etapaAtual=2,
                                           ondeparou="/projeto/%s/votar/" % slug)
        aluno.save()
    elif idProj.etapa == 3:
        aluno = alunosNoProjeto.objects.create(aluno=request.user.username, projeto=idProj, etapaAtual=3,
                                           ondeparou="/projeto/%s/conhecimento_previo/" % slug)
        aluno.save()
    elif idProj.etapa == 4:
        aluno = alunosNoProjeto.objects.create(aluno=request.user.username, projeto=idProj, etapaAtual=4,
                                           ondeparou="/projeto/%s/unidades/" % slug)
        aluno.save()

    tarefa = 'entrou no projeto %s na etapa %s' %(slug, idProj.etapa)
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/lobby/%s/" % slug)


@login_required
def unidadesInvestigacao(request, slug, unidade=None):
    idProjeto = espacoProjeto.objects.get(slugProjeto=slug).id
    numeroUnidades = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto).values_list('nomeDoBloco',
                                                                                           flat=True).distinct()
    lista = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade)
    context = dict(numeroUnidades=numeroUnidades, lista=lista, slug=slug, unidade=unidade)
    c = RequestContext(request, context)
    return render_to_response('unidades.html', c)


@login_required
def precisaAjuda(request, slug, unidade, itemslug):
    item = unidadeInvestigacao.objects.select_for_update().filter(slugConhecimento=itemslug).update(precisaAjuda=1)
    tarefa = 'precisou de ajuda em %s' %itemslug
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))


@login_required
def areaDeTrabalho(request, pk, id):
    context = dict()
    c = RequestContext(request, context)
    return render_to_response('area.html', c)


@login_required
#  rotina que cria um novo texto
def salvaTexto(request, slug, unidade, itemslug):
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    titulo = request.POST.get('tituloDoc')
    texto = request.POST['conteudo']
    historico = '%s criou um documento' % request.user.username
    doc = textoProduzido.objects.create(titulo=titulo, vinculadoItem=qualItem, texto=texto, historico=historico,
                                        criador=request.user.username)
    doc.save()
    tarefa = 'redigiu o texto %s' %titulo
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    docAtual = textoProduzido.objects.get(texto=texto).id
    return HttpResponseRedirect(
        "/projeto/%s/%s/%s/elementos_textuais/editando/%s" % (slug, unidade, itemslug, docAtual))


@login_required
#  rotina que edita um texto ja existente
def atualizaTexto(request, slug, unidade, itemslug, id):
    texto = request.POST['conteudo']
    historico = '%s editou um documento' % request.user.username
    response_data = {}
    doc = textoProduzido.objects.select_for_update().filter(pk=id).update(texto=texto, historico=historico)
    tarefa = 'editou um texto em %s' %itemslug
    link = 'nada ainda'
    escreveHistorico(request.user.username, tarefa, datetime.now(), slug, link)
    return HttpResponseRedirect("/projeto/%s/%s/%s/elementos_textuais/editando/%s" % (slug, unidade, itemslug, id))
