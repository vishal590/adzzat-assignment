#!/bin/sh
set -eu
mkdir -p /logs/verifier
printf '0\n' > /logs/verifier/reward.txt
if python /tests/grade.py /workspace; then
    printf '1\n' > /logs/verifier/reward.txt
fi
