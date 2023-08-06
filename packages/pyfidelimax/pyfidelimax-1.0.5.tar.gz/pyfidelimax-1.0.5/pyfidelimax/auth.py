import requests
import json


def ResponseGet(token=None, url=None):
    headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    if token:
        headers.update({'AuthToken': token})
    response = requests.get(url, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict


def ResponsePost(token, url, data={}):
    data = json.dumps(data)
    headers = {'AuthToken': token, 'content-type': 'application/json', 'Accept': 'application/json'}
    responose = requests.post(url, data=data, headers=headers)
    responose_dict = json.loads(responose.text)
    return responose_dict


def GetToken(login, password):
    data = {'Login': login, 'Senha': password}
    token_url = "https://api.fidelimax.com.br/api/Integracao/GetToken"
    responose = requests.post(token_url, data=data)
    return json.loads(responose.text)
            


def LojaPertencentesPrograma(login, password):
    token = GetToken(login, password)
    url = "https://api.fidelimax.com.br/api/Integracao/LojaPertencentesPrograma?token={'%s'}" % token
    return ResponseGet(token, url)


def CadastrarConsumidor(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/CadastrarConsumidor"
    token_dict = GetToken(login, password)
    if token_dict.get('MensagemErro', False):
        return token_dict
    token = token_dict['token']
    return ResponsePost(token, url, data)


def AtualizarConsumidor(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/AtualizarConsumidor"
    token_dict = GetToken(login, password)
    if token_dict.get('MensagemErro', False):
        return token_dict
    token = token_dict['token']	
    return ResponsePost(token, url, data)

def ExtratoConsumidor(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/ExtratoConsumidor"
    token_dict = GetToken(login, password)
    if token_dict.get('MensagemErro', False):
        return token_dict
    token = token_dict['token']	
    return ResponsePost(token, url, data)

def ConsultaConsumidor(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/ConsultaConsumidor"
    token_dict = GetToken(login, password)
    if token_dict.get('MensagemErro', False):
        return token_dict
    token = token_dict['token']	
    return ResponsePost(token, url, data)


def RetornaDadosCliente(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/RetornaDadosCliente"
    token_dict = GetToken(login, password)
    if token_dict.get('MensagemErro', False):
        return token_dict
    token = token_dict['token']	
    return ResponsePost(token, url, data)


def ResgataPremio(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/ResgataPremio"
    token_dict = GetToken(login, password)
    if token_dict.get('MensagemErro', False):
        return token_dict
    token = token_dict['token']
    return ResponsePost(token, url, data)


def PontuaConsumidor(login, password, data={}):
    url = "https://api.fidelimax.com.br/api/Integracao/PontuaConsumidor"
    token_dict = GetToken(login, password)
    if token_dict.get('MensagemErro', False):
        return token_dict
    token = token_dict['token']	
    return ResponsePost(token, url, data)


def ListaProdutos(login, password):
    url = "https://api.fidelimax.com.br/api/Integracao/ListaProdutos"
    token_dict = GetToken(login, password)
    if token_dict.get('MensagemErro', False):
        return token_dict
    token = token_dict['token']	
    return ResponseGet(token, url)
