with source as (

    select * from {{ source('synthea_raw', 'procedures') }}

)

select
    patient as patient_id,
    encounter as encounter_id,
    cast("START" as date) as procedure_date,
    code as procedure_code,
    description as procedure_description
from source
where patient is not null
