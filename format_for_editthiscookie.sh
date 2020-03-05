#! /bin/bash

# Filters out just the field we're interested in from Chrome's response, and also removes leading `.` characters from domain names (e.g. `.google.com` -> `google.com`, which is needed for EditThisCookie)
jq '.result.cookies' | sed -E 's/"\./"/'
