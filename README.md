# Twitter Stream Extractor

[![License](https://img.shields.io/github/license/AlanTaranti/twitter_stream_extractor)](LICENSE)
![Maintenance](https://img.shields.io/maintenance/yes/2022)

Extrai tweets de acordo com as regras definidas pré-estabelecidos e os converte no formato Pandas.

## Começando

Estas instruções vão te ajudar a iniciar o projeto.

### Prerequisitos

- Python 3

### Instalando

```
pip install -r requirements.txt
```
```
cp .env.example .env
```

### Configurando

Adicione no arquivo .env a chave da API do Twitter e altere as variáveis conforme a necessidade.

- Variável DATA_TYPE - altera o tipo de dado extraído. Atualmente somente suportado 'emoji'.

### Executando
```
python start.py
```

## Licença

Este trabalho está licenciado sobre a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.
