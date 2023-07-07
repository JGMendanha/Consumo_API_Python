import requests
import json

def requests_ids():
  id_votacao = requests.get("https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio=2022-01-01&ordem=DESC&ordenarPor=dataHoraRegistro")

  id_votacao = id_votacao.json()
  with open("links_votacoes_nominais.txt", 'w') as file:
    for i in range(len(id_votacao["dados"])):
      ids = id_votacao["dados"][i]
      id = "https://dadosabertos.camara.leg.br/api/v2/votacoes/" + ids["id"] + "/votos"
      votacoes_nominas = requests.get(id)
      votacoes_nominas = votacoes_nominas.json()
      if votacoes_nominas["dados"] != []:
        file.write(f"{id}\n")

def requests_votacoes_nominais(link):
  votos = requests.get(link)
  votos = votos.json()
  return votos
