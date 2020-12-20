DROP FUNCTION IF EXISTS clear_all_tables();
CREATE FUNCTION clear_all_tables()
	RETURNS void AS 
	$$ 
	DELETE FROM employee;
	DELETE FROM bank;
	DELETE FROM department;
	$$
LANGUAGE sql;


DROP FUNCTION IF EXISTS clear_department();
CREATE FUNCTION clear_department()
	RETURNS void AS 
	$$ 
	DELETE FROM department;
	$$	
LANGUAGE sql;


DROP FUNCTION IF EXISTS clear_bank();
CREATE FUNCTION clear_bank()
	RETURNS void AS 
	$$ 
	DELETE FROM bank;
	$$	
LANGUAGE sql;


DROP FUNCTION IF EXISTS clear_employee();
CREATE FUNCTION clear_employee()
	RETURNS void AS 
	$$ 
	DELETE FROM employee;
	$$	
LANGUAGE sql;


DROP FUNCTION IF EXISTS add_to_department(INTEGER, TEXT, TEXT, INTEGER);
CREATE FUNCTION add_to_department(new_id INTEGER, new_name TEXT, new_phone TEXT, new_kpi INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT d.id FROM department d WHERE d.id = new_id) THEN
			RAISE EXCEPTION 'Department with id % exists', new_id;
			RETURN 0;
		ELSE 
			INSERT INTO Department (id, name, phone, kpi)
			VALUES (new_id, new_name, new_phone, new_kpi);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS add_to_bank(INTEGER, TEXT, TEXT, INTEGER);
CREATE FUNCTION add_to_bank(new_id INTEGER, new_name TEXT, new_address TEXT, new_interest INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT b.id FROM bank b WHERE b.id = new_id) THEN
			RAISE EXCEPTION 'Bank with id % exists', new_id;
			RETURN 0;
		ELSE 
			INSERT INTO Bank (id, name, address, interest)
			VALUES (new_id, new_name, new_address, new_interest);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS add_to_employee(INTEGER, TEXT, INTEGER, TEXT, INTEGER, INTEGER, INTEGER, INTEGER);
CREATE FUNCTION add_to_employee(new_id INTEGER, new_name TEXT, new_department INTEGER, new_mobile_phone TEXT, new_bank INTEGER, new_salary INTEGER, new_prize INTEGER, new_total_salary INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF NOT EXISTS (SELECT d.id FROM department d WHERE d.id = new_department) THEN
			RAISE EXCEPTION 'Department % was not found', new_department;
			RETURN 0;
		ELSIF NOT EXISTS (SELECT b.id FROM bank b WHERE b.id = new_bank) THEN
			RAISE EXCEPTION 'Bank % was not found', new_bank;
			RETURN 0;						  
		ELSIF EXISTS (SELECT e.id FROM employee e WHERE e.id = new_id) THEN
			RAISE EXCEPTION 'Employee with id % already exists', new_id;
			RETURN 0;
		ELSE
			INSERT INTO employee (id, name, department, mobile_phone, bank, salary, prize, total_salary)
			VALUES (new_id, new_name, new_department, new_mobile_phone, new_bank, new_salary, new_prize, new_total_salary);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS search_employee_by_mobile_phone(TEXT);
CREATE FUNCTION search_employee_by_mobile_phone(new_mobile_phone TEXT)
	RETURNS TABLE (id INTEGER, name TEXT, department INTEGER, mobile_phone TEXT, bank INTEGER, salary INTEGER, prize INTEGER, total_salary INTEGER) AS
	$$
	BEGIN
		RETURN QUERY SELECT * FROM employee e WHERE e.mobile_phone = new_mobile_phone;
		IF NOT FOUND THEN
			RAISE EXCEPTION 'Employee with phone % was not found', new_mobile_phone;
		END IF;
		RETURN;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS update_employee(INTEGER, TEXT, INTEGER, TEXT, INTEGER, INTEGER, INTEGER, INTEGER);
CREATE FUNCTION update_employee(new_id INTEGER, new_name TEXT, new_department INTEGER, new_mobile_phone TEXT, new_bank INTEGER, new_salary INTEGER, new_prize INTEGER, new_total_salary INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT e.id FROM employee e WHERE e.id = new_id) THEN
			IF (new_department <> -1) AND NOT EXISTS (SELECT d.id FROM department d WHERE d.id = new_department) THEN
				RAISE EXCEPTION 'Department % was not found', new_department;
				RETURN 0;
			ELSIF (new_bank <> -1) AND NOT EXISTS (SELECT b.id FROM bank b WHERE b.id = new_bank) THEN
				RAISE EXCEPTION 'Bank % was not found', new_bank;
				RETURN 0;
			ELSE
				IF (new_name <> '') THEN
					UPDATE employee
					SET name = new_name
					WHERE id = new_id;
				END IF;
				IF (new_department <> -1) THEN 
					UPDATE employee 
					SET department = new_department
					WHERE id = new_id;
				END IF;
				IF (new_mobile_phone <> '') THEN
					UPDATE employee
					SET mobile_phone = new_mobile_phone
					WHERE id = new_id;
				END IF;
				IF (new_bank <> -1) THEN
					UPDATE employee 
					SET bank = new_bank
					WHERE id = new_id;
				END IF;
				IF (new_salary <> -1) THEN 
					UPDATE employee 
					SET salary = new_salary
					WHERE id = new_id;
				END IF;
				IF (new_prize <> -1) THEN 
					UPDATE employee 
					SET prize = new_prize
					WHERE id = new_id;
				END IF;
				RETURN 1;
			END IF;
		ELSE 
			RAISE EXCEPTION 'Employee with id % was not found', new_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_employee_by_mobile_phone(TEXT);
CREATE FUNCTION delete_employee_by_mobile_phone(new_mobile_phone TEXT)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT e.mobile_phone FROM employee e WHERE e.mobile_phone = new_mobile_phone) THEN
			DELETE FROM employee e WHERE e.mobile_phone = new_mobile_phone;
			RETURN 1;
		ELSE 
			RAISE EXCEPTION 'Employee with phone % was not found', new_mobile_phone;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_employee_by_id(INTEGER);
