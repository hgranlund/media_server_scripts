#!/bin/bash

cat /dev/null > /var/log/cron_subtitels

##find /mnt/* -type f -regex '.*\.\(mkv\|mp4\|wmv\|flv\|webm\|mov\)' -exec /usr/local/bin/subliminal  -l en no  --log-file /home/simenhg/.log/cron_subtitels.log -- '{}' > /home/simenhg/.log/cron_test.txt \;
find /mnt/* -type f -regex '.*\.\(mkv\|mp4\|wmv\|flv\|webm\|mov\)' -exec /usr/local/bin/subliminal  -l en no  -- '{}' > /home/simenhg/.log/cron_test.txt \;

