with source as (

    select * from {{ source('synthea_raw', 'medications') }}

)

select
    patient as patient_id,
    encounter as encounter_id,
    cast("START" as date) as medication_start,
    cast(stop as date) as medication_stop,
    code as rxnorm_code,
    description as medication_description,
    stop is null as is_active
from source
where patient is not null
