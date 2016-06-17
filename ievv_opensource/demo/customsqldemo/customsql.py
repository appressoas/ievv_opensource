# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ievv_opensource.ievv_customsql import customsql_registry


class PersonCustomSql(customsql_registry.AbstractCustomSql):
    def initialize(self):
        self.execute_sql("""

            -- Add search_vector column to the Person model
            ALTER TABLE customsqldemo_person DROP COLUMN IF EXISTS search_vector;
            ALTER TABLE customsqldemo_person ADD COLUMN search_vector tsvector;

            -- Function used to create the search_vector value both in the trigger,
            -- and in the UPDATE statement (in recreate_data()).
            CREATE OR REPLACE FUNCTION customsqldemo_person_get_search_vector_value(param_table customsqldemo_person)
            RETURNS tsvector AS $$
            BEGIN
                RETURN setweight(to_tsvector(param_table.name), 'A') ||
                    setweight(to_tsvector(param_table.description), 'C');
            END
            $$ LANGUAGE plpgsql;

            -- Trigger function called on insert or update to keep the search_vector column
            -- in sync.
            CREATE OR REPLACE FUNCTION customsqldemo_person_set_search_vector() RETURNS trigger AS $$
            BEGIN
                NEW.search_vector := customsqldemo_person_get_search_vector_value(NEW);
              return NEW;
            END
            $$ LANGUAGE plpgsql;

            DROP TRIGGER IF EXISTS customsqldemo_person_set_search_vector_trigger ON customsqldemo_person;
            CREATE TRIGGER customsqldemo_person_set_search_vector_trigger BEFORE INSERT OR UPDATE
                ON customsqldemo_person FOR EACH ROW
                EXECUTE PROCEDURE customsqldemo_person_set_search_vector();
        """)

    def recreate_data(self):
        self.execute_sql("""
            UPDATE customsqldemo_person SET
                search_vector = customsqldemo_person_get_search_vector_value(customsqldemo_person);
        """)
