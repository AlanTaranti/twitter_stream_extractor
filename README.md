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

Adicione no arquivo .env o Bearer Token da API do Twitter.
Caso não tenha um token de acesso, é necessário solicitar ao Twitter através do [Portal do Desenvolvedor](https://developer.twitter.com/)

### Executando
```
python cli.py --help
```

```
python cli.py run-emoji --output tweets
```

```
python cli.py run '(biscoito OR bolacha) lang:pt -is:retweet' briga_eterna
```

## Licença

Este trabalho está licenciado sobre a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.
