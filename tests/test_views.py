from unittest.mock import patch
from django.http import JsonResponse
from conversor_moeda.views import get_exchange_rate

def test_get_exchange_rate():
    # Simule uma resposta bem-sucedida da API
    class MockResponse:
        status_code = 200
        def json(self):
            return {
                "USD-BRL": {"code": "USD", "codein": "BRL", "name": "Dólar Americano/Real Brasileiro", "bid": "5.38"},
                "USD-EUR": {"code": "USD", "codein": "EUR", "name": "Dólar Americano/Euro", "bid": "0.88"}
            }

    # Defina o resultado esperado com base nos dados simulados
    expected_result = JsonResponse({
        "USD-BRL": {"code": "USD", "codein": "BRL", "name": "Dólar Americano/Real Brasileiro", "bid": "5.38"},
        "USD-EUR": {"code": "USD", "codein": "EUR", "name": "Dólar Americano/Euro", "bid": "0.88"}
    })

    # Substitua a função requests.get por uma versão mockada
    with patch('conversor_moeda.views.requests.get') as mocked_get:
        mocked_get.return_value = MockResponse()
        
        # Chame a função e obtenha o resultado real
        response = get_exchange_rate(None)

        # Verifique se o resultado real é igual ao esperado
        assert response.content == expected_result.content
