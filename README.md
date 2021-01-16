# PFE

Please install the 'Bert-as-service'

1.  pip install -U bert-serving-server bert-serving-client
2.  pip install tensorflow == 1.15.0
3.  Download the pre-trained bert model with the link : https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip
4.  To run the server service of the bert-as-service, Run the command in terminal : bert-serving-start -model_dir /Users/yma/Downloads/uncased_L-12_H-768_A-12 -num_worker=1 -port 8190 -port_out 8191
