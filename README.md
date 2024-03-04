# Conversor de Moedas - README

Este projeto consiste em uma aplicação web construída utilizando Python/Django que oferece uma API para converter valores entre diferentes moedas. A aplicação utiliza uma API pública de cotações de moedas e criptomoedas para obter os dados necessários.

## FLUXO UML

![DIAGRAMA](https://i.imgur.com/JsvU26R.png)

## Organização do código

O código está organizado seguindo o padrão de separação de módulos, com uma estrutura clara que distingue entre a lógica de negócios (model), a interface com o usuário (view) e o back-end responsável por conectar-se com a API de cotações.

## CI

Realizei a criação de pipe no github actions para testar a aplicação com e sem Docker

## Cobertura de testes

A aplicação possui testes implementados utilizando Pytest para garantir a qualidade do código. Embora não seja esperada uma cobertura completa de testes, desenvolvi testes para cobrir as principais funcionalidades da aplicação.

Para rodar os teste, na rayz do projeto executar o comando `pytest`

## Escolhas técnicas

Foram feitas com base na adequação ao problema e na eficiência da solução.

# Como rodar a aplicação

## Localmente sem Docker

1. Instale o Python na versão 3.10.12.
2. Instale as dependências do projeto executando `pip install -r requirements.txt`.
3. Ative o ambiente virtual com `source venv/bin/activate`.
4. Inicie o servidor Django executando `python3 manage.py runserver`.
5. Para executar os testes, utilize o Pytest.

## Com Docker

1. Certifique-se de ter o Docker instalado em sua máquina.
2. Execute `docker compose up` no diretório raiz do projeto para construir e iniciar os contêineres Docker necessários para a aplicação.

# Chamadas de exemplo

A aplicação já está em funcionamento e pode ser acessada através do seguinte link de chamadas de API:

```
https://conversor-60f6.onrender.com/api/converter/?from=USD&to=ETH&amount=250
```

Esta chamada converte 250 dólares para Ethereum (ETH).

Outras moedas suportadas são USD, BRL, EUR, BTC. A rota de conversão localmente é:

```
http://localhost:8000/api/converter/?from=MOEDA-DE-ORIGEM&to=MOEDA-DESTINO&amount=QUANTIDADE
```

Substitua "MOEDA-DE-ORIGEM", "MOEDA-DESTINO" e "QUANTIDADE" pelos valores desejados para realizar a conversão.
````
