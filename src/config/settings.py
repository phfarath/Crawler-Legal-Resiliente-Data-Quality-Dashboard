"""Configurações centralizadas do projeto."""

from functools import lru_cache
from typing import List, Optional

from pydantic import AnyUrl, BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente."""

    project_name: str = Field("Crawler Legal Resiliente", alias="PROJECT_NAME")
    environment: str = Field("development", alias="ENVIRONMENT")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    timezone: str = Field("America/Sao_Paulo", alias="TIMEZONE")

    # PostgreSQL
    postgres_host: str = Field("localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_db: str = Field("crawler_legal", alias="POSTGRES_DB")
    postgres_user: str = Field("crawler_admin", alias="POSTGRES_USER")
    postgres_password: str = Field("SecurePassword123!", alias="POSTGRES_PASSWORD")
    postgres_max_connections: int = Field(100, alias="POSTGRES_MAX_CONNECTIONS")
    postgres_pool_size: int = Field(20, alias="POSTGRES_POOL_SIZE")

    # MongoDB
    mongodb_host: str = Field("localhost", alias="MONGODB_HOST")
    mongodb_port: int = Field(27017, alias="MONGODB_PORT")
    mongodb_db: str = Field("judicial_documents", alias="MONGODB_DB")
    mongodb_user: str = Field("mongo_admin", alias="MONGODB_USER")
    mongodb_password: str = Field("SecureMongoPass456!", alias="MONGODB_PASSWORD")
    mongodb_max_pool_size: int = Field(50, alias="MONGODB_MAX_POOL_SIZE")

    # Redis
    redis_host: str = Field("localhost", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    redis_db: int = Field(0, alias="REDIS_DB")
    redis_password: str = Field("SecureRedisPass789!", alias="REDIS_PASSWORD")
    redis_max_connections: int = Field(50, alias="REDIS_MAX_CONNECTIONS")

    # RabbitMQ
    rabbitmq_host: str = Field("localhost", alias="RABBITMQ_HOST")
    rabbitmq_port: int = Field(5672, alias="RABBITMQ_PORT")
    rabbitmq_management_port: int = Field(15672, alias="RABBITMQ_MANAGEMENT_PORT")
    rabbitmq_user: str = Field("rabbitmq_admin", alias="RABBITMQ_USER")
    rabbitmq_password: str = Field("SecureRabbitPass012!", alias="RABBITMQ_PASSWORD")
    rabbitmq_vhost: str = Field("/crawler", alias="RABBITMQ_VHOST")

    # OpenSearch
    opensearch_host: str = Field("localhost", alias="OPENSEARCH_HOST")
    opensearch_port: int = Field(9200, alias="OPENSEARCH_PORT")
    opensearch_user: str = Field("admin", alias="OPENSEARCH_USER")
    opensearch_password: str = Field("SecureSearchPass345!", alias="OPENSEARCH_PASSWORD")
    opensearch_index: str = Field("judicial_decisions", alias="OPENSEARCH_INDEX")

    # Scrapy
    scrapy_concurrent_requests: int = Field(16, alias="SCRAPY_CONCURRENT_REQUESTS")
    scrapy_download_delay: float = Field(0.5, alias="SCRAPY_DOWNLOAD_DELAY")
    scrapy_autothrottle_enabled: bool = Field(True, alias="SCRAPY_AUTOTHROTTLE_ENABLED")
    scrapy_autothrottle_target_concurrency: float = Field(
        4.0, alias="SCRAPY_AUTOTHROTTLE_TARGET_CONCURRENCY"
    )
    scrapy_retry_times: int = Field(5, alias="SCRAPY_RETRY_TIMES")
    scrapy_user_agent_rotation: bool = Field(True, alias="SCRAPY_USER_AGENT_ROTATION")

    # Selenium
    selenium_headless: bool = Field(True, alias="SELENIUM_HEADLESS")
    selenium_driver_path: str = Field("/usr/local/bin/chromedriver", alias="SELENIUM_DRIVER_PATH")
    selenium_implicit_wait: int = Field(10, alias="SELENIUM_IMPLICIT_WAIT")
    selenium_page_load_timeout: int = Field(30, alias="SELENIUM_PAGE_LOAD_TIMEOUT")

    # Anti Bot
    proxy_enabled: bool = Field(False, alias="PROXY_ENABLED")
    proxy_pool_size: int = Field(50, alias="PROXY_POOL_SIZE")
    proxy_provider: str = Field("custom", alias="PROXY_PROVIDER")
    proxy_rotation_interval: int = Field(300, alias="PROXY_ROTATION_INTERVAL")
    captcha_solver: str = Field("2captcha", alias="CAPTCHA_SOLVER")
    captcha_api_key: str = Field("chave-api-servico", alias="CAPTCHA_API_KEY")

    # Monitoring
    sentry_dsn: str = Field("chave-api-servico", alias="SENTRY_DSN")
    prometheus_port: int = Field(9090, alias="PROMETHEUS_PORT")
    grafana_port: int = Field(3000, alias="GRAFANA_PORT")
    alert_email: str = Field("alerts@your-company.com", alias="ALERT_EMAIL")
    slack_webhook_url: str = Field("chave-api-servico", alias="SLACK_WEBHOOK_URL")

    # Cloud GCP
    gcp_project_id: str = Field("your-gcp-project", alias="GCP_PROJECT_ID")
    gcp_region: str = Field("us-central1", alias="GCP_REGION")
    gcp_bucket_name: str = Field("crawler-legal-data", alias="GCP_BUCKET_NAME")
    gcs_credentials_path: str = Field("/path/to/credentials.json", alias="GCS_CREDENTIALS_PATH")

    # Cloud AWS
    aws_region: str = Field("us-east-1", alias="AWS_REGION")
    aws_access_key_id: str = Field("chave-api-servico", alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field("chave-api-servico", alias="AWS_SECRET_ACCESS_KEY")
    s3_bucket_name: str = Field("crawler-legal-data", alias="S3_BUCKET_NAME")

    # Dashboard
    streamlit_server_port: int = Field(8501, alias="STREAMLIT_SERVER_PORT")
    streamlit_server_address: str = Field("0.0.0.0", alias="STREAMLIT_SERVER_ADDRESS")
    dashboard_refresh_interval: int = Field(30, alias="DASHBOARD_REFRESH_INTERVAL")

    # Feature flags
    enable_opensearch: bool = Field(True, alias="ENABLE_OPENSEARCH")
    enable_mongodb: bool = Field(True, alias="ENABLE_MONGODB")

    sql_echo: bool = Field(False, alias="SQL_ECHO")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        populate_by_name = True

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            host=self.postgres_host,
            port=str(self.postgres_port),
            user=self.postgres_user,
            password=self.postgres_password,
            path=f"/{self.postgres_db}",
        )

    @property
    def mongodb_uri(self) -> str:
        return (
            f"mongodb://{self.mongodb_user}:{self.mongodb_password}"
            f"@{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_db}"
        )

    @property
    def redis_uri(self) -> str:
        return (
            f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        )

    @property
    def opensearch_url(self) -> str:
        return f"https://{self.opensearch_host}:{self.opensearch_port}"

    @validator("environment")
    def validate_environment(cls, value: str) -> str:
        allowed = {"development", "staging", "production", "test"}
        if value not in allowed:
            raise ValueError(f"ENVIRONMENT deve ser um dos valores: {allowed}")
        return value


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
