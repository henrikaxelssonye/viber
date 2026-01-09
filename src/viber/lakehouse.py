"""Fabric Lakehouse connector helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
import pyarrow as pa
import pyarrow.parquet as pq

from viber.config import FabricLakehouseConfig

OutputType = Literal["pyarrow", "pandas"]


@dataclass(frozen=True)
class LakehousePaths:
    """Resolved paths inside a Fabric Lakehouse."""

    table_prefix: str
    file_prefix: str


class FabricLakehouseReader:
    """Read data from Fabric Lakehouse via OneLake (ADLS Gen2-compatible) endpoints."""

    def __init__(self, config: FabricLakehouseConfig, output_type: OutputType = "pyarrow") -> None:
        self._config = config
        self._output_type = output_type
        self._paths = self._resolve_paths(config)

    def read_table(self, table_name: Optional[str] = None):
        """Read a table from the Lakehouse Tables area."""

        table = table_name or self._config.table
        if not table:
            raise ValueError("Table name is required to read from the Lakehouse.")
        path = f"{self._paths.table_prefix}/{table}"
        return self._read_parquet_dataset(path)

    def read_path(self, relative_path: Optional[str] = None):
        """Read a file or folder from the Lakehouse Files area."""

        path_value = relative_path or self._config.path
        if not path_value:
            raise ValueError("Path is required to read from the Lakehouse.")
        normalized = path_value.lstrip("/")
        path = f"{self._paths.file_prefix}/{normalized}"
        return self._read_parquet_dataset(path)

    def _resolve_paths(self, config: FabricLakehouseConfig) -> LakehousePaths:
        if not config.workspace or not config.lakehouse:
            raise ValueError("Workspace and lakehouse must be configured.")
        base = config.lakehouse.rstrip("/")
        return LakehousePaths(
            table_prefix=f"{base}/Tables",
            file_prefix=f"{base}/Files",
        )

    def _read_parquet_dataset(self, path: str):
        filesystem = self._get_filesystem_client()
        parquet_paths = self._list_parquet_files(filesystem, path)
        tables = [self._read_parquet_file(filesystem, file_path) for file_path in parquet_paths]
        combined = pa.concat_tables(tables)
        if self._output_type == "pandas":
            return combined.to_pandas()
        return combined

    def _read_parquet_file(self, filesystem, file_path: str) -> pa.Table:
        file_client = filesystem.get_file_client(file_path)
        stream = file_client.download_file()
        data = stream.readall()
        buffer = pa.BufferReader(data)
        return pq.read_table(buffer)

    def _list_parquet_files(self, filesystem, path: str) -> list[str]:
        paths = list(filesystem.get_paths(path=path))
        if not paths and path.endswith(".parquet"):
            return [path]
        files = [
            entry.name
            for entry in paths
            if not entry.is_directory and entry.name.endswith(".parquet")
        ]
        if not files and path.endswith(".parquet"):
            return [path]
        if not files:
            raise FileNotFoundError(f"No parquet files found at {path}.")
        return files

    def _get_filesystem_client(self):
        service_client = self._get_service_client()
        return service_client.get_file_system_client(self._config.workspace)

    def _get_service_client(self) -> DataLakeServiceClient:
        if self._config.account_key:
            return DataLakeServiceClient(
                account_url=self._config.endpoint,
                credential=self._config.account_key,
            )
        credential = self._get_credential()
        return DataLakeServiceClient(account_url=self._config.endpoint, credential=credential)

    def _get_credential(self):
        if self._config.client_id and self._config.client_secret and self._config.tenant_id:
            return ClientSecretCredential(
                tenant_id=self._config.tenant_id,
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
            )
        return DefaultAzureCredential(exclude_interactive_browser_credential=True)
