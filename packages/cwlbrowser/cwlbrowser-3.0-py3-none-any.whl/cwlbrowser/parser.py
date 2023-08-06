#!/usr/bin/env python3
import yaml
import sys

inputworkflow = str(sys.argv[1])
file = open(inputworkflow)
wf = yaml.safe_load(file)
print(wf)