CREATE TABLE boba AS
    SELECT 'Black Milk Tea' AS name, '100%' AS sweetness, 'Regular' AS ice, 23 AS pieces UNION
    SELECT 'Wintermelon Milk Tea', '50%', 'Light', 22 UNION
    SELECT '61A Special Milk Tea', '100%', 'Extra', 25 UNION
    SELECT 'Wintermelon Milk Tea', '75%', 'Light', 23 UNION
    SELECT 'Thanos Milk Tea', '50%', 'Regular', 12 UNION
    SELECT '61A Special Milk Tea', '75%', 'Regular', 27 UNION
    SELECT '61A Special Milk Tea', '75%', 'Extra', 24 UNION
    SELECT 'Black Milk Tea', '0%', 'Light', 24 UNION
    SELECT 'Thanos Milk Tea', '50%', 'Regular', 12 UNION
    SELECT 'Wintermelon Milk Tea', '25%', 'Regular', 22 UNION
    SELECT 'Black Milk Tea', '100%', 'Regular', 24;

CREATE TABLE orders AS
    SELECT 'Rabia' AS name, 'Black Milk Tea' AS item, 'Regular' AS ice UNION
    SELECT 'Richard', '61A Special Milk Tea', 'Light' UNION
    SELECT 'Rebecca', 'Thanos Milk Tea', 'Extra' UNION
    SELECT 'Sriya', 'Black Milk Tea', 'Regular';

CREATE TABLE menu AS
    SELECT 'Black Milk Tea' AS item, 5 AS price UNION
    SELECT 'Wintermelon Milk Tea', 6 UNION
    SELECT 'Thanos Milk Tea', 7 UNION
    SELECT '61A Special Milk Tea', 8;

-- Q1: Write a query that gives back a two-column table
-- consisting of the name and ice columns in the table boba.
CREATE TABLE q1 AS
SELECT 'YOUR CODE HERE';

-- Q2: Write a query that gives a table with the same columns as boba
-- but only includes drinks with a sweetness of 100% and over 20 pieces.
-- Be careful: The sweetness column contains strings!
CREATE TABLE q2 AS
SELECT 'YOUR CODE HERE';

-- Q3: Create a table with the same columns as boba but now has double the amount of pieces of boba
-- in every drink and sort by the amount of pieces. Rename the doubled pieces column to doubled_pieces.
CREATE TABLE q3 AS
SELECT 'YOUR CODE HERE';

-- Q4: Write a query that returns a table identical to the orders table,
-- but also includes the price for the item ordered.
-- Challenge: Do this 2 ways (with implicit and explicit join)
CREATE TABLE q4 AS
SELECT 'YOUR CODE HERE';

-- Q5: Write a query that returns the names of people who have the same order
-- (they ordered the same item from the menu).
-- Call the first column "person1" and the second column "person2"
-- You should not have duplicate pairs, and you should not match a person with themselves!
CREATE TABLE q5 AS
SELECT 'YOUR CODE HERE';
