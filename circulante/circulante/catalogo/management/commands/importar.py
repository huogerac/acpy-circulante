# coding: utf-8

import io

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<arq_delimitado_por_tabs> [<encoding>]'
    help = 'Importa massa de dados da livraria (encoding default=utf-8)'

    def handle(self, *args, **options):
        
        if len(args) < 1:
            raise CommandError('Informe o nome do arquivo a importar')
        
        nome_arq = args[0]
        
        encoding = 'utf-8'
        if len(arqs) == 2:
            encoding = args[1]
        
        with io.open(nome_arq, 'rt', encoding=encoding) as arq_ent:
            linhas = arq_ent.readlines()
            
        self.stdout.write('Importando %s linhas\n' % len(linhas))
        
        #for poll_id in args:
        #    try:
        #        poll = Poll.objects.get(pk=int(poll_id))
        #    except Poll.DoesNotExist:
        #        raise CommandError('Poll "%s" does not exist' % poll_id)
        #    poll.opened = False
        #    poll.save()
