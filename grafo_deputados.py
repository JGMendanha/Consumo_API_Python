import requests
import json
from requisicao import requests_votacoes_nominais

class Deputados:
  def __init__(self) -> None:
    self.adj_list = {}
    self.num_nos = 0
    self.num_arestas = 0

  def adicionar_no(self, no):
    if no in self.adj_list:
      return
    self.adj_list[no] = {}
    self.adj_list[no]["participacao"] = 0
    self.num_nos += 1

  def adicionar_aresta(self, no1, no2):
    if no1 not in self.adj_list:
      self.adicionar_no(no1)
    if no2 not in self.adj_list:
      self.adicionar_no(no2)
    if no2 in self.adj_list[no1]:
      self.adj_list[no1][no2] += 1
    else:
      self.adj_list[no1][no2] = 1
      self.num_arestas += 1

  def separando_deputados_por_voto(self):
    votos_sim = []
    votos_nao = []
    with open("links_votacoes_nominais.txt", 'r') as file:
      for linha in file:
        linha = linha.replace("\n", "")
        votos = requests_votacoes_nominais(linha)
        for i in range(len(votos["dados"])):
          voto_atual = votos["dados"][i]
          if voto_atual["tipoVoto"] == "Sim":
            votos_sim.append(voto_atual["deputado_"]["nome"])
          elif voto_atual["tipoVoto"] == "Não":
            votos_nao.append(voto_atual["deputado_"]["nome"])
        self.estruturacao_grafo(votos_sim)
        self.estruturacao_grafo(votos_nao)
        votos_sim = []
        votos_nao = []

  def estruturacao_grafo(self, votos):
    for dep in votos:
      for dep2 in votos:
        if dep == dep2:
          continue
        self.adicionar_aresta(dep, dep2)
      self.adj_list[dep]["participacao"] += 1

  def escrever_arquivo_grafo(self):
    dep_descobertos = []
    with open("votacaoVotos-2022-graph.txt", 'w') as file:
      file.write(f"{self.num_nos} {self.num_arestas}\n")
      for dep in self.adj_list:
        for dep2 in self.adj_list[dep]:
          if dep2 not in dep_descobertos and dep2 != "participacao":
            file.write(f"{dep} {dep2} {self.adj_list[dep][dep2]}\n")
        dep_descobertos.append(dep)

  def escrever_arquivo_participacao(self):
    with open("votacaoVotos-2022-participacao-deputados.txt", 'w') as file:
      participacao = "participacao"
      for dep in self.adj_list:
        file.write(f"{dep} {self.adj_list[dep][participacao]}\n")
