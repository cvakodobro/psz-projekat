select block, count(*) as number from db.realestate where add_type = 's' and location='Beograd' group by block order by number desc limit 10
select block, count(*) as number from db.realestate where add_type = 'r' and location='Beograd' group by block order by number desc limit 10
select block, count(*) as number from db.realestate where location='Beograd' group by block order by number desc limit 10

select category, count(*) from
	(SELECT size,
	CASE
		WHEN size <= 35 THEN 'Less than 35'
		WHEN size > 35 and size <= 50 THEN '36 - 50'
		WHEN size > 50 and size <= 65 THEN '51 - 65'
		WHEN size > 65 and size <= 80 THEN '66 - 80'
		WHEN size > 80 and size <= 95 THEN '81 - 95'
		WHEN size > 95 and size <= 110 THEN '96 - 110'
		WHEN size > 110 THEN 'More than 110'
	ELSE 'No size data'
	END AS category
	FROM db.realestate) a
group by category


select category, count(*) from
	(SELECT year,
	CASE
		WHEN year < 1950 THEN 'Before 1951'
		WHEN year > 1950 and year <= 1960 THEN '1951 - 1960'
		WHEN year > 1960 and year <= 1970 THEN '1961 - 1970'
		WHEN year > 1970 and year <= 1980 THEN '1971 - 1980'
		WHEN year > 1980 and year <= 1990 THEN '1981 - 1990'
		WHEN year > 1990 and year <= 2000 THEN '1991 - 2000'
		WHEN year > 2000 and year <= 2010 THEN '2001 - 2010'
		WHEN year > 2010 and year <= 2020 THEN '2011 - 2020'
		WHEN year > 2020 THEN 'Aftrer 2021 (under construction)'
	ELSE 'No year data'
	END AS category
	FROM db.realestate) a
group by category



select location, sell, rent, sell/rent, sell+rent as total from
	(select a.location as location, a.sell as sell, b.rent as rent from 
		(select location, count(*) as sell from db.realestate where add_type='s' group by location) as a
		left join
		(select location, count(*) as rent from db.realestate where add_type='r' group by location) as b 
		on a.location=b.location
	) a
where location in 
	(select location from 
		(select location, count(*) as number from db.realestate group by location order by number desc limit 5) a
	)
	
	
select category, count(*) from
	(SELECT price,
	CASE
		WHEN price < 49999 THEN 'Less then 49,999'
		WHEN price >= 50000 and price <= 99999 THEN '50,000 - 99,999'
		WHEN price >=100000 and price <= 149999 THEN '100,000 - 149,999'
		WHEN price >= 150000 and price <= 199999 THEN '150,000 - 199,999'
		WHEN price >=200000 THEN 'Greater then 200,000'
	ELSE 'No price data'
	END AS category
	FROM db.realestate where add_type='s') a
group by category



select count(*) from db.realestate where parking = 1 and add_type ='s' and location='Beograd'
union
select count(*) from db.realestate where add_type ='s' and location='Beograd'