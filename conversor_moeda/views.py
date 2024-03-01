from django.http import JsonResponse
import requests
import locale

# Variável global para armazenar os dados das taxas de câmbio filtradas
filtered_data = None

def get_exchange_rate(request):
    global filtered_data

    url = f"https://economia.awesomeapi.com.br/last/USD-BRL,USD-EUR,ETH-USD,BTC-USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        filtered_data = {}
        
        for currency, info in data.items():
            filtered_data[currency] = {
                'code': info['code'],
                'codein': info['codein'],
                'name': info['name'],
                'bid': info['bid']
            }
        
        return JsonResponse(filtered_data)
    
    return JsonResponse({'error': 'Failed to fetch exchange rate data'})

# Chama a função get_exchange_rate() para recuperar e salvar os dados de taxa de câmbio no início
get_exchange_rate(None)

def convert_currency(request):
    global filtered_data

    from_currency = request.GET.get('from')
    to_currency = request.GET.get('to')
    amount = float(request.GET.get('amount', 0))

    if not from_currency or not to_currency or not amount:
        return JsonResponse({'error': 'Missing parameters'})

    if not filtered_data:
        get_exchange_rate(None)

    # Se a moeda de destino for "USD", retornar o valor convertido em from_currency para USD
    if to_currency == 'USD':
        if from_currency == 'USD':
            return JsonResponse({
                'from_currency': f'{from_currency}',
                'to_currency': f'{to_currency}',
                'amount': amount,
                'conversion': amount
            })
        else:
            # Verifica se a moeda de origem é BTC ou ETH
            if from_currency in ['BTC', 'ETH']:
                # Procura pela taxa de câmbio correspondente ao par moeda + "USD"
                if f"{from_currency}USD" in filtered_data:
                    rate_from = float(filtered_data[f"{from_currency}USD"]['bid'])
                else:
                    return JsonResponse({'error': f'Exchange rate for {from_currency} not found'})
                
                # Calcula o valor convertido de from_currency para USD
                amount_usd = amount * rate_from
            else:
                # Verifica se a moeda de origem é "USD"
                if from_currency == 'USD':
                    amount_usd = amount
                else:
                    # Procura pela taxa de câmbio correspondente ao par "USD" + moeda
                    if f"USD{from_currency}" in filtered_data:
                        rate_from = float(filtered_data[f"USD{from_currency}"]['bid'])
                    else:
                        return JsonResponse({'error': f'Exchange rate for {from_currency} not found'})
                    
                    # Calcula o valor convertido de from_currency para USD
                    amount_usd = amount / rate_from

                    formatted_amount = f'${amount_usd:,.2f}'   

            return JsonResponse({
                'from_currency': f'{from_currency}',
                'to_currency': f'{to_currency}',
                'amount': amount,
                'conversion': formatted_amount
            })

    # Verifica se a moeda de origem é BTC ou ETH
    if from_currency in ['BTC', 'ETH']:
        # Procura pela taxa de câmbio correspondente ao par moeda + "USD"
        if f"{from_currency}USD" in filtered_data:
            rate_from = float(filtered_data[f"{from_currency}USD"]['bid'])
        else:
            return JsonResponse({'error': f'Exchange rate for {from_currency} not found'})
        
        # Calcula o valor convertido de from_currency para USD
        amount_usd = amount * rate_from
    else:
        # Verifica se a moeda de origem é "USD"
        if from_currency == 'USD':
            amount_usd = amount
        else:
            # Procura pela taxa de câmbio correspondente ao par "USD" + moeda
            if f"USD{from_currency}" in filtered_data:
                rate_from = float(filtered_data[f"USD{from_currency}"]['bid'])
            else:
                return JsonResponse({'error': f'Exchange rate for {from_currency} not found'})
            
            # Calcula o valor convertido de from_currency para USD
            amount_usd = amount / rate_from

    # Verifica se a moeda final é BTC ou ETH
    if to_currency in ['BTC', 'ETH']:
        # Procura pela taxa de câmbio correspondente ao par "USD" + moeda
        if f"{to_currency}USD" in filtered_data:
            rate_to_usd = float(filtered_data[f"{to_currency}USD"]['bid'])
        else:
            return JsonResponse({'error': f'Exchange rate for {to_currency} not found'})
        
        # Calcula o valor convertido de USD para to_currency
        converted_amount = amount_usd / rate_to_usd
    else:
        # Procura pela taxa de câmbio correspondente ao par moeda + "USD"
        if f"USD{to_currency}" in filtered_data:
            rate_to_usd = float(filtered_data[f"USD{to_currency}"]['bid'])
        else:
            return JsonResponse({'error': f'Exchange rate for {to_currency} not found'})
        
        # Calcula o valor convertido de USD para to_currency
        converted_amount = amount_usd * rate_to_usd

    # Formata o valor convertido na moeda de destino com sua formatação padrão
    if to_currency == 'BTC':
        formatted_amount = f'{to_currency}{converted_amount:.8f}'
    elif to_currency == 'ETH':
        formatted_amount = f'{to_currency}{converted_amount:.6f}'
    elif to_currency == 'BRL':
        formatted_amount = f'R${converted_amount:,.2f}'
    elif to_currency == 'EUR':
        formatted_amount = f'€{converted_amount:,.2f}'
     
    else:
        locale.setlocale(locale.LC_ALL, '')
        formatted_amount = locale.currency(converted_amount, grouping=True)

    return JsonResponse({
        'from_currency': f'{from_currency}-USD',
        'to_currency': f'{to_currency}',
        'amount': amount,
        'conversion': formatted_amount
    })
