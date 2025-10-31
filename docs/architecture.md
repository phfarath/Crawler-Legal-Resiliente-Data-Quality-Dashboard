# Arquitetura do Crawler Legal Resiliente

## Visão Geral

O sistema é composto por múltiplos componentes integrados para garantir resiliência na coleta, qualidade de dados e observabilidade.

![Arquitetura](../README-detailed.md)

## Componentes Principais

- **Scrapy/Selenium**: Coleta de dados com mecanismos anti-bot
- **Pipelines**: Normalização, validação, deduplicação, enriquecimento
- **Persistência**: PostgreSQL (estruturado), MongoDB (raw), Redis (cache), OpenSearch (busca)
- **Mensageria**: RabbitMQ + Celery para execução assíncrona
- **Dashboard**: Streamlit para visualização de métricas em tempo real
- **API**: FastAPI para exposição de dados

```
               ┌──────────────┐
               │   Celery     │
               │  (Workers)   │
               └──────┬───────┘
                      │
        ┌─────────────▼─────────────┐
        │         Scrapy            │
        │   (Resilient Spider)      │
        └─────────────┬─────────────┘
                      │
              ┌───────▼───────┐
              │ Pipelines     │
              │(Normaliza etc)│
              └───────┬───────┘
                      │
        ┌─────────────▼────────────┐
        │   Persistência           │
        │ Postgres / Mongo / Redis │
        └─────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │   OpenSearch / API      │
         └────────────┬────────────┘
                      │
               ┌──────▼──────┐
               │ Dashboard   │
               └─────────────┘
```
