# Crawler Legal Resiliente + Data Quality Dashboard

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)

Sistema de crawling robusto e resiliente para coleta automatizada de decisões judiciais dos principais portais brasileiros (PJe, eSAJ, eProc) com dashboard de qualidade de dados e monitoramento em tempo real.

## 🚀 Quick Start

### Pré-requisitos
- Python 3.9+
- Docker e Docker Compose
- Git

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/crawler-legal-resiliente.git
cd crawler-legal-resiliente

# Configure variáveis de ambiente
cp .env.example .env

# Inicie os serviços com Docker
docker-compose up -d

# Acesse o dashboard
open http://localhost:8501
```

## ⚡ Funcionalidades Principais

### 1. Crawling Resiliente
- ✅ Retry automático com backoff exponencial
- ✅ Rotação de proxies e user-agents
- ✅ Detecção e resolução de CAPTCHAs
- ✅ Fallback entre Scrapy/Selenium
- ✅ Auto-recuperação de falhas estruturais

### 2. Qualidade de Dados
- ✅ Validação de schemas com Pydantic
- ✅ Normalização automática (CNJ, datas, textos)
- ✅ Deduplicação (hash exato + MinHash fuzzy)
- ✅ Enriquecimento com metadados derivados

### 3. Monitoramento
- ✅ Dashboard Streamlit em tempo real
- ✅ Métricas Prometheus
- ✅ Alertas automáticos (Slack, email, Sentry)
- ✅ Detecção de mudanças estruturais nos portais

### 4. Arquitetura Cloud-Ready
- ✅ Deploy via Docker/Docker Compose
- ✅ Suporte para GCP e AWS
- ✅ Message queue com RabbitMQ + Celery
- ✅ Multi-database (PostgreSQL, MongoDB, Redis, OpenSearch)

## 📊 Stack Tecnológica

| Categoria | Tecnologias |
|-----------|-------------|
| **Crawling** | Scrapy, Selenium, undetected-chromedriver |
| **Anti-Bot** | fake-useragent, playwright-stealth, 2captcha |
| **Qualidade** | Pydantic, pandas, fuzzywuzzy, datasketch |
| **Databases** | PostgreSQL, MongoDB, Redis, OpenSearch |
| **Queue** | RabbitMQ, Celery, Flower |
| **Dashboard** | Streamlit, Plotly |
| **API** | FastAPI |
| **Deploy** | Docker, Docker Compose |

## 📁 Estrutura do Projeto

```
crawler-legal-resiliente/
├── src/                        # Código-fonte principal
│   ├── crawlers/              # Spiders (PJe, eSAJ, eProc)
│   ├── pipelines/             # Processamento de dados
│   ├── models/                # Modelos e schemas
│   ├── database/              # Camadas de persistência
│   ├── services/              # Serviços de negócio
│   ├── utils/                 # Utilitários
│   ├── config/                # Configurações
│   └── tasks/                 # Tasks Celery
├── dashboard/                  # Dashboard Streamlit
├── api/                       # API REST
├── tests/                     # Testes automatizados
├── docker-compose.yml         # Orquestração de containers
└── requirements.txt           # Dependências Python
```

## 🔧 Configuração

### Variáveis de Ambiente

Copie `.env.example` para `.env` e ajuste conforme necessário:

```bash
# Principais configurações
ENVIRONMENT=development
PROXY_ENABLED=false
CAPTCHA_API_KEY=chave-api-servico
SLACK_WEBHOOK_URL=chave-api-servico
SENTRY_DSN=chave-api-servico
```

### Bancos de Dados

O projeto usa múltiplos bancos para diferentes propósitos:

- **PostgreSQL**: Metadados estruturados (decisões, partes, datas)
- **MongoDB**: Documentos brutos (HTML, JSON)
- **Redis**: Cache, sessões, deduplicação
- **OpenSearch**: Busca full-text

Todos são provisionados automaticamente via Docker Compose.

## 🏃 Execução

### Local (Desenvolvimento)

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar bancos via Docker
docker-compose up -d postgres mongodb redis rabbitmq opensearch

# Executar spider
scrapy crawl tjsp_esaj

# Iniciar dashboard
streamlit run dashboard/app.py

# Iniciar API
uvicorn api.main:app --reload
```

### Docker (Produção)

```bash
# Build e start completo
docker-compose up -d

# Escalar workers
docker-compose up -d --scale crawler-worker=5

# Ver logs
docker-compose logs -f dashboard

# Parar tudo
docker-compose down
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Apenas testes unitários
pytest tests/unit/

# Testes específicos
pytest tests/unit/test_cnj_utils.py -v
```

## 📊 Dashboard

Acesse `http://localhost:8501` para visualizar:

- **Overview**: Total de processos, taxa de sucesso, cobertura
- **Qualidade**: Duplicatas, completude, validações
- **Portais**: Status e latência de cada portal
- **Alertas**: Notificações de erros e falhas

## 🔍 API REST

Acesse `http://localhost:8000/docs` para documentação interativa.

Principais endpoints:

```
GET /health              # Health check
GET /api/v1/decisions    # Listar decisões
GET /api/v1/decisions/{cnj}  # Buscar por número CNJ
GET /api/v1/metrics/quality  # Métricas de qualidade
```

## 📝 Desenvolvimento

### Code Style

O projeto segue PEP8 com Black + isort + flake8:

```bash
# Formatar código
black src/ tests/

# Ordenar imports
isort src/ tests/

# Linter
flake8 src/ tests/

# Type checking
mypy src/
```

### Pre-commit Hooks

```bash
# Instalar hooks
pre-commit install

# Executar manualmente
pre-commit run --all-files
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Projeto desenvolvido para demonstrar boas práticas em web scraping, qualidade de dados e observabilidade
- Stack tecnológico baseado em ferramentas production-grade usadas pela indústria

## 📞 Contato

- **Documentação Completa**: Ver [README-detailed.md](README-detailed.md)
- **Issues**: https://github.com/seu-usuario/crawler-legal-resiliente/issues

---

**⚖️ Desenvolvido com foco em resiliência, qualidade e observabilidade**
