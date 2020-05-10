CREATE TABLE coronavirus (
  id int(11) NOT NULL AUTO_INCREMENT,
  created_at datetime(6) DEFAULT NULL,
  updated_at datetime(6) DEFAULT NULL,
  country_id varchar(100) DEFAULT NULL,
  region_id varchar(100) DEFAULT NULL,
  subregion_id varchar(100) DEFAULT NULL,
  date varchar(20) DEFAULT NULL,
  today_confirmed int(10) unsigned DEFAULT NULL,
  today_deaths int(10) unsigned DEFAULT NULL,
  today_recovered int(10) unsigned DEFAULT NULL,
  today_open_case int(10) unsigned DEFAULT NULL,
  today_new_confirmed int(10) unsigned DEFAULT NULL,
  today_new_deaths int(10) unsigned DEFAULT NULL,
  today_new_recovered int(10) unsigned DEFAULT NULL,
  today_new_open_case int(10) unsigned DEFAULT NULL,
  yesterday_confirmed int(10) unsigned DEFAULT NULL,
  yesterday_deaths int(10) unsigned DEFAULT NULL,
  yesterday_recovered int(10) unsigned DEFAULT NULL,
  yesterday_open_case int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (id)
)
;


CREATE TABLE coronavirus_countries (
  created_at datetime(6) DEFAULT NULL,
  updated_at datetime(6) DEFAULT NULL,
  country_id varchar(100) NOT NULL,
  country_name varchar(100) DEFAULT NULL,
  country_name_es varchar(100) DEFAULT NULL,
  continent varchar(100) DEFAULT NULL,
  rank_by_continent int(10) unsigned DEFAULT NULL,
  rank_all int(10) unsigned DEFAULT NULL,
  population bigint(20) unsigned DEFAULT NULL,
  confirmed int(10) unsigned DEFAULT NULL,
  death int(10) unsigned DEFAULT NULL,
  recovered int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (country_id)
);


CREATE TABLE coronavirus_regions (
  created_at datetime(6) DEFAULT NULL,
  updated_at datetime(6) DEFAULT NULL,
  country_id varchar(100) NOT NULL,
  region_id varchar(100) NOT NULL,
  region_name varchar(100) DEFAULT NULL,
  region_name_es varchar(100) DEFAULT NULL,
  PRIMARY KEY (region_id)
);


CREATE TABLE coronavirus_subregions (
  created_at datetime(6) DEFAULT NULL,
  updated_at datetime(6) DEFAULT NULL,
  region_id varchar(100) NOT NULL,
  subregion_id varchar(100) NOT NULL,
  subregion_name varchar(100) DEFAULT NULL,
  subregion_name_es varchar(100) DEFAULT NULL,
  PRIMARY KEY (subregion_id)
);


CREATE OR REPLACE VIEW coronavirus_geography AS
select
    c.continent AS continent,
    c.country_id AS country_id,
    c.country_name AS country_name,
    c.country_name_es AS country_name_es,
    r.region_id AS region_id,
    r.region_name AS region_name,
    r.region_name_es AS region_name_es,
    c.rank_all AS rank_all,
    c.rank_by_continent AS rank_by_continent,
    c.population AS population
from
    coronavirus_countries c
		inner join
	coronavirus_regions r on c.country_id = r.country_id



CREATE DEFINER=coronavirus@localhost PROCEDURE coronavirus.update_countries_ranks()
BEGIN
	DECLARE 
		v_continent CHAR(100);

	DECLARE cur1 CURSOR FOR
		select distinct
			continent
		from
			countries c2;

	update
		coronavirus_countries 
			left join
		(
			select
				ss.country_id ,
				sum(ss.today_confirmed ) as confirmed,
				sum(ss.today_deaths ) as deaths,
				sum(ss.today_recovered ) as recovered
			from
				coronavirus_temp ss
			group by 1
		)ss_agg
			on
				coronavirus_countries.country_id = ss_agg.country_id
	set
		coronavirus_countries.confirmed = ss_agg.confirmed,
		coronavirus_countries.death = ss_agg.deaths,
		coronavirus_countries.recovered = ss_agg.recovered,
		updated_at = now();

	truncate table coronavirus_countries_temp;
	
	insert into coronavirus_countries_temp
		select
			country_id,
			continent,
			@curRank := @curRank + 1 AS rank
		from
			coronavirus_countries c, (SELECT @curRank := 0) r
		order by confirmed desc;
	
	update
		coronavirus_countries 
			left join
		coronavirus_countries_temp ss_rank
			on
				coronavirus_countries.country_id = ss_rank.country_id 
	set
		coronavirus_countries.rank_all = ss_rank.rank;


	OPEN cur1;

	read_loop: LOOP
	    FETCH cur1
	    INTO
	    	v_continent
		;


		truncate table coronavirus_countries_temp;
		
		insert into coronavirus_countries_temp
			select
				country_id,
				continent,
				@curRank := @curRank + 1 AS rank
			from
				coronavirus_countries c, (SELECT @curRank := 0) r
			where
				continent = v_continent
			order by confirmed desc;

		update
			coronavirus_countries
				inner join
			coronavirus_countries_temp ss_rank
				on
					coronavirus_countries.country_id = ss_rank.country_id
		set
			coronavirus_countries.rank_by_continent = ss_rank.rank
		;

		commit;
	END LOOP;

	CLOSE cur1;
END
