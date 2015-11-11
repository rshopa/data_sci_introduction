-- Problem 2: Matrix Multiplication in SQL

-- Problem 2 (g):

-- To display all the pairs of elements from both matrices that need to be multiplied
-- with corresponding indices the next code should be applied:
--
-- SELECT a.row_num, b.col_num, a.value, b.value
-- FROM a,b WHERE a.col_num = b.row_num ORDER BY a.row_num,b.col_num;
-- 
-- To calculate the multiplications a.value, b.value should be replaced with
-- (a.value * b.value)

-- to calculate sum of multiplications which are the corresponding values
-- of a * b matrix - sum(a.value * b.value) is obvious, but 
-- GROUP BY is needed instead of ORDER BY:
--
-- SELECT a.row_num,b.col_num,sum(a.value * b.value)
-- FROM a,b WHERE a.col_num = b.row_num GROUP BY a.row_num,b.col_num;
--
-- It may be even simplified in case of this assignment, but I will use longer code
-- just to clear up the idea of solution mechanism.


-- Select output

	.output '../multiply.txt'

-- Answer:

	SELECT answer
	FROM
	(
		SELECT a.row_num,b.col_num,sum(a.value * b.value) as answer
		FROM a,b
		WHERE a.col_num = b.row_num
		GROUP BY a.row_num,b.col_num
		HAVING a.row_num = 2 AND b.col_num = 3
	);

-- End problem 2(g)