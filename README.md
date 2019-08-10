# Twitter Stream Extractor

Extrai tweets em vários idiomas de acordo com termos pré-estabelecidos e os converte no formato Pandas.

## Começando

Estas instruções vão te ajudar a iniciar o projeto.

### Prerequisites

- Python 3

### Instalando

```
pip install -r requirements.txt
```
```
cp .env.example .env
```

### Configurando

Adcicione no arquivo .env a chave da API do Twitter e altere as variáveis conforme a necessidade.

- Variável DATA_TYPE - altera o tipo de dado extraído. Atualmente somente suportado 'emoji'.

### Executando
```
python start.py
```

## Licença

Este trabalho está licenciado sobre a MIT License - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.
