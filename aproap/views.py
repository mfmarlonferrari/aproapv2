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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

register = template.Library()

def index(request):
    return render_to_response('index.html', {})

def cadastrar(request):
    return render_to_response('cadastrar.html', {})

def mapa(request):
    return render_to_response('mapa.html', {})

def showcronograma(request):
    #filtra as entradas cujo investigador seja o usuario atual e os prazos nao sejam nulos
    entries = unidadeInvestigacao.objects.filter(investigador=request.user.username, prazo__isnull=False, prazoFinal__isnull=False)
    print entries
    json_list = []
    for entry in entries:
        title = entry.conhecimentoPrevio
        print title
        start = entry.prazo.strftime("%Y-%m-%d")
        print start
        end = entry.prazoFinal.strftime("%Y-%m-%d")
        print end
        json_entry = {'start':start, 'end': end, 'title': title}
        json_list.append(json_entry)
    return HttpResponse(json.dumps(json_list), content_type='application/json')

def salvaCronograma(request):
    if request.method == 'POST':
        eventsJson = request.POST.get('eventsJson')
        jsonDec = json.loads(eventsJson)
        titulo,dataBruta, dataBrutaFinal = [], [], []
        #percorre os objetos do jsonDec
        for i in range(len(jsonDec)):
            titulo.append(jsonDec[i]['title'])
            #pega a data no formato com hora
            dataBruta.append(jsonDec[i]['start'])
            #se a data final for None, entao a data inicial e final devem ser no mesmo dia
            testeDtFinal = jsonDec[i]['end']
            if testeDtFinal is None:
                #recebe a mesma data de inicio
                dataBrutaFinal.append(jsonDec[i]['start'])
            else:
                #senao recebe a data final que nao esta vazia. Isto ocorre porque ao arrastar o item para
                #o calendario, o javascript nao preenche a data final como sendo a do mesmo dia em caso de tarefas
                #de apenas um dia.
                dataBrutaFinal.append(jsonDec[i]['end'])

        #rotina para formatar a data para salvamento
        dataApenas, dataApenasFinal = [],[]
        for i in range(len(dataBruta)):
            #divide a data em dois itens data e hora
            divide = dataBruta[i].split('T')
            divideFinal = dataBrutaFinal[i].split('T')
            #pega apenas o item da data
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

def cronograma(request, usuario, slug, unidade):
    itensSemPrazo = unidadeInvestigacao.objects.filter(
        investigador=request.user.username, prazo__isnull=True, prazoFinal__isnull=True)
    context = dict(itensSemPrazo=itensSemPrazo, slug=slug, unidade=unidade)
    c = RequestContext(request, context)
    return render_to_response('cronograma.html', c)

def vincularItem(request, id, unidade, pk):
    slug = espacoProjeto.objects.get(pk=id).slugProjeto
    item = unidadeInvestigacao.objects.select_for_update().filter(id=pk).update(investigador=request.user.username)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/detalhes/" % (slug, unidade))

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
    ideias = ideaDeQuestao.objects.filter(usuario=dono,espaco=projetoId)
    context = dict(ideias=ideias, espacoId=espacoId)
    c = RequestContext(request, context)
    return render_to_response('inserirIdeia.html', c)

def detalhesUnidade(request, slug, unidade):
    pk= espacoProjeto.objects.get(slugProjeto=slug).id
    idProjeto = Projeto.objects.get(espaco=pk)
    #itens ja completados
    qtdCompletados = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto,
                                               nomeDoBloco=unidade, status=100).count()
    #quantidade de itens que precisam de ajuda, excluindo os que ja foram completados
    ajuda = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto,
                                               nomeDoBloco=unidade, precisaAjuda='1').exclude(status=100)
    qtdAjuda = ajuda.count()
    #filtra todos os conhecimentos sem investigador vinculado
    pendentes = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade, investigador='')
    qtdPendentes = pendentes.count()
    #filtra todos os conhecimentos cujo investigador exista
    todos = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade).exclude(investigador='')
    #verifica se o usuario possui itens a investigar sem cronograma
    semCronograma = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade,
                                                       investigador=request.user.username, prazo__isnull=True,
                                                       prazoFinal__isnull=True).count()
    #filtra todos os itens do usuario atual
    desteUsuario = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade,
                                                      investigador=request.user.username)
    #calcula o andamento da unidade pela media de andamento dos itens
    somaUnidade = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade).aggregate(total=Sum('status'))
    somaUnidadeValor = somaUnidade['total']
    qtdItens = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade).count()
    mediaDaUnidade = somaUnidadeValor/qtdItens
    context = dict(pendentes=pendentes, espacoId=pk, unidade=unidade,
                   qtdPendentes=qtdPendentes, todos=todos, semCronograma=semCronograma, desteUsuario=desteUsuario,
                   mediaDaUnidade=mediaDaUnidade, slug=slug, qtdAjuda=qtdAjuda,
                   ajuda=ajuda, qtdCompletados=qtdCompletados)
    c = RequestContext(request, context)
    return render_to_response('detalhesUnidade.html', c)

