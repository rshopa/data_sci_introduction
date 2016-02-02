-- filter/ self-join, for a smaller file

register ../myudfs.jar

load '../cse344-test-file' USING TextLoader as (line: chararray);

-- flatten as in problem 2
tmp = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

-- first filter
tmp_f = filter tmp by (subject matches '.*business.*');

-- remove duplicates
f = distinct tmp_f;

-- a copy of f list
f2 = foreach f GENERATE * as (subject2:chararray,predicate2:chararray,object2:chararray);

-- join (f.subject >-< f2.subject2)
j = JOIN f by subject, f2 by subject2;

-- remove duplicates
result = distinct j;

-- store
store result into '../tmp/finaloutput3_small' using PigStorage();