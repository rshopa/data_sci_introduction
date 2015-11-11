-- Problem 1: Inspecting the Reuters Dataset; Relational Algebra

-- Problem 1(a):
-- Select output

	.output '../select.txt'

-- Answer:

	SELECT COUNT(docid)
	FROM Frequency
	WHERE docid='10398_txt_earn';

-- End problem 1(a)


-- Problem 1(b):
-- Select output

	.output '../select_project.txt'

-- Answer:

	SELECT COUNT(term)
	FROM Frequency
	WHERE docid = '10398_txt_earn'
	AND count = 1;

-- End problem 1(b)


-- Problem 1(c):
-- Select output

	.output '../union.txt'

-- Answer:

	SELECT COUNT(*) FROM
	(
		SELECT term FROM Frequency
		WHERE docid = '10398_txt_earn' AND count = 1
		UNION
		SELECT term FROM Frequency
		WHERE docid = '925_txt_trade' AND count = 1
	);

-- End problem 1(c)


-- Problem 1(d):
-- Select output

	.output '../count.txt'

-- Answer:

	SELECT COUNT(docid)
	FROM Frequency
	WHERE term = 'parliament';

-- End problem 1(d)


-- Problem 1(e):
-- Select output

	.output '../big_documents.txt'

-- Answer 1:

	SELECT COUNT(*)
	FROM
	(
		SELECT docid, sum(count) as S
		FROM Frequency
		GROUP BY docid
	)
	WHERE S>300;

-- Answer 2:

	SELECT COUNT(*)
	FROM
	(
		SELECT docid, sum(count)
		FROM Frequency
		GROUP BY docid
		HAVING sum(count) > 300
	);

-- End problem 1(e)


-- Problem 1(f):
-- Select output

	.output '../two_words.txt'

-- Answer:

	SELECT COUNT(*)
	FROM
		Frequency as A
	INNER JOIN
		Frequency as B
	ON A.docid = B.docid
		WHERE A.term = 'transactions'
		AND B.term = 'world';

-- End problem 1(f)