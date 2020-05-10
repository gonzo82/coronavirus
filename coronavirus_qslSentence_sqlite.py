DELETE_STATEMENT = 'delete from coronavirus.coronavirus where date >= %s'

INSERT_STATEMENT = 'INSERT INTO coronavirus ( ' \
                   'country_id, region_id, subregion_id, date, ' \
                   'today_confirmed, today_deaths, today_recovered, today_open_case, ' \
                   'today_new_confirmed, today_new_deaths, today_new_recovered, today_new_open_case, ' \
                   'yesterday_confirmed, yesterday_deaths, yesterday_recovered, yesterday_open_case) ' \
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

INSERT_COUNTRY_STATEMENT = 'insert into coronavirus.coronavirus_countries ' \
                           '(country_id, country_name, country_name_es) ' \
                           'values (%s, %s, %s) ' \
                           'on duplicate key update ' \
                           'created_at = now(), ' \
                           'updated_at = now(), ' \
                           'country_name = %s, ' \
                           'country_name_es = %s'

INSERT_REGION_STATEMENT = 'insert into coronavirus.coronavirus_regions ' \
                          '(country_id, region_id, region_name, region_name_es) ' \
                          'values (%s, %s, %s, %s) ' \
                          'on duplicate key update ' \
                          'created_at = now(), ' \
                          'updated_at = now(), ' \
                          'region_name = %s, ' \
                          'region_name_es = %s'

INSERT_SUBREGION_STATEMENT = 'insert into coronavirus.coronavirus_subregions ' \
                             '(region_id, subregion_id, subregion_name, subregion_name_es) ' \
                             'values (%s, %s, %s, %s) ' \
                             'on duplicate key update ' \
                             'subregion_name = %s, ' \
                             'subregion_name_es = %s'

INSERT_NULL_SUBREGIONS = 'insert into coronavirus_subregions ' \
                         '(region_id, subregion_id, subregion_name, subregion_name_es) ' \
                         'select csr.region_id, csr.region_id, csr.region_name , csr.region_name_es ' \
                         'from coronavirus_regions csr ' \
                         'where not exists (select * from coronavirus_subregions css where csr.region_id = css.region_id)'

INSERT_NULL_REGIONS = 'insert into coronavirus_regions ' \
                      '(country_id, region_id, region_name, region_name_es) ' \
                      'select cc.country_id, cc.country_id, cc.country_name , cc.country_name_es ' \
                      'from coronavirus_countries cc ' \
                      'where not exists (select * from coronavirus_regions csr where cc.country_id = csr.country_id)'

SELECT_CORONAVIRUS_STATEMENT = 'select ' \
                               'country_id, region_id, date, ' \
                               'today_confirmed, today_deaths, today_recovered, today_open_case, ' \
                               'today_new_confirmed, today_new_deaths, today_new_recovered, today_new_open_case, ' \
                               'yesterday_confirmed, yesterday_deaths, yesterday_recovered, yesterday_open_case ' \
                               'from coronavirus ' \
                               'where ' \
                               'today_confirmed <> 0 or today_deaths <> 0 or ' \
                               'today_recovered <> 0 or today_open_case <> 0 ' \
                               'or today_new_confirmed <> 0 or today_new_deaths <> 0 ' \
                               'or today_new_recovered <> 0 or today_new_open_case <> 0 ' \
                               'or yesterday_confirmed <> 0 or yesterday_deaths <> 0 ' \
                               'or yesterday_recovered <> 0 or yesterday_open_case <> 0 ' \
                               'order by country_id, region_id, subregion_id, date'

SELECT_GEOGRAPHY_STATEMENT = 'select * from coronavirus_geography ' \
                             'order by country_id, region_id'
