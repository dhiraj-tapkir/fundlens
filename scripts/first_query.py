import duckdb

con = duckdb.connect()

con.sql("""
    create view navs as
    select
        cast(scheme_code as integer) as scheme_code,
        nav_name,
        try_cast(nav as double) as nav,
        try_strptime(nav_date, '%d-%b-%Y')::date as nav_date
    from read_csv('data/nav_history_sample.txt',
        auto_detect = false, delim = ';', header = false, quote = '',
        null_padding = true, strict_mode = false,
        columns = {'scheme_code': 'VARCHAR', 'nav_name': 'VARCHAR',
                   'plan': 'VARCHAR', 'option': 'VARCHAR',
                   'isin_growth': 'VARCHAR', 'isin_reinvest': 'VARCHAR',
                   'nav': 'VARCHAR', 'nav_date': 'VARCHAR'})
    where regexp_matches(scheme_code, '^[0-9]+$')
""")

print("rows parsed:", con.sql("select count(*) from navs").fetchall()[0][0])

con.sql("""
    select
        nav_date,
        nav,
        lag(nav) over w as prev_nav,
        round(100 * (nav / lag(nav) over w - 1), 3) as daily_ret_pct
    from navs
    where scheme_code = 148921
    window w as (partition by scheme_code order by nav_date)
    order by nav_date
""").show()