def detalhesItem(request, slug, unidade, itemslug):
    item = unidadeInvestigacao.objects.get(slugConhecimento=itemslug).id
    vinculoItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    qualItem = unidadeInvestigacao.objects.get(pk=item).conhecimentoPrevio
    conversas = conversa.objects.filter(qualItem=vinculoItem)
    #quantos documentos associados ao item
    producoes = textoProduzido.objects.filter(vinculadoItem=vinculoItem).count()
    #verifica se o item possui cronograma
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
    #media do progresso
    mediaTarefas = vinculoItem.status
    qtdTarefasFinalizadas = tarefasItem.objects.filter(vinculoConhecimento=qualItemId, status=1).count()
    context = dict(tarefasPendentes=tarefasPendentes, tarefasAndamento=tarefasAndamento,
                   qualItem=qualItemId, item=item, qtdTarefasPendentes=qtdTarefasPendentes,
                   qtdajudantes=qtdajudantes, ajudantes=ajudante, slug=slug, unidade=unidade, itemslug=itemslug,
                   semCronograma=semCronograma, producoes=producoes, vinculoItem=vinculoItem, conversas=conversas,
                   mediaTarefas=mediaTarefas, qtdTarefasFinalizadas=qtdTarefasFinalizadas)
    c = RequestContext(request, context)
    return render_to_response('detalheItem.html', c)

def concluirItem(request, slug, unidade, itemslug):
    qualItem = unidadeInvestigacao.objects.select_for_update().filter(slugConhecimento=itemslug).update(status=100)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))

def postarConversa(request, slug, unidade, itemslug):
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    mensagem = request.POST['mensagem']
    a = conversa.objects.create(usuario=request.user.username, mensagem=mensagem,
                                dataHora=datetime.now(), qualItem=qualItem)
    a.save()
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))

def salvarElementoTextual(request, slug, unidade, itemslug):
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    titulo = request.POST['titulo']
    url = request.POST['link']
    subcategoria = request.POST['categoria']
    historico = '%s inseriu "%s"' % (request.user.username, titulo)
    a = elementoTextual.objects.create(vinculadoItem=qualItem, quemEnviou=request.user.username,
                                       titulo=titulo, url=url, subcategoria=subcategoria, historico=historico)
    a.save()
    return HttpResponseRedirect("/projeto/%s/%s/%s/elementos_textuais/" % (slug, unidade, itemslug))

def concluirDocumento(request, slug, unidade, itemslug):
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)


def insereTarefa(request, slug, unidade, itemslug):
    titulo = request.POST['titulo']
    categoria = request.POST['categoria']
    slugtarefa = slugify(titulo)
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    qualItemId = qualItem.id
    salva = tarefasItem.objects.create(tarefaDesc=titulo, vinculoConhecimento=qualItem,
                                       categoria=categoria, slugTarefa=slugtarefa)
    salva.save()
    #recalcula o status do item
    #media do progresso
    qtdTarefasGeral = tarefasItem.objects.filter(vinculoConhecimento=qualItemId).count()
    #converte para float para o python nao arredondar valores decimais para zero
    qtdTarefasGeral = float(qtdTarefasGeral)
    qtdTarefasFinalizadas = tarefasItem.objects.filter(vinculoConhecimento=qualItemId, status=1).count()
    qtdTarefasFinalizadas = float(qtdTarefasFinalizadas)
    mediaTarefas = (qtdTarefasFinalizadas/qtdTarefasGeral)*100
    #converte para int para cortar casas decimais
    mediaTarefas = int(mediaTarefas)
    x = unidadeInvestigacao.objects.select_for_update().filter(slugConhecimento=itemslug).update(status=mediaTarefas)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))

