#!/bin/bash

cd daily_report/Daily_Reports
mkdir dailyReport_$1$2
mv dailyReport_$1$2*.html dailyReport_$1$2/
mkdir dailyReport_$1$2/.static
cp echarts.js dailyReport_$1$2/.static/

cd ../pdf
mkdir pdf_$1$2
mv Daily\ Report\ on\ $1-$2-*.pdf pdf_$1$2/

echo $1-$2 moved!!