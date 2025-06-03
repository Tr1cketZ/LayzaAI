# Backend da Layza AI

Este é o backend da plataforma educacional Layza AI, uma tutora virtual que ajuda estudantes do ensino médio a se prepararem para o ENEM.

## Bibliotecas Educacionais Integradas

O backend agora integra as melhores bibliotecas gratuitas para cada disciplina:

### Matemática
- **SymPy**: Matemática simbólica (álgebra, cálculo, equações)
- **NumPy**: Computação numérica
- **Matplotlib**: Geração de gráficos matemáticos

### Ciências
- **SciPy**: Cálculos científicos, estatística, física
- **BioPython**: Análise de dados biológicos
- **ChemPy**: Química computacional

### Português
- **spaCy**: Processamento de linguagem natural para português
- **NLTK**: Ferramentas clássicas de PLN
- **TextBlob-pt**: Análise de sentimentos e processamento de texto em português

## Configuração do DeepSeek API

O backend utiliza a API do DeepSeek v3 para gerar respostas inteligentes para os usuários. Para configurar:

1. Crie uma conta em [DeepSeek](https://platform.deepseek.com/) e obtenha sua chave de API
2. Crie um arquivo `.env` na pasta `backend/` com o seguinte conteúdo:

```
DEEPSEEK_API_KEY=sua_chave_api_aqui
```

3. Substitua `sua_chave_api_aqui` pela sua chave de API real

## Instalação

```bash
pip install -r requirements.txt
```

## Executando o servidor

```bash
python server.py
```

O servidor será iniciado em `http://localhost:5000`.

## Testando as bibliotecas integradas

Acesse o endpoint:

```
GET http://localhost:5000/api/libraries-check
```

Você verá um JSON indicando se cada biblioteca está funcionando corretamente.

## Endpoints da API

- `/api/chat` - Endpoint para conversação com a IA
- `/api/upload-image` - Endpoint para upload de imagens
- `/api/upload-audio` - Endpoint para upload de áudio
- `/api/youtube-recommendations` - Endpoint para recomendações de vídeos do YouTube
- `/api/exam-papers` - Endpoint para obter provas do ENEM
- `/api/feedback` - Endpoint para enviar feedback sobre a conversa
- `/api/libraries-check` - Testa se todas as bibliotecas educacionais estão funcionando 