def insereItem(request, slug, unidade):
    qualEspaco = espacoProjeto.objects.get(slugProjeto = slug)
    qualProjeto = Projeto.objects.get(espaco=qualEspaco)
    titulo = request.POST['titulo']
    slugconhecimento = slugify(titulo)
    salva = unidadeInvestigacao.objects.create(nomeDoBloco=unidade, qualProjeto=qualProjeto,
                                               conhecimentoPrevio=titulo, slugConhecimento=slugconhecimento)
    salva.save()
    return HttpResponseRedirect("/projeto/%s/unidade/%s/detalhes/" % (slug, unidade))

def vincularTarefa(request, slug, unidade, itemslug, slugtarefa):
    vincItem = tarefasItem.objects.select_for_update().filter(slugTarefa=slugtarefa).update(responsavel=request.user.username)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))

def elementosTextuais(request, slug, unidade, itemslug):
    itemId = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    documentos = textoProduzido.objects.filter(vinculadoItem=itemId)
    nomeDoItem = itemId.conhecimentoPrevio
    todos = elementoTextual.objects.filter(vinculadoItem=itemId)
    context = dict(todos=todos, nomeDoItem=nomeDoItem, slug=slug, unidade=unidade,
                   itemslug=itemslug, documentos=documentos)
    c = RequestContext(request, context)
    return render_to_response('elementosTextuais.html', c)

def redator(request, slug, unidade, itemslug):
    itemId = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    nomeDoItem = itemId.conhecimentoPrevio
    todos = elementoTextual.objects.filter(vinculadoItem=itemId)
    context = dict(itemId=itemId, nomeDoItem=nomeDoItem, todos=todos, slug=slug, itemslug=itemslug, unidade=unidade)
    c = RequestContext(request, context)
    return render_to_response('edicaotextual.html', c)

def modoEdicao(request, slug, unidade, itemslug, id):
    #verifica se o usuario possui direito de editar
    usuarioAtual = request.user.username
    itemId = textoProduzido.objects.get(pk=id)
    if usuarioAtual != itemId.criador:
        return HttpResponseRedirect("/projeto/%s/%s/%s/elementos_textuais/visualizando/%s/" % (slug, unidade,
                                                                                               itemslug, itemId.id))
    else:
        #se possuir direito de editar
        texto = itemId.texto
        qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
        qualItemId = qualItem.id
        nomeDoItem = qualItem.conhecimentoPrevio
        todos = textoProduzido.objects.filter(vinculadoItem=qualItemId)
        todosRef = elementoTextual.objects.filter(vinculadoItem=qualItem)
        tarefasAvincular=tarefasItem.objects.filter(vinculoConhecimento=qualItemId)
        context = dict(itemId=itemId, nomeDoItem=nomeDoItem, todos=todos, todosRef=todosRef, slug=slug,
                       itemslug=itemslug, unidade=unidade, id=id, texto=texto, tarefasAvincular=tarefasAvincular)
        c = RequestContext(request, context)
        return render_to_response('editarDocumento.html', c)

