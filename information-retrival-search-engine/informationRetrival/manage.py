#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "informationRetrival.settings")

    from django.core.management import execute_from_command_line

    os.system("bert-serving-start -model_dir /Users/yma/Downloads/wwm_uncased_L-24_H-1024_A-16 -num_worker=2")
    execute_from_command_line(sys.argv)
