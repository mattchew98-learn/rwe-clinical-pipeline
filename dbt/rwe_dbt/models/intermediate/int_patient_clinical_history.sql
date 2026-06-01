with patients as (

    select * from {{ ref('stg_patients') }}

),

condition_counts as (

    select
        patient_id,
        count(*) as condition_count
    from {{ ref('stg_conditions') }}
    group by patient_id

),

procedure_counts as (

    select
        patient_id,
        count(*) as procedure_count
    from {{ ref('stg_procedures') }}
    group by patient_id

),

medication_counts as (

    select
        patient_id,
        count(*) as medication_count,
        count_if(is_active) as active_medication_count
    from {{ ref('stg_medications') }}
    group by patient_id

)

select
    p.patient_id,
    p.birth_date,
    p.gender,
    p.race,
    p.ethnicity,
    p.state,
    coalesce(c.condition_count, 0) as condition_count,
    coalesce(pr.procedure_count, 0) as procedure_count,
    coalesce(m.medication_count, 0) as medication_count,
    coalesce(m.active_medication_count, 0) as active_medication_count
from patients as p
left join condition_counts as c on p.patient_id = c.patient_id
left join procedure_counts as pr on p.patient_id = pr.patient_id
left join medication_counts as m on p.patient_id = m.patient_id
