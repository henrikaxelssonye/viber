with users as (
    select *
    from {{ ref('stg_users') }}
)

select
    count(*) as total_users,
    count(distinct email) as unique_emails
from users
