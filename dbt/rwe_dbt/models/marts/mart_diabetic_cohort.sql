-- Research-ready cohort: patients with a diabetes diagnosis, with their
-- demographics and a summary of conditions, procedures, and active meds.
-- This is the productionized version of the cohort deliverables shipped to
-- the biostatistics team. Adjust the condition filter to define new cohorts.
with diabetic_patients as (

    select distinct patient_id
    from {{ ref('stg_conditions') }}
    where lower(condition_description) like '%diabetes%'

),

history as (

    select * from {{ ref('int_patient_clinical_history') }}

)

select h.*
from history as h
inner join diabetic_patients as d on h.patient_id = d.patient_id
