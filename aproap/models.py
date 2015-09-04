from django.db import models
from datetime import datetime

class Usuarios(models.Model):
    nomeCompleto = models.CharField(max_length = 100)

class espacoProjeto(models.Model):
    nome = models.CharField(max_length=50)

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
    totalDeVotosRecebidos = models.FloatField()

class alunosNoProjeto(models.Model):
    projeto = models.ForeignKey(Projeto)
    aluno = models.CharField(max_length = 100)
    etapaAtual = models.IntegerField(default=1)
    ondeparou = models.CharField(max_length=30, default="/espacos/")

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

    def __unicode__(self):
        return "%s - %s" %(self.nomeDoBloco, self.conhecimentoPrevio)