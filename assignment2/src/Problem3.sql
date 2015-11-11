-- Problem 3: Working with a Term-Document Matrix

-- Problem 3(h):
-- Select output

	.output '../similarity_matrix.txt'

-- Answer:

	SELECT sum(f1.count * f2.count)
	FROM
		Frequency as f1
	JOIN
		Frequency as f2
	ON f1.term = f2.term
	WHERE
		f1.docid = '10080_txt_crude'
		AND f2.docid = '17035_txt_earn';


-- End problem 3(h)


-- Problem 3(i):
-- Select output

	.output '../keyword_search.txt'

-- Unlike the solution hint, proposed in the assignment, the maximum similarity score
-- could be found without computing the similarity of two identical matrices,
-- expanded by adding 'query document'. The proper value of the maximum similarity
-- is also correct when the first matrix consists of just one 'query document'.

-- Answer 1:

	SELECT max(Sim)
	FROM
	(
		SELECT sum(f1.count * f2.count) as Sim
		FROM
			(SELECT 'query' as docid, 'washington' as term, 1 as count
			UNION
			SELECT 'query' as docid, 'taxes' as term, 1 as count
			UNION
			SELECT 'query' as docid, 'treasury' as term, 1 as count) as f1
		JOIN
			(SELECT * FROM Frequency
			UNION
			SELECT 'query' as docid, 'washington' as term, 1 as count
			UNION
			SELECT 'query' as docid, 'taxes' as term, 1 as count
			UNION
			SELECT 'query' as docid, 'treasury' as term, 1 as count) as f2
		ON f1.term = f2.term
		GROUP BY f2.docid
	);

-- However, to compute the similarity matrix correctly, two BIG ones are mandatory,
-- therefore for the purpose of economy a view could be created:

-- Answer 2:

	CREATE VIEW Freq_extended AS
	SELECT * FROM Frequency
	UNION
	SELECT 'query' as docid, 'washington' as term, 1 as count
	UNION
	SELECT 'query' as docid, 'taxes' as term, 1 as count
	UNION
	SELECT 'query' as docid, 'treasury' as term, 1 as count;


	SELECT max(Sim)
	FROM
	(
		SELECT sum(f1.count * f2.count) as Sim
		FROM
			Freq_extended AS f1
		JOIN
			Freq_extended AS f2
		ON f1.term = f2.term
		WHERE f1.docid = 'query'
		GROUP BY f2.docid
	);

-- End problem 3(i)
