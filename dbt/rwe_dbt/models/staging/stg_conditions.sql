with source as (

    select * from {{ source('synthea_raw', 'conditions') }}

)

select
    patient as patient_id,
    encounter as encounter_id,
    cast("START" as date) as condition_start,
    cast(stop as date) as condition_stop,
    code as snomed_code,
    description as condition_description
from source
where patient is not null
