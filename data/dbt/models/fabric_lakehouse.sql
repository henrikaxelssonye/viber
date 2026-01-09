with lakehouse as (
    select *
    from read_parquet(
        '{{ env_var("VIBER_FABRIC_LOCAL_PARQUET", "data/lakehouse/lakehouse.parquet") }}'
    )
)

select *
from lakehouse
