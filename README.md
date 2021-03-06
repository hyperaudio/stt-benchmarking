# stt-benchmarking
a place to discuss and create an independent speech-to-text benchmarking tool.

## Design principles
- Benchmarking metrics will be measured in relation to a reference transcript and audio prepared by the client.   
- The tool should be language-agnostic: the client will create the reference in the language they require and test the tools.  
- The tool should require as little configuration as possible and depend on test data format as much as possible for deciding which evaluation metrics to compute. (R5)

## Installation
- `python3 -m venv venv`
- `pip install -r requirements.txt`
- `python -m spacy download en`


[TextAV STT-Benchmarking GDoc](https://docs.google.com/document/d/14BKrWuK4Wkqr_IYYU2OjBu1QrpwiLdj7XEKMn6tbC4U/edit)
