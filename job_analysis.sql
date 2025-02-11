-- Get the total number of job postings.
select count(*) as "Posting Count"
from jobs;

-- Get the total number of applicants.
select sum(num_applicants) as "Total Applicants"
from jobs;

-- What are the top 5 job titles with the highest number of job postings?
select job_title, count(*) as job_count
from jobs
group by job_title
order by job_count desc
limit 5;

-- What is the distribution of employment types for Data Scientist, Data Analyst, and Data Engineer roles based on the number of job postings?
select job_title, employment_type, count(*) Count
from jobs
where job_title in ("Data Scientist", "Data Analyst", "Data Engineer")
group by job_title,employment_type;

-- Which companies have the highest number of job postings, and how are the job postings distributed among the top 10 companies?
select company_name, count(*) as job_distribution
from jobs
group by company_name
order by job_distribution desc 
limit 10;

-- Which states have the highest number of job postings, and how are job opportunities distributed across different states?
select state, count(*) as job_count
from jobs
where state <> ""
group by state
order by job_count desc;


-- What is the average salary for different seniority levels among Data Scientist, Data Analyst, and Data Engineer roles?
with averagesalaries as (
    select seniority_level,job_title, (min_salary + max_salary) / 2 as average_salary
    from jobs
)

select seniority_level, avg(average_salary) as avg_salary_by_seniority
from averagesalaries
where job_title in ("Data Scientist", "Data Analyst", "Data Engineer")
group by seniority_level;





