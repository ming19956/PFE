#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "informationRetrival.settings")

    from django.core.management import execute_from_command_line

    os.system("bert-serving-start -model_dir /Users/yma/Downloads/wwm_uncased_L-12_H-768_A-12 -num_worker=2")
    execute_from_command_line(sys.argv)


## Download the document with the link : storage/googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip