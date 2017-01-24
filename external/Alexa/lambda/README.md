# How to deploy lambda
1. Install request by doing:

    `pip install requests -t baby journal/external/Alexa/lambda`
2. Zip requests folders and Alexa_Lambda.py

    `zip babyjournal_lambda.zip -r requests* Alexa_Lambda.py`
3. Upload zip to Amazon Lambda website