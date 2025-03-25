-- DUMMY
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    employee_id INT,
    salary INT,
    department_id INT
);

INSERT INTO employees (employee_id, salary, department_id) VALUES
    (1, 7500, 80),
    (2, 8500, 80),
    (3, 9000, 80),
    (4, 5000, 80),
    (5, 6000, 90); 

DROP TABLE IF EXISTS bonuses;
CREATE TABLE bonuses (
    employee_id INT,
    bonus DECIMAL(10,2)
);

INSERT INTO bonuses (employee_id, bonus) VALUES
    (1, 100.00),
    (2, 200.00);

-- MERGE INTO
MERGE INTO bonuses D
USING (
    SELECT employee_id, salary, department_id
    FROM employees
    WHERE department_id = 80
) S
ON (D.employee_id = S.employee_id)
WHEN MATCHED AND (S.salary > 8000) THEN
    DELETE
WHEN MATCHED THEN
    UPDATE
        SET D.bonus = D.bonus + S.salary * 0.02
WHEN NOT MATCHED AND (S.salary <= 8000) THEN
    INSERT (D.employee_id, D.bonus)
    VALUES (S.employee_id, S.salary * 0.01);
