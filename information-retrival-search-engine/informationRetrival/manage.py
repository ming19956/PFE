#!/usr/bin/env python
import os
import sys
from thread import  MyThread

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "informationRetrival.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    p = MyThread('子线程1')
    p.run()
    p.join()






## Download the document with the link : storage/googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip