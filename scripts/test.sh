#!/bin/sh -e
set -x

pytest developing_tools --cov-report html
