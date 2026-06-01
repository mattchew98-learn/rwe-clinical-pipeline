with source as (

    select * from {{ source('synthea_raw', 'patients') }}

)

select
    id as patient_id,
    cast(birthdate as date) as birth_date,
    cast(deathdate as date) as death_date,
    gender,
    race,
    ethnicity,
    city,
    state,
    zip
from source
where id is not null
qualify row_number() over (partition by id order by birthdate) = 1
