register ../myudfs.jar

-- load the test file into Pig
raw = LOAD '../cse344-test-file' USING TextLoader as (line:chararray);
-- for the bigger file
-- raw = LOAD '../btc-2010-chunk-000' USING TextLoader as (line:chararray);

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

-- The result will look like this:
-- subject	predicate	object
-- <A,		pre1,		O1>
-- <B,		pre3,		O2>
-- <B,		pre3,		O3>
-- <C,		pre2,		O1>
-- ...

--group the n-triples by subject column
subjects = group ntriples by (subject) PARALLEL 50;

-- the result will be:
-- 	<A, {<A, pre1, O1>}>
-- 	<B, {<B, pre3, O2>, <B, pre3, O3>,<B, pre1, O1>}>
-- 	<C, {<C, pre2, O1>, <C, pre2, O3>, <C, pre3, O4>}>
-- 	...

-- flatten the objects out and count the number of tuples associated with each object
count_subj = foreach subjects generate flatten($0), COUNT($1) as count PARALLEL 50;

-- 	subject count
-- 	<A,	1>
-- 	<B,	3>
-- 	<C,	3>
-- 	<D,	2>
-- 	...

--group by count
count_count = group count_subj by (count);

-- 	<1, {<A, 1>, <E, 1>}>
-- 	<2, {<D, 2>}>
-- 	<3, {<B, 3>, <C, 3>}>
-- 	...

-- count the number of subjects associated with each particular count
histogram = foreach count_count generate $0 as x, COUNT($1) as y PARALLEL 50;

--	 x  y
--	<1, 2>
--	<2, 1>
--	<3, 2>
--	...

-- store histogram 
store histogram into '../tmp/finaloutput2' using PigStorage();
