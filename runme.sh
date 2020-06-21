#!/bin/bash
# remove logfile and start scraping in the background

rm nohup.out
nohup python3 scrape_yobit.py &
cat nohup.out