# SAPO-TOOLS
Toolkit para facilitar algumas operações ligadas ao sistema SAPO (Sistema de Auditoria de Portais).

## Builder
Ferramenta para facilitar o uso da aplicação web do SAPO. O Builder contém uma rotina que atualiza e executa as rotinas internas dos projetos [SAPO-API](https://github.com/JonKoala/sapo-api) e [SAPO-CLIENT](https://github.com/JonKoala/sapo-client), e por fim abre a aplicação web no navegador padrão do usuário.

### Requisitos
 - [Node](https://nodejs.org) >= 6.9
 - [gulp](https://gulpjs.com) (o [gulp-cli](https://github.com/gulpjs/gulp/blob/v3.9.1/docs/getting-started.md#getting-started) deve estar instalado como [pacote global](https://docs.npmjs.com/getting-started/installing-npm-packages-globally))

### Instalação
Clone o projeto para a sua máquina e acesse o diretório do mesmo.
``` bash
git clone https://github.com/JonKoala/sapo-tools.git
cd sapo-tools/builder
```
Instale as dependências.
``` bash
npm install
```

### Configuração
O projeto depende de um arquivo `appconfig.json`, na sua raiz, contendo algumas configurações locais. Crie uma cópia do arquivo `appconfig.json.example` e coloque as configurações do seu ambiente.

Exemplo de `appconfig.json`:
``` javascript
{
  "path": {
    "api": "../sapo-api/",
    "client": "../sapo-client/"
  },
  "url": "http://localhost:8081/"
}
```

### Execução
Para subir a aplicação web do SAPO, basta executar o comando `gulp` no terminal.
``` bash
gulp
```
Ou executar o arquivo `builder.bat`, que se encontra na raiz do projeto. Note que esse arquivo presume que o _npm_ foi instalado no caminho `%APPDATA%\npm`.

Caso não ocorra nenhum erro, os servidores de API e CLIENT devem ser criados e a aplicação irá abrir no navegador padrão do usuário.

## Scraper
Ferramenta para automatizar a avaliação das APIs dos jurisdicionados auditados. O Scraper varre a lista de APIs especificadas, busca os dados disponíveis, avalia os resultados e gera um relatório final sobre a avaliação.

A avaliação é feita sobre os seguintes quesitos:
 - disponibilidade (se as APIs estão realmente disponíveis na web)
 - existência de dados (se foi retornado algum dado na busca)
 - confiabilidade (nessa versão verifica-se apenas se a API retorna dados para datas posteriores à da execução)

### Requisitos
 - [Python](https://www.python.org/) >= 3.6
   - [PyYAML](http://pyyaml.org/wiki/PyYAML)
   - [Requests](http://docs.python-requests.org)

### Configuração
O projeto depende de um arquivo `appconfig.yaml`, na sua raiz, contendo algumas configurações locais. Crie uma cópia do arquivo `appconfig.yaml.example` e coloque as configurações do seu ambiente.

Exemplo de `appconfig.yaml`:
``` yaml
dates:
  - !!python/tuple [2017, 1]
  - !!python/tuple [2017, 2]

logger:
  filepath: 'output'
  filename: 'log.txt'
```
O Scraper também depende de um arquivo `source.csv`, na sua raiz, contendo a lista dos jurisdicionados a serem auditados e as URLs de suas APIs. Crie uma cópia do arquivo `source.csv` e coloque as informações necessárias.

Cada linha do `source.csv` deve obedecer à seguinte estrutura:
``` csv
[MUNICÍPIO];;[URL DA PREFEITURA];;[URL DA CÂMARA];
```
Exemplo de `source.csv`:
``` csv
Município;;Prefeitura;;Camara;
Afonso Cláudio;;https://afonsoclaudio-es.portaltp.com.br;;https://cmafonsoclaudio-es.portaltp.com.br;
...
```

### Execução
Para executar a rotina do Scraper, basta executar o script `routine.py`.
``` bash
python routine.py
```
Ou executar o arquivo `scraper.bat`, que se encontra na raiz do projeto. Note que esse arquivo presume que o _Python_ foi instalado no caminho `%PROGRAMDATA%\Anaconda3` e as bibliotecas extras no caminho `%PROGRAMDATA%\Anaconda3\Scripts`.

Ao final da rotina o script deve gerar um arquivo `results.csv` na pasta `output`, contendo os resultados dos testes realizados sobre cada jurisdicionado.

## Video Compressor
Ferramenta para automatizar a compressão de vídeos.

### Requisitos
 - [Node](https://nodejs.org) >= 6.9
 - [FFmpeg](https://www.ffmpeg.org) >= 3.4

### Instalação
Clone o projeto para a sua máquina e acesse o diretório do mesmo.
``` bash
git clone https://github.com/JonKoala/sapo-tools.git
cd sapo-tools/video-compressor
```
Instale as dependências.
``` bash
npm install
```

### Configuração
O projeto depende de um arquivo `appconfig.json`, na sua raiz, contendo algumas configurações locais. Crie uma cópia do arquivo `appconfig.json.example` e coloque as configurações do seu ambiente.

Exemplo de `appconfig.json`:
``` javascript
{
  "codec": "libx264",
  "bitrate": "500k"
}
```

### Execução
Antes de executar o script, certifique-se que os vídeos a serem comprimidos estão na pasta `input`.

Para executar a rotina de compressão, basta executar o comando `start` do _npm_.
``` bash
npm start
```
Ou executar o arquivo `compressor.bat`, que se encontra na raiz do projeto. Note que esse arquivo presume que o _npm_ foi instalado no caminho `%APPDATA%\npm` e o _FFmpeg_ no caminho `%APPDATA%\ffmpeg\bin`.

Ao final da rotina o script deve gerar na pasta `output` um novo vídeo, já comprimido, para cada vídeo presente na pasta `input`.
