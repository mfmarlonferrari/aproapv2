from django.db import models
from datetime import datetime
from django.utils import timezone


class Usuarios(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    curso = models.CharField(max_length=100, blank=True)
    educacao = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(blank=True)
    nomeUsuario = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s %s - %s" %(self.nome, self.sobrenome, self.nomeUsuario)

class espacoProjeto(models.Model):
    nome = models.CharField(max_length=50)
    slugProjeto = models.SlugField()
    
    def __unicode__(self):
        return self.nome


class ideaDeQuestao(models.Model):
    espaco = models.ForeignKey(espacoProjeto)
    usuario = models.CharField(max_length=100)
    texto = models.CharField(max_length=200)

    def __unicode__(self):
        return self.texto


class Projeto(models.Model):
    espaco = models.ForeignKey(espacoProjeto)
    questaoInvestigacao = models.CharField(max_length=100, blank=True)
    dataPublicacao = models.DateTimeField(default=datetime.now, blank=False)
    etapa = models.IntegerField(default=1)

    def __unicode__(self):
        return "%s" % self.dataPublicacao


class votosQuestao(models.Model):
    usuario = models.CharField(max_length=100)
    questao = models.ForeignKey(ideaDeQuestao)
    classificacao = models.FloatField(default=0)

    def __unicode__(self):
        return "%s na questao %s" % (self.usuario, self.questao)


class resultadoVotacao(models.Model):
    questao = models.ForeignKey(ideaDeQuestao)
    totalDeVotosRecebidos = models.FloatField(null=True)


class alunosNoProjeto(models.Model):
    projeto = models.ForeignKey(Projeto)
    aluno = models.CharField(max_length=100)
    etapaAtual = models.IntegerField(default=1)
    ondeparou = models.CharField(max_length=200, default="/espacos/")

    def __unicode__(self):
        return "Projeto:%s -Aluno:%s-Etapa:%s" % (self.projeto_id, self.aluno, self.etapaAtual)


class conhecimento(models.Model):
    qualProjeto = models.ForeignKey(Projeto)
    usuario = models.CharField(max_length=100)
    texto = models.CharField(max_length=200)
    # por convencao, C sera certeza e D sera duvida
    certezaOuDuvida = models.CharField(max_length=1)

    def __unicode__(self):
        return self.texto


class unidadeInvestigacao(models.Model):
    nomeDoBloco = models.IntegerField()
    qualProjeto = models.ForeignKey(Projeto)
    conhecimentoPrevio = models.CharField(max_length=200)
    slugConhecimento = models.SlugField()
    investigador = models.CharField(max_length=100, blank=True)
    prazo = models.DateField(blank=True, null=True)
    prazoFinal = models.DateField(blank=True, null=True)
    precisaAjuda = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s - %s" % (self.nomeDoBloco, self.conhecimentoPrevio)


class ajudantes(models.Model):
    ajudante = models.CharField(max_length=100)
    qualItem = models.ForeignKey(unidadeInvestigacao)

    def __unicode__(self):
        return self.ajudante


class tarefasItem(models.Model):
    tarefaDesc = models.CharField(max_length=100)
    slugTarefa = models.SlugField()
    vinculoConhecimento = models.ForeignKey(unidadeInvestigacao)
    responsavel = models.CharField(max_length=100, blank=True)
    status = models.IntegerField(default=0)
    categoria = models.CharField(max_length=30)

    def __unicode__(self):
        return self.tarefaDesc


class elementoTextual(models.Model):
    vinculadoItem = models.ForeignKey(unidadeInvestigacao)
    quemEnviou = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    subcategoria = models.CharField(max_length=30)
    historico = models.CharField(max_length=300)
    data = models.DateTimeField(default=timezone.now())


class textoProduzido(models.Model):
    vinculadoTarefa = models.ForeignKey(tarefasItem, blank=True, null=True)
    vinculadoItem = models.ForeignKey(unidadeInvestigacao)
    titulo = models.CharField(max_length=300)
    criador = models.CharField(max_length=100)
    texto = models.TextField()
    historico = models.CharField(max_length=300)
    data = models.DateTimeField(default=timezone.now())

class conversa(models.Model):
    usuario = models.CharField(max_length=100)
    mensagem = models.CharField(max_length=200)
    dataHora = models.DateTimeField()
    qualItem = models.ForeignKey(unidadeInvestigacao)


class mensagemAssistente(models.Model):
    usuario = models.CharField(max_length=100)
    mensagem = models.CharField(max_length=200)
    data = models.DateField(default=timezone.now())
    qualItem = models.ForeignKey(unidadeInvestigacao)


class mapaConceitual(models.Model):
    pertence = models.CharField(max_length=200)
    usuario = models.CharField(max_length=100)
    conceitosRelacoes = models.TextField()


class postagem(models.Model):
    usuario = models.CharField(max_length=100)
    pertence = models.ForeignKey(espacoProjeto)
    texto = models.CharField(max_length=300)


class respostas(models.Model):
    usuario = models.CharField(max_length=100)
    forum = models.ForeignKey(postagem)
    resposta = models.CharField(max_length=300)


class mensagemDeContato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    mensagem = models.TextField()


class historicoAluno(models.Model):
    aluno = models.CharField(max_length=100)
    tarefa = models.CharField(max_length=200)
    data = models.DateTimeField()
    qualEspaco = models.ForeignKey(espacoProjeto)
    link = models.CharField(max_length=200)
    tipoConteudo = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s %s" %(self.aluno, self.tarefa)


class atividadesCampo(models.Model):
    aluno = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200)
    resumo = models.CharField(max_length=200)
    relato = models.CharField(max_length=200)
    data = models.DateTimeField()
    qualItem = models.ForeignKey(unidadeInvestigacao)

    def __unicode__(self):
        return "%s %s" %(self.aluno, self.titulo)