def vinculaDocItem(request, slug, unidade, itemslug, idDoc):
    tarefa = request.POST['tarefas']
    qualTarefa = tarefasItem.objects.get(tarefaDesc=tarefa)
    qualDocumento = textoProduzido.objects.get(pk=idDoc)
    a = textoProduzido.objects.select_for_update().filter(pk=idDoc).update(vinculadoTarefa=qualTarefa)
    b = tarefasItem.objects.select_for_update().filter(pk=qualTarefa.id).update(status=1)
    #salva a media no status do Item
    qualItemId = unidadeInvestigacao.objects.get(slugConhecimento=itemslug).id
    #media do progresso
    qtdTarefasGeral = tarefasItem.objects.filter(vinculoConhecimento=qualItemId).count()
    #converte para float para o python nao arredondar valores decimais para zero
    qtdTarefasGeral = float(qtdTarefasGeral)
    qtdTarefasFinalizadas = tarefasItem.objects.filter(vinculoConhecimento=qualItemId, status=1).count()
    qtdTarefasFinalizadas = float(qtdTarefasFinalizadas)
    mediaTarefas = (qtdTarefasFinalizadas/qtdTarefasGeral)*100
    #converte para int para cortar casas decimais
    mediaTarefas = int(mediaTarefas)
    x = unidadeInvestigacao.objects.select_for_update().filter(slugConhecimento=itemslug).update(status=mediaTarefas)
    return HttpResponseRedirect("/projeto/%s/%s/%s/elementos_textuais/visualizando/%s/" % (slug, unidade,
                                                                                               itemslug, qualDocumento.id))

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
def votarIdeia(request,slug):
    #filtra todas as questoes do espaco de projeto atual
    pk=espacoProjeto.objects.get(slugProjeto=slug).id
    questoes = ideaDeQuestao.objects.filter(espaco=pk)
    #filtra as questoes ja votadas pelo usuario atual
    jaVotadas = votosQuestao.objects.filter(usuario=request.user.username)
    #excluir as questoes que estiverem na lista jaVotadas
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
        #slug do espaco
        slug = slugify(espaco)
        #salva o espaco de projeto
        esp = espacoProjeto.objects.create(nome=espaco, slugProjeto=slug)
        esp.save()
        idEspaco = espacoProjeto.objects.get(nome=espaco)
        #registra um novo projeto ainda sem QI
        proj = Projeto.objects.create(espaco=idEspaco)
        proj.save()
        #vicula o criador do espaco/projeto como participante
        idProjeto = Projeto.objects.get(espaco_id=idEspaco)
        link = "/projeto/%s/ideias" % slug
        part = alunosNoProjeto.objects.create(projeto=idProjeto, aluno=request.user.username, ondeparou=link)
        part.save()
        return HttpResponseRedirect("/espacos/")

@login_required
def salvarIdeia(request,pk):
    id = espacoProjeto.objects.get(id=pk)
    slug = espacoProjeto.objects.get(id=pk).slugProjeto
    p = request.POST
    ideia = p['ideia']
    usuario = request.user.username
    doc = ideaDeQuestao.objects.create(usuario=usuario, texto=ideia, espaco=id)
    doc.save()
    return HttpResponseRedirect("/projeto/%s/ideias/" % slug)

def lobbyProjeto(request,slug):
    espaco = espacoProjeto.objects.get(slugProjeto=slug)
    idProjeto = Projeto.objects.get(espaco=espaco).id
    totalAlunos = alunosNoProjeto.objects.filter(projeto=idProjeto).count()
    #verifica se o aluno esta neste projeto filtrando uma busca no projeto atual e seu nome de usuario
    estaParticipando = alunosNoProjeto.objects.filter(projeto=idProjeto, aluno=request.user.username).count()
    #tenta pegar o link para onde o aluno vai, se der erro, significa que o aluno nao esta neste projeto
    try:
        link = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username).ondeparou
    except:
        link = "/espacos/"
    etapa = Projeto.objects.get(espaco=idProjeto).etapa
    questaoDeInvestigacao = Projeto.objects.get(espaco=idProjeto).questaoInvestigacao
    context = dict(espaco=espaco, etapa=etapa, pk=slug, totalAlunos=totalAlunos,
                   questaoDeInvestigacao=questaoDeInvestigacao, estaParticipando=estaParticipando, espacoId=slug, link=link)
    c = RequestContext(request, context)
    return render_to_response('status.html', c)

@login_required
def terminaEtapa1(request, pk):
    idProjeto = Projeto.objects.get(espaco=pk)
    slug=espacoProjeto.objects.get(id=idProjeto).slugProjeto
    atualiza = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username)
    atualiza.etapaAtual = 2
    link = '/projeto/%s/votar/' % slug
    atualiza.save()
    #verifica se todos os alunos do projeto estao em status 2
    if alunosNoProjeto.objects.filter(projeto=idProjeto).count() == alunosNoProjeto.objects.filter(projeto=idProjeto, etapaAtual=2).count():
        idProjeto.etapa = 2
        idProjeto.save()
        #atualiza o campo ondeparou de todos os alunos do projeto
        a = alunosNoProjeto.objects.filter(projeto=idProjeto).update(ondeparou=link)
        return HttpResponseRedirect("/projeto/%s/votar/" % slug)
    else:
        return HttpResponseRedirect("/espacos/")

