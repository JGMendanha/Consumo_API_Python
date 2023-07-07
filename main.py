import requisicao as r
from grafo_deputados import Deputados

r.requests_ids()

grafoDeputados = Deputados()

grafoDeputados.separando_deputados_por_voto()

grafoDeputados.escrever_arquivo_grafo()

grafoDeputados.escrever_arquivo_participacao()
