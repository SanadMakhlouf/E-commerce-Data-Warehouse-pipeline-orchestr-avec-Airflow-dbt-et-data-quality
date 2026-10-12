-- Echoue si la table de faits est vide apres transformation.
select 1
where (select count(*) from {{ ref('fact_sales') }}) = 0
