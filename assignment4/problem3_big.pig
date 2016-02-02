-- filter/ self-join, for a bigger file

register ../myudfs.jar

load '../btc-2010-chunk-000' USING TextLoader as (line: chararray);

-- flatten as in problem 2
tmp = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray) PARALLEL 50;

-- first filter
tmp_f = filter tmp by (subject matches '.*rdfabout\\.com.*') PARALLEL 50;

-- remove duplicates
f = distinct tmp_f;

-- a copy of f list
f2 = foreach f GENERATE * as (subject2:chararray,predicate2:chararray,object2:chararray) PARALLEL 50;

-- join (f.object >-< f2.subject2)
j = JOIN f by object, f2 by subject2 PARALLEL 50;

-- remove duplicates
result = distinct j;

-- store
store result into '../tmp/finaloutput3_big' using PigStorage();