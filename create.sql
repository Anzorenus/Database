CREATE EXTENSION IF NOT EXISTS dblink;


DROP FUNCTION IF EXISTS create_db(text, text); 
CREATE FUNCTION create_db(dname text, username text)
	RETURNS INTEGER AS
	$func$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dname) THEN
   			RAISE EXCEPTION 'Database "%" already created', dname;
			RETURN 0; 
		ELSE
   			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || current_database(), 'CREATE DATABASE ' || dname);
								
			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || dname,
				'DROP TABLE IF EXISTS Department CASCADE;
				CREATE TABLE Department(
					id INTEGER NOT NULL UNIQUE,
					name TEXT NOT NULL,
					phone TEXT NOT NULL,
					kpi INTEGER NOT NULL DEFAULT 0,
					PRIMARY KEY (id)
				);
				DROP TABLE IF EXISTS Bank CASCADE;
				CREATE TABLE Bank(
					id INTEGER NOT NULL UNIQUE,
					name TEXT NOT NULL,
					address TEXT NOT NULL,
					interest INTEGER NOT NULL,
					PRIMARY KEY (id)
				);
				DROP TABLE IF EXISTS Employee;
				CREATE TABLE Employee(
					id INTEGER NOT NULL UNIQUE,
					name TEXT NOT NULL,
					department INTEGER NOT NULL,
					mobile_phone TEXT NOT NULL,
					bank INTEGER NOT NULL,
					salary INTEGER NOT NULL,
					prize INTEGER NOT NULL,
					total_salary INTEGER NOT NULL,
					PRIMARY KEY (id),
					FOREIGN KEY (department) REFERENCES Department(id) ON DELETE CASCADE,
					FOREIGN KEY (bank) REFERENCES Bank(id) ON DELETE CASCADE
				);
				CREATE INDEX mobile_phone ON Employee (mobile_phone);
				DROP FUNCTION IF EXISTS total_salary() CASCADE;
				CREATE OR REPLACE FUNCTION total_salary() 
				RETURNS TRIGGER AS 
				$$
				BEGIN	
					NEW.total_salary = NEW.salary+NEW.prize;
					RETURN NEW; 
				END;
				$$ 
				LANGUAGE plpgsql;
				DROP TRIGGER IF EXISTS total_salary on Employee;
				CREATE TRIGGER total_salary BEFORE INSERT OR UPDATE ON Employee
				FOR EACH ROW EXECUTE PROCEDURE total_salary();
				'
			);

			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || dname, 'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ' || username );
			RETURN 1;
		END IF;

	END
	$func$ 
	LANGUAGE plpgsql;

 
DROP FUNCTION IF EXISTS drop_db(text);
CREATE FUNCTION drop_db(dname text)
	RETURNS INTEGER AS
	$func$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dname) THEN
   			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || current_database(),
								'DROP DATABASE ' || quote_ident(dname));
			RETURN 1;			
		ELSE
			RAISE EXCEPTION 'Database "%" was not found', dname;
			RETURN 0; 
		END IF;
	END
	$func$ 
	LANGUAGE plpgsql;