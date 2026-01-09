"""Export Fabric Lakehouse tables or paths to local Parquet for dbt."""

from __future__ import annotations

import argparse
from pathlib import Path

import pyarrow.parquet as pq

from viber.config import load_fabric_lakehouse_config
from viber.lakehouse import FabricLakehouseReader


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", help="Lakehouse table name to export.")
    parser.add_argument("--path", help="Lakehouse Files/ path to export.")
    parser.add_argument(
        "--output",
        default="data/lakehouse/lakehouse.parquet",
        help="Output Parquet file path.",
    )
    parser.add_argument(
        "--output-type",
        choices=("pyarrow", "pandas"),
        default="pyarrow",
        help="Reader output type before writing parquet.",
    )
    args = parser.parse_args()
    if not args.table and not args.path:
        parser.error("Provide --table or --path to export data.")
    return args


def main() -> None:
    args = parse_args()
    config = load_fabric_lakehouse_config()
    reader = FabricLakehouseReader(config, output_type=args.output_type)
    if args.table:
        result = reader.read_table(args.table)
    else:
        result = reader.read_path(args.path)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if args.output_type == "pandas":
        result = result.to_arrow()
    pq.write_table(result, output_path)


if __name__ == "__main__":
    main()
