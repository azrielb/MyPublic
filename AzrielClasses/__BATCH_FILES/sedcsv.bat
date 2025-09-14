@echo off
echo Start Time: %time%
sed -i -E "s/ 00:00:00//g" *.csv
sed -i -E "s/( [0-9][0-9]:[0-9][0-9]):[0-9][0-9](\.[0-9]+)?,/\1,/g" *.csv
sed -i -E "s/( \d\d:\d\d)\.\d+,/\1,/g" *.csv
sed -i -E "s/,([0-9][0-9]+)\/([0-9][0-9]+)\/([0-9][0-9][0-9][0-9])(,| )/,\3-\2-\1\4/g" *.csv
setlocal enabledelayedexpansion
set count=1
:repeat	
sed -i -E 's/,"(-?[0-9]+),([0-9.]+)",/,\1\2,/g' *.csv
sed -i -E 's/,"(-?[0-9]+),([0-9.]+),([0-9.]+)",/,\1\2\3,/g' *.csv
sed -i -E 's/(,-?[0-9]+)\\.0+,/\1,/g' *.csv
sed -i -E 's/(,-?[0-9]+\\.[0-9]*[1-9])0+,/\1,/g' *.csv
set /a count+=1
if !count! LEQ 3 goto repeat
echo Finish Time: %time%