CREATE FUNCTION delete_employee_by_id(new_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT e.id FROM employee e WHERE e.id = new_id) THEN
			DELETE FROM employee e WHERE e.id = new_id;
			RETURN 1;
		ELSE 
			RAISE EXCEPTION 'Employee with id % was not found', new_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_department_by_id(INTEGER);
CREATE FUNCTION delete_department_by_id(new_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT d.id FROM department d WHERE d.id = new_id) THEN
			DELETE FROM department d WHERE d.id = new_id;
			RETURN 1;
		ELSE 
			RAISE EXCEPTION 'Department with id % was not found', new_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_bank_by_id(INTEGER);
CREATE FUNCTION delete_bank_by_id(new_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT b.id FROM bank b WHERE b.id = new_id) THEN
			DELETE FROM bank b WHERE b.id = new_id;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Bank with id % was not found', new_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS print_table_employee();
CREATE FUNCTION print_table_employee()
	RETURNS TABLE (id INTEGER, name TEXT, department INTEGER, mobile_phone TEXT, bank INTEGER, salary INTEGER, prize INTEGER, total_salary INTEGER) AS
	$$
	BEGIN
		RETURN QUERY SELECT * FROM employee;
		IF NOT FOUND THEN
			RAISE EXCEPTION 'Table is empty';
		END IF;
		RETURN;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS print_table_department();
CREATE FUNCTION print_table_department()
	RETURNS TABLE (id INTEGER, name TEXT, phone TEXT, kpi INTEGER) AS
	$$
	BEGIN
		RETURN QUERY SELECT * FROM department;
		IF NOT FOUND THEN
			RAISE EXCEPTION 'Table is empty';
		END IF;
		RETURN;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS print_table_bank();
CREATE FUNCTION print_table_bank()
	RETURNS TABLE (id INTEGER, name TEXT, address TEXT, interest INTEGER) AS
	$$
	BEGIN
		RETURN QUERY SELECT * FROM bank;
		IF NOT FOUND THEN
			RAISE EXCEPTION 'Table is empty';
		END IF;
		RETURN;
	END;
	$$
LANGUAGE plpgsql;