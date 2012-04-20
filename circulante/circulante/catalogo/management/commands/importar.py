# coding: utf-8

import io

from django.core.management.base import BaseCommand, CommandError

from circulante.catalogo.models import Publicacao

class Command(BaseCommand):
    args = '<arq_delimitado_por_tabs> [<encoding>]'
    help = 'Importa massa de dados da livraria (encoding default=utf-8)'

    def handle(self, *args, **options):
        
        if len(args) < 1:
            raise CommandError('Informe o nome do arquivo a importar')
        
        nome_arq = args[0]
        
        encoding = 'utf-8'
        if len(args) == 2:
            encoding = args[1]
        
        with io.open(nome_arq, 'rt', encoding=encoding) as arq_ent:
            qt_registros = 0
            try:
                #linhas = arq_ent.readlines()
                for linha in arq_ent:
                    linha = linha.rstrip()
                    if not linha:
                        continue
                    partes = linha.split('\t')
                    
                    id_padrao = None
                    autores = ''
                    
                    if len(partes) >= 3:
                        id_padrao, num_paginas, titulo = partes[:3]
                    if len(partes) == 4:
                        autores = partes[3]
                    
                    if id_padrao is None:
                        raise CommandError( repr(partes) )
                    
                    qt_registros += 1 
                
            except UnicodeDecodeError as exc:
                # para ativar uma linha de breakpoint para debug
                #import pdb; pdb.set_trace()
                msg = u'Encondig incorreto: "{0.reason}" posicao:{0.start}'
                raise CommandError(msg.format(exc))
            
        self.stdout.write('Importando %s linhas\n' % qt_registros)
