from conversor_moeda.views import convert_currency
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
import json

api_response_mock = {
    "USDBRL": {"code": "USD", "codein": "BRL", "name": "Dólar Americano/Real Brasileiro", "bid": "4.9514"},
    "USDEUR": {"code": "USD", "codein": "EUR", "name": "Dólar Americano/Euro", "bid": "0.9226"},
    "ETHUSD": {"code": "ETH", "codein": "USD", "name": "Ethereum/Dólar Americano", "bid": "3411.31"},
    "BTCUSD": {"code": "BTC", "codein": "USD", "name": "Bitcoin/Dólar Americano", "bid": "61839"}
}

def test_missing_parameters_error():
    # Criando uma solicitação de mock com parâmetros ausentes
    request_factory = RequestFactory()
    request = request_factory.post('/path/', {'from': '', 'to': 'BRL', 'amount': ''})

    # Chamando a função convert_currency com os dados mockados
    response = convert_currency(request)
    response_data = json.loads(response.content)

    # Verificando se a mensagem de erro está presente na resposta
    assert 'error' in response_data

def test_convert_currency():
    # Testando conversão de BTC para BRL
    request_btc_to_brl = MagicMock()
    request_btc_to_brl.GET = {'from': 'BTC', 'to': 'BRL', 'amount': '1'}

    # Chamando a função convert_currency com os dados mockados
    with patch('conversor_moeda.views.filtered_data', api_response_mock):
        response_btc_to_brl = convert_currency(request_btc_to_brl)
    
    assert response_btc_to_brl.status_code == 200

    # Verifica se a conversão para USD está correta
    assert b'"from_currency": "BTC-USD"' in response_btc_to_brl.content

    # Verifica se a conversão para BRL está correta
    assert b'"to_currency": "BRL"' in response_btc_to_brl.content

    # Verifica se a conversão foi realizada corretamente
    assert b'"conversion": "R$306,189.62"' in response_btc_to_brl.content

def test_no_params():   

    # Testando parâmetros ausentes
    request = type('Request', (object,), {'GET': {}})
    response = convert_currency(request)
    assert response.status_code == 200
    assert response.content == b'{"error": "Missing parameters"}'