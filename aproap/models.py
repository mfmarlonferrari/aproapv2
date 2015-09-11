from django.db import models
from datetime import datetime

class Usuarios(models.Model):
    nomeCompleto = models.CharField(max_length = 100)

class espacoProjeto(models.Model):
    nome = models.CharField(max_length=50)
    slugProjeto = models.SlugField()
    def __unicode__(self):
        return self.nome

class ideaDeQuestao(models.Model):
    espaco = models.ForeignKey(espacoProjeto)
    usuario = models.CharField(max_length = 100)
    texto = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.texto

class Projeto(models.Model):
    espaco = models.ForeignKey(espacoProjeto)
    questaoInvestigacao = models.CharField(max_length = 100, blank=True)
    dataPublicacao = models.DateTimeField(default=datetime.now, blank=False)
    etapa = models.IntegerField(default=1)

    def __unicode__(self):
        return "%s" % self.dataPublicacao

class votosQuestao(models.Model):
    usuario = models.CharField(max_length=100)
    questao = models.ForeignKey(ideaDeQuestao)
    classificacao = models.FloatField(default=0)

    def __unicode__(self):
        return "%s na questao %s" %(self.usuario, self.questao)

class resultadoVotacao(models.Model):
    questao = models.ForeignKey(ideaDeQuestao)
    totalDeVotosRecebidos = models.FloatField(null=True)

class alunosNoProjeto(models.Model):
    projeto = models.ForeignKey(Projeto)
    aluno = models.CharField(max_length = 100)
    etapaAtual = models.IntegerField(default=1)
    ondeparou = models.CharField(max_length=200, default="/espacos/")

    def __unicode__(self):
        return "Projeto:%s -Aluno:%s-Etapa:%s" %(self.projeto_id, self.aluno, self.etapaAtual)

class conhecimento(models.Model):
    qualProjeto = models.ForeignKey(Projeto)
    usuario = models.CharField(max_length = 100)
    texto = models.CharField(max_length = 200)
    #por convencao, True sera certeza e False sera duvida
    certezaOuDuvida = models.BooleanField()

    def __unicode__(self):
        return self.texto

class unidadeInvestigacao(models.Model):
    nomeDoBloco = models.IntegerField()
    qualProjeto = models.ForeignKey(Projeto)
    conhecimentoPrevio = models.CharField(max_length=200)
    slugConhecimento = models.SlugField()
    investigador = models.CharField(max_length = 100, blank=True)
    prazo = models.DateField(blank=True, null=True)
    prazoFinal = models.DateField(blank=True, null=True)
    precisaAjuda = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s - %s" %(self.nomeDoBloco, self.conhecimentoPrevio)

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
    data = models.DateTimeField(default=datetime.now())

class textoProduzido(models.Model):
    titulo = models.CharField(max_length=300)
    vinculadoItem = models.ForeignKey(unidadeInvestigacao)
    criador = models.CharField(max_length=100)
    texto = models.TextField()
    historico = models.CharField(max_length=300)
    data = models.DateTimeField(default=datetime.now())