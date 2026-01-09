"""Configuration helpers for the Viber data platform."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    """Application configuration loaded from environment variables."""

    environment: str
    log_level: str


def load_config() -> AppConfig:
    """Load configuration from environment variables with sensible defaults."""

    return AppConfig(
        environment=os.getenv("VIBER_ENV", "development"),
        log_level=os.getenv("VIBER_LOG_LEVEL", "INFO"),
    )