def terminaEtapa2(request, pk):
    idProjeto = Projeto.objects.get(espaco=pk)
    slug=espacoProjeto.objects.get(pk=pk).slugProjeto
    atualiza = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username)
    atualiza.etapaAtual = 3
    link = '/projeto/%s/conhecimento_previo/' % slug
    atualiza.save()
    #verifica se todos os alunos do projeto estao em status 3
    if alunosNoProjeto.objects.filter(projeto=idProjeto).count() == alunosNoProjeto.objects.filter(projeto=idProjeto, etapaAtual=3).count():
        idQuestao = ideaDeQuestao.objects.filter(espaco=pk)
        #Soma todos os votos de uma questao
        somaDosVotos = ideaDeQuestao.objects.filter(espaco=pk).annotate(total=Sum('votosquestao__classificacao'))
        #pegando o maior valor
        maioresValores = somaDosVotos.all().aggregate(maior=Max('total'))
        #variavel contendo o maior valor do dicionario maioresValores
        valorMax = maioresValores.get('maior')
        #pesquisar quais questoes tem o valor maximo dos votos
        questoesMaximas = somaDosVotos.filter(total=valorMax)
        #quantidade de questoes com o valor maximo dos votos
        qtdQuestoesMaximas = questoesMaximas.count()
        #caso a quantidade seja maior que 1 significa que ha empate
        if qtdQuestoesMaximas > 1:
            #atualiza o campo etapaAtual de todos os alunos do projeto, voltando a etapa anterior
            endereco = '/projeto/%s/votar/' % slug
            etapaValida = alunosNoProjeto.objects.filter(projeto=idProjeto).update(etapaAtual=2, ondeparou=endereco)
            for i in questoesMaximas:
                #apaga os registros de votacao anteriores das questoes repetidas para uma nova etapa de votacao
                o = votosQuestao.objects.filter(questao=i).delete()
            return HttpResponseRedirect('/projeto/%s/votar/' % slug)

        #se nao houver projetos duplicados, passe para a etapa 3
        else:
            #salva as questoes e seus votos para log
            for questao in somaDosVotos:
                a = resultadoVotacao.objects.create(questao=questao, totalDeVotosRecebidos=questao.total)
                a.save()
            idProjeto.etapa = 3
            #ordena as questoes por ordem descrescente de mais votadas
            listaDecrescente = somaDosVotos.order_by('-total')
            #preenche a questao de investigacao do projeto com o texto da questao mais votada
            idProjeto.questaoInvestigacao = listaDecrescente[0].texto
            idProjeto.save()
            #atualiza o campo ondeparou de todos os alunos do projeto
            a = alunosNoProjeto.objects.filter(projeto=idProjeto).update(ondeparou=link)
            return HttpResponseRedirect("/lobby/%s/" % slug)
    else:
        return HttpResponseRedirect("/espacos/")

def terminaEtapa3(request, pk):
    idProjeto = Projeto.objects.get(espaco=pk)
    slug=espacoProjeto.objects.get(pk=pk).slugProjeto
    atualiza = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username)
    atualiza.etapaAtual = 4
    link = '/projeto/%s/unidades/' % slug
    atualiza.save()
    #verifica se todos os alunos do projeto estao em status 2
    if alunosNoProjeto.objects.filter(projeto=idProjeto).count() == alunosNoProjeto.objects.filter(projeto=idProjeto, etapaAtual=4).count():
        idProjeto.etapa = 4
        idProjeto.save()
        #pega as certezas e duvidas do projeto
        qtdCertezas = conhecimento.objects.filter(qualProjeto=idProjeto, certezaOuDuvida=True)
        qtdDuvidas = conhecimento.objects.filter(qualProjeto=idProjeto, certezaOuDuvida=False)
        #une as certezas e duvidas
        uneConhecimento = list(chain(qtdCertezas, qtdDuvidas))
        #forma uma lista com sublista de 4 elementos contendo certezas e duvidas
        f = lambda A, n=4: [A[i:i+n] for i in range(0, len(A), n)]
        separada = f(uneConhecimento)
        for i in range(len(separada)):
            for t in range(len(separada[i])):
                slugCon=slugify(separada[i][t].texto)
                a = unidadeInvestigacao.objects.create(nomeDoBloco=i, qualProjeto=idProjeto,
                                                       conhecimentoPrevio=separada[i][t].texto, slugConhecimento=slugCon)
                a.save()
        #atualiza o campo ondeparou de todos os alunos do projeto
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
        salvando = votosQuestao.objects.create(usuario=request.user.username, questao=qualQuestao, classificacao=classificacao)
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

