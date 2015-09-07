from django.shortcuts import render_to_response
from aproap.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max
from django import template
from itertools import chain
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

register = template.Library()

def index(request):
    return render_to_response('intro.html', {})

def cadastrar(request):
    return render_to_response('cadastrar.html', {})

def showcronograma(request):
    from django.utils.timezone import utc
    from django.core.serializers.json import DjangoJSONEncoder

    if request.is_ajax():
        print 'Its ajax from fullCalendar()'
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

def cronograma(request):
    itensSemPrazo = unidadeInvestigacao.objects.filter(
        investigador=request.user.username, prazo__isnull=True, prazoFinal__isnull=True)
    context = dict(itensSemPrazo=itensSemPrazo)
    c = RequestContext(request, context)
    return render_to_response('cronograma.html', c)

def listagem(request):
    espacos = espacoProjeto.objects.all()
    context = dict(espacos=espacos)
    c = RequestContext(request, context)
    return render_to_response('lista.html', c)

@login_required
def inserirIdeia(request,pk):
    espacoId = pk
    dono = request.user
    ideias = ideaDeQuestao.objects.filter(usuario=dono,espaco=pk)
    context = dict(ideias=ideias, espacoId=espacoId)
    c = RequestContext(request, context)
    return render_to_response('inserirIdeia.html', c)

def detalhesUnidade(request,pk, unidade):
    idProjeto = Projeto.objects.get(espaco=pk)
    #filtra todos os conhecimentos sem investigador vinculado
    pendentes = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco=unidade, investigador='')
    context = dict(pendentes=pendentes)
    c = RequestContext(request, context)
    return render_to_response('detalhesUnidade.html', c)

@login_required
def votarIdeia(request,pk):
    #filtra todas as questoes do espaco de projeto atual
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
        #salva o espaco de projeto
        esp = espacoProjeto.objects.create(nome=espaco)
        esp.save()
        idEspaco = espacoProjeto.objects.get(nome=espaco)
        #registra um novo projeto ainda sem QI
        proj = Projeto.objects.create(espaco=idEspaco)
        proj.save()
        #vicula o criador do espaco/projeto como participante
        idProjeto = Projeto.objects.get(espaco_id=idEspaco)
        link = "/ideias/%s" %idEspaco.id
        part = alunosNoProjeto.objects.create(projeto=idProjeto, aluno=request.user.username, ondeparou=link)
        part.save()
        return HttpResponseRedirect("/espacos/")

@login_required
def salvarIdeia(request,pk):
    id = espacoProjeto.objects.get(id=pk)
    p = request.POST
    ideia = p['ideia']
    usuario = request.user.username
    doc = ideaDeQuestao.objects.create(usuario=usuario, texto=ideia, espaco=id)
    doc.save()
    return HttpResponseRedirect("/ideias/%s/" %pk)

def lobbyProjeto(request,pk):
    espaco = espacoProjeto.objects.get(pk=pk).nome
    idProjeto = Projeto.objects.get(espaco=pk)
    totalAlunos = alunosNoProjeto.objects.filter(projeto=idProjeto).count()
    #verifica se o aluno esta neste projeto filtrando uma busca no projeto atual e seu nome de usuario
    estaParticipando = alunosNoProjeto.objects.filter(projeto=idProjeto, aluno=request.user.username).count()
    #tenta pegar o link para onde o aluno vai, se der erro, significa que o aluno nao esta neste projeto
    try:
        link = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username).ondeparou
    except:
        link = "/espacos/"
    etapa = Projeto.objects.get(espaco=pk).etapa
    questaoDeInvestigacao = Projeto.objects.get(espaco=pk).questaoInvestigacao
    context = dict(espaco=espaco, etapa=etapa, pk=pk, totalAlunos=totalAlunos,
                   questaoDeInvestigacao=questaoDeInvestigacao, estaParticipando=estaParticipando, espacoId=pk, link=link)
    c = RequestContext(request, context)
    return render_to_response('status.html', c)

@login_required
def terminaEtapa1(request, pk):
    idProjeto = Projeto.objects.get(espaco=pk)
    atualiza = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username)
    atualiza.etapaAtual = 2
    link = '/votar/%s' %pk
    atualiza.save()
    #verifica se todos os alunos do projeto estao em status 2
    if alunosNoProjeto.objects.filter(projeto=idProjeto).count() == alunosNoProjeto.objects.filter(projeto=idProjeto, etapaAtual=2).count():
        idProjeto.etapa = 2
        idProjeto.save()
        #atualiza o campo ondeparou de todos os alunos do projeto
        a = alunosNoProjeto.objects.filter(projeto=idProjeto).update(ondeparou=link)
        return HttpResponseRedirect("/votar/%s" %pk)
    else:
        return HttpResponseRedirect("/espacos/")

def terminaEtapa2(request, pk):
    idProjeto = Projeto.objects.get(espaco=pk)
    atualiza = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username)
    atualiza.etapaAtual = 3
    link = '/conhecimentoPrevio/%s' %pk
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
            endereco = '/votar/%s' %pk
            etapaValida = alunosNoProjeto.objects.filter(projeto=idProjeto).update(etapaAtual=2, ondeparou=endereco)
            for i in questoesMaximas:
                #apaga os registros de votacao anteriores das questoes repetidas para uma nova etapa de votacao
                o = votosQuestao.objects.filter(questao=i).delete()
            return HttpResponseRedirect("/votar/%s" %pk)

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
            return HttpResponseRedirect("/lobby/%s" %pk)
    else:
        return HttpResponseRedirect("/espacos/")

def terminaEtapa3(request, pk):
    idProjeto = Projeto.objects.get(espaco=pk)
    atualiza = alunosNoProjeto.objects.get(projeto=idProjeto, aluno=request.user.username)
    atualiza.etapaAtual = 4
    link = '/unidades/%s' %pk
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
                a = unidadeInvestigacao.objects.create(nomeDoBloco=i, qualProjeto=idProjeto, conhecimentoPrevio=separada[i][t].texto)
                a.save()
        #atualiza o campo ondeparou de todos os alunos do projeto
        a = alunosNoProjeto.objects.filter(projeto=idProjeto).update(ondeparou=link)
        return HttpResponseRedirect("/lobby/%s" %pk)
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

def conhecimentoPrevio(request, pk):
     #pesquisa o projeto do espaco atual pk
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
        return HttpResponseRedirect("/conhecimentoPrevio/%s/" %pk)
    else:
        return HttpResponseRedirect("/conhecimentoPrevio/%s/" %pk)

def participarProjeto(request, pk):
     #pesquisa o projeto do espaco atual pk
    idProj = Projeto.objects.get(espaco=pk)
    aluno = alunosNoProjeto.objects.create(aluno=request.user.username, projeto=idProj, ondeparou="/ideias/%s" %pk)
    aluno.save()
    return HttpResponseRedirect("/lobby/%s/" %pk)

def unidadesInvestigacao(request,pk, unidade=None):
    idProjeto = Projeto.objects.get(espaco=pk)
    numeroUnidades = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto).values_list('nomeDoBloco', flat=True).distinct()
    lista = unidadeInvestigacao.objects.filter(qualProjeto=idProjeto, nomeDoBloco = unidade)
    context = dict(numeroUnidades=numeroUnidades, lista=lista, pk=pk, unidade=unidade)
    c = RequestContext(request, context)
    return render_to_response('unidades.html', c)

def areaDeTrabalho(request, pk, id):
    context = dict()
    c = RequestContext(request, context)
    return render_to_response('area.html', c)