with source as (
    select *
    from {{ ref('sample_users') }}
),

renamed as (
    select
        cast(user_id as integer) as user_id,
        cast(name as string) as name,
        cast(email as string) as email,
        cast(created_at as date) as created_at
    from source
)

select *
from renamed
