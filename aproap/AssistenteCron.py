from django_cron import CronJobBase, Schedule
from aproap.models import *
import datetime

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        dataAtual = datetime.date.today()
        print dataAtual
        datas = unidadeInvestigacao.objects.filter(prazoFinal=dataAtual)
        print datas
        for i in range(len(datas)):
            usuario = datas[i].investigador
            qualItem = datas[i]
            mensagem = u'%s, o item de conhecimento "%s" ' \
                       u'precisa ser finalizado hoje, %s' % (usuario, qualItem.conhecimentoPrevio, dataAtual)
            print mensagem
            #evita o assistente enviar avisos duplicados
            avisou = mensagemAssistente.objects.filter(mensagem=mensagem).count()
            #caso nao tenha nenhum aviso, mande
            if avisou == 0:
                a = mensagemAssistente.objects.create(usuario=usuario, qualItem=qualItem,
                                                  dataHora=dataAtual, mensagem=mensagem)
                a.save()
