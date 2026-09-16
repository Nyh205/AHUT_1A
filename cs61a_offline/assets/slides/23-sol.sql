-- Q1: Middle Manager
-- Consider the `records` table preloaded into 61A code.
-- Write a query that outputs a table with 3 columns:
-- The name of an employee (call this column "employee")
-- The name of the previous person's supervisor (call this column "middle_manager")
-- The name of the previous person's supervisor (e.g. the employee's supervisor's supervisor) (call this column "skip_manager")
-- Sort the output by employee, middle_manager, and skip_manager, breaking ties in that order.
-- Note that some people supervise themselves. You don't need to handle this case in a special way;
-- see the expected output table below, e.g. the row where all 3 columns contain Lana Lambda is fine.

-- EXPECTED OUTPUT TABLE:
-- employee|manager|skip_manager
-- Alyssa P Hacker|Ben Bitdiddle|Oliver Warbucks
-- Ben Bitdiddle|Oliver Warbucks|Oliver Warbucks
-- Cy D Fect|Ben Bitdiddle|Oliver Warbucks
-- Eben Scrooge|Oliver Warbucks|Oliver Warbucks
-- Lana Lambda|Lana Lambda|Lana Lambda
-- Lem E Tweakit|Ben Bitdiddle|Oliver Warbucks
-- Louis Reasoner|Alyssa P Hacker|Ben Bitdiddle
-- Oliver Warbucks|Oliver Warbucks|Oliver Warbucks
-- Robert Cratchet|Eben Scrooge|Oliver Warbucks
SELECT a.name AS employee, b.name AS middle_manager, c.name AS skip_manager
FROM records AS a
JOIN records AS b
JOIN records AS c
ON a.supervisor = b.name AND b.supervisor = c.name
ORDER BY employee, middle_manager, skip_manager;