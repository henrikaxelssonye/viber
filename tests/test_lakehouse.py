from __future__ import annotations

from dataclasses import dataclass

import pytest

pa = pytest.importorskip("pyarrow")
pq = pytest.importorskip("pyarrow.parquet")

from viber.config import FabricLakehouseConfig
from viber.lakehouse import FabricLakehouseReader


@dataclass(frozen=True)
class FakePath:
    name: str
    is_directory: bool = False


class FakeDownload:
    def __init__(self, payload: bytes) -> None:
        self._payload = payload

    def readall(self) -> bytes:
        return self._payload


class FakeFileClient:
    def __init__(self, payload: bytes) -> None:
        self._payload = payload

    def download_file(self) -> FakeDownload:
        return FakeDownload(self._payload)


class FakeFileSystemClient:
    def __init__(self, payload: bytes, paths: list[FakePath]) -> None:
        self._payload = payload
        self._paths = paths

    def get_paths(self, path: str):
        return self._paths

    def get_file_client(self, file_path: str) -> FakeFileClient:
        return FakeFileClient(self._payload)


def _parquet_payload() -> bytes:
    table = pa.table({"name": ["alpha", "bravo"], "value": [1, 2]})
    sink = pa.BufferOutputStream()
    pq.write_table(table, sink)
    return sink.getvalue().to_pybytes()


def test_read_table_returns_pyarrow_table(monkeypatch):
    payload = _parquet_payload()
    fake_fs = FakeFileSystemClient(payload, [FakePath("lake/Tables/sales/part-0.parquet")])

    config = FabricLakehouseConfig(
        workspace="workspace",
        lakehouse="lake",
        table="sales",
        path=None,
        endpoint="https://onelake.dfs.fabric.microsoft.com",
        tenant_id=None,
        client_id=None,
        client_secret=None,
        account_key="account-key",
    )
    reader = FabricLakehouseReader(config, output_type="pyarrow")
    monkeypatch.setattr(reader, "_get_filesystem_client", lambda: fake_fs)

    table = reader.read_table()

    assert isinstance(table, pa.Table)
    assert table.column_names == ["name", "value"]
    assert table.to_pydict()["value"] == [1, 2]


def test_read_table_returns_pandas_frame(monkeypatch):
    payload = _parquet_payload()
    fake_fs = FakeFileSystemClient(payload, [FakePath("lake/Tables/sales/part-0.parquet")])

    config = FabricLakehouseConfig(
        workspace="workspace",
        lakehouse="lake",
        table="sales",
        path=None,
        endpoint="https://onelake.dfs.fabric.microsoft.com",
        tenant_id=None,
        client_id=None,
        client_secret=None,
        account_key="account-key",
    )
    reader = FabricLakehouseReader(config, output_type="pandas")
    monkeypatch.setattr(reader, "_get_filesystem_client", lambda: fake_fs)

    frame = reader.read_table()

    assert list(frame.columns) == ["name", "value"]
    assert frame["value"].tolist() == [1, 2]
