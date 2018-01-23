import datetime as dt, pprint, time
import pandas as pd
import requests


print('\nIniciando coleta de dados...\n')
print('Recolhendo dados de deputados...')
## DEPUTADOS
t0 = time.time()

hoje = dt.date.today()
r = requests.get("https://dadosabertos.camara.leg.br/api/v2/legislaturas?data={}".format(hoje))
legislatura_atual = r.json()['dados'][0]['id']

deputados = []
url = "https://dadosabertos.camara.leg.br/api/v2/deputados/?idLegislatura={}&itens=100".format(legislatura_atual)

while True:
    r = requests.get(url)
    d = r.json()

    for parl in d['dados']:
        uri = parl['uri']
        cadastro = requests.get(uri).json()['dados']
        if cadastro['ultimoStatus']['situacao'] != "Exercício":
            continue

        dados_deputado = {
            "casa": "Camara dos Deputados",
            "nome_civil": cadastro['nomeCivil'],
            "nome_parlamentar": cadastro["ultimoStatus"]['nomeEleitoral'],
            "partido": cadastro["ultimoStatus"]['siglaPartido'],
            "uf": cadastro["ultimoStatus"]['siglaUf'],
            'endereco': "Câmara dos Deputados, Edifício Anexo" + cadastro["ultimoStatus"]['gabinete']['predio'] + ", gabinete nº" + cadastro["ultimoStatus"]['gabinete']['sala'],
            "telefone": cadastro["ultimoStatus"]['gabinete']['telefone'],
            "email": cadastro["ultimoStatus"]['gabinete']['email'],
            "condicaoEleitoral": cadastro["ultimoStatus"]['condicaoEleitoral'],
            "genero": cadastro["sexo"],
            "data_nascimento": cadastro["dataNascimento"],
            "uf_nascimento": cadastro['ufNascimento']
        }

        deputados.append(dados_deputado)

    url = next((link for link in d['links'] if link["rel"] == "next"), None)
    if not url:
        break
    url = url['href']

print('Finalizada coleta de deputados - total obtido: {} em {:.02f}s'.format(len(deputados), time.time() - t0))
deputados = pd.DataFrame(deputados)
deputados.to_csv('data/deputados.csv', index=False, encoding='utf-8')

print('Recolhendo dados de senadores...')
## SENADORES
t1 = time.time()

url = 'http://legis.senado.leg.br/dadosabertos/senador/lista/atual'
headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
r = requests.get(url, headers=headers)
dados = r.json()['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']

senadores = []
for parl in dados:
    url = "http://legis.senado.leg.br/dadosabertos/senador/{}".format(parl['IdentificacaoParlamentar']['CodigoParlamentar'])
    r = requests.get(url, headers=headers)
    senador = r.json()

    identificacao = senador['DetalheParlamentar']['Parlamentar']['IdentificacaoParlamentar']
    dados_basicos = senador['DetalheParlamentar']['Parlamentar']['DadosBasicosParlamentar']
    mandato = senador['DetalheParlamentar']['Parlamentar']['MandatoAtual']

    dados_senador = {
        "casa": "Senado Federal",
        "nome_civil": identificacao.get('NomeCompletoParlamentar'),
        "nome_parlamentar": identificacao.get('NomeParlamentar'),
        "partido": identificacao.get('SiglaPartidoParlamentar'),
        "uf": identificacao.get('UfParlamentar'),
        "endereco": dados_basicos.get('EnderecoParlamentar'),
        "telefone": dados_basicos.get('TelefoneParlamentar'),
        "email": identificacao.get('EmailParlamentar'),
        "condicaoEleitoral": mandato.get('DescricaoParticipacao'),
        "genero": identificacao.get('SexoParlamentar'),
        "data_nascimento": dados_basicos.get("DataNascimento"),
        "uf_nascimento": dados_basicos.get('UfNaturalidade')
    }

    senadores.append(dados_senador)
    
print('Finalizada coleta de senadores - total obtido: {} em {:.02f}s'.format(len(senadores), time.time() - t1))

senadores = pd.DataFrame(senadores)
senadores.genero = senadores.genero.map({'Masculino': "M", "Feminino": 'F'})
senadores.to_csv('data/senadores.csv', index=False, encoding='utf-8')

parlamentares = pd.concat([deputados, senadores])
parlamentares.to_csv('data/parlamentares.csv', index=False, encoding='utf-8')
