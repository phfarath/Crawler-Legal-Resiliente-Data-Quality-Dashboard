"""Métricas Prometheus para monitoramento."""

from prometheus_client import Counter, Gauge, Histogram

requests_total = Counter(
    "crawler_requests_total",
    "Total de requisições",
    ["portal", "status"],
)

items_scraped = Counter(
    "crawler_items_scraped_total",
    "Total de itens coletados",
    ["portal", "spider"],
)

duplicates_found = Counter(
    "crawler_duplicates_total",
    "Total de duplicatas detectadas",
    ["tipo"],
)

request_duration = Histogram(
    "crawler_request_duration_seconds",
    "Duração das requisições",
    ["portal"],
)

processing_duration = Histogram(
    "crawler_processing_duration_seconds",
    "Duração do processamento",
    ["pipeline"],
)

active_spiders = Gauge(
    "crawler_active_spiders",
    "Quantidade de spiders ativas",
    ["portal"],
)

portal_health = Gauge(
    "crawler_portal_health",
    "Saúde calculada do portal",
    ["portal"],
)
