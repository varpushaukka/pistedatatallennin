run: bottle.py import-schema
	python pistesovellus.py

bottle.py:
	wget http://bottlepy.org/bottle.py

import-schema:
	psql pistedata < create_tables.sql
	touch import-schema

import-data: import-schema
	psql pistedata < add_test_data.sql
	touch import-data

clean-database:
	psql pistedata < drop_tables.sql
	rm -f import-schema import-data