def conhecimentoPrevio(request, slug):
     #pesquisa o projeto do espaco atual pk
    pk= espacoProjeto.objects.get(slugProjeto=slug).id
    idProj = Projeto.objects.get(espaco=pk)
    #filtra as certezas e duvidas que pertencem a este projeto e este usuario
    try:
        certezas = conhecimento.objects.filter(qualProjeto=idProj, usuario=request.user.username, certezaOuDuvida=True)
    except:
        certezas = None
    try:
        duvidas = conhecimento.objects.filter(qualProjeto=idProj, usuario=request.user.username, certezaOuDuvida=False)
    except:
        duvidas = None
    context = dict(certezas=certezas, duvidas=duvidas, espacoId=pk)
    c = RequestContext(request, context)
    return render_to_response('conhecPrevio.html', c)

def salvarConhecimento(request, pk):
    #pesquisa o projeto do espaco atual pk
    idProj = Projeto.objects.get(espaco=pk)
    slug=espacoProjeto.objects.get(pk=pk).slugProjeto
    p = request.POST
    if p['conhecimento']:
        texto = p['conhecimento']
        #se houver uma interrogacao, trata-se de uma duvida
        if "?" in texto:
            certezaOuDuvida = False
        else:
            certezaOuDuvida = True
        conhec = conhecimento.objects.create(usuario=request.user.username, texto=texto, qualProjeto=idProj, certezaOuDuvida=certezaOuDuvida)
        conhec.save()
        return HttpResponseRedirect("/projeto/%s/conhecimento_previo/" % slug)
    else:
        return HttpResponseRedirect("/projeto/%s/conhecimento_previo/" % slug)

def participarProjeto(request, slug):
     #pesquisa o projeto do espaco atual pk
    espaco = espacoProjeto.objects.get(slugProjeto=slug)
    idProj = Projeto.objects.get(espaco=espaco)
    aluno = alunosNoProjeto.objects.create(aluno=request.user.username, projeto=idProj, ondeparou="/projeto/%s/ideias/" % slug)
    aluno.save()
    return HttpResponseRedirect("/lobby/%s/" % slug)

def unidadesInvestigacao(request,slug, unidade=None):
    idProjeto = espacoProjeto.objects.get(slugProjeto=slug).id
    numeroUnidades = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto).values_list('nomeDoBloco', flat=True).distinct()
    lista = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco = unidade)
    context = dict(numeroUnidades=numeroUnidades, lista=lista, slug=slug, unidade=unidade)
    c = RequestContext(request, context)
    return render_to_response('unidades.html', c)

def precisaAjuda(request, slug, unidade, itemslug):
    item = unidadeInvestigacao.objects.select_for_update().filter(slugConhecimento=itemslug).update(precisaAjuda=1)
    return HttpResponseRedirect("/projeto/%s/unidade/%s/item/%s/" % (slug, unidade, itemslug))

def areaDeTrabalho(request, pk, id):
    context = dict()
    c = RequestContext(request, context)
    return render_to_response('area.html', c)

#rotina que cria um novo texto
def salvaTexto(request, slug, unidade, itemslug):
    qualItem = unidadeInvestigacao.objects.get(slugConhecimento=itemslug)
    titulo = request.POST.get('tituloDoc')
    texto = request.POST['conteudo']
    historico = '%s criou um documento' % request.user.username
    response_data = {}
    print texto
    print historico
    doc = textoProduzido.objects.create(titulo=titulo, vinculadoItem=qualItem, texto=texto, historico=historico,
                                        criador=request.user.username)
    doc.save()
    docAtual = textoProduzido.objects.get(texto=texto).id
    return HttpResponseRedirect("/projeto/%s/%s/%s/elementos_textuais/editando/%s" % (slug, unidade, itemslug, docAtual))

#rotina que edita um texto ja existente
def atualizaTexto(request, slug, unidade, itemslug, id):
    texto = request.POST['conteudo']
    historico = '%s editou um documento' % request.user.username
    response_data = {}
    doc = textoProduzido.objects.select_for_update().filter(pk=id).update(texto=texto, historico=historico)
    return HttpResponseRedirect("/projeto/%s/%s/%s/elementos_textuais/editando/%s" % (slug, unidade, itemslug, id))