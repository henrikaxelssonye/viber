"""Configuration helpers for the Viber data platform."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional


@dataclass(frozen=True)
class AppConfig:
    """Application configuration loaded from environment variables."""

    environment: str
    log_level: str


@dataclass(frozen=True)
class FabricLakehouseConfig:
    """Configuration for connecting to a Fabric Lakehouse via OneLake."""

    workspace: Optional[str]
    lakehouse: Optional[str]
    table: Optional[str]
    path: Optional[str]
    endpoint: str
    tenant_id: Optional[str]
    client_id: Optional[str]
    client_secret: Optional[str]
    account_key: Optional[str]


def load_config() -> AppConfig:
    """Load configuration from environment variables with sensible defaults."""

    return AppConfig(
        environment=os.getenv("VIBER_ENV", "development"),
        log_level=os.getenv("VIBER_LOG_LEVEL", "INFO"),
    )


def load_fabric_lakehouse_config() -> FabricLakehouseConfig:
    """Load Fabric Lakehouse configuration from environment variables."""

    return FabricLakehouseConfig(
        workspace=os.getenv("VIBER_FABRIC_WORKSPACE"),
        lakehouse=os.getenv("VIBER_FABRIC_LAKEHOUSE"),
        table=os.getenv("VIBER_FABRIC_TABLE"),
        path=os.getenv("VIBER_FABRIC_PATH"),
        endpoint=os.getenv(
            "VIBER_FABRIC_ENDPOINT",
            "https://onelake.dfs.fabric.microsoft.com",
        ),
        tenant_id=os.getenv("VIBER_FABRIC_TENANT_ID"),
        client_id=os.getenv("VIBER_FABRIC_CLIENT_ID"),
        client_secret=os.getenv("VIBER_FABRIC_CLIENT_SECRET"),
        account_key=os.getenv("VIBER_FABRIC_ACCOUNT_KEY"),
    )
