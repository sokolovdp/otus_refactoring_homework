# CodeAnalysator

**codea_analysator.py** was done as home work to refactor code which scans folders with Python source code files to check usage  of english verbs in functions names. Results of analysis are printed to console. 

## Usage
```
usage: code_analysator.py [-h] [--dir FOLDER] [--top MAX_TOP] [--type FILE_TYPES]

analyses use of verbs in functions names

optional arguments:
  -h, --help         show this help message and exit
  --dir FOLDER       folder with code to analyse, default folder is current
  --top MAX_TOP      number of top used words, default=10
  --type FILE_TYPES  code file types, default='python'

```

## Sample output to console
```
file: ./flask/test.py -> top verbs: ('get', 6)
file: ./setup.py -> no verbs in function names!
file: ./django/test.py -> top verbs: ('get', 6)
file: ./data_out.py -> no verbs in function names!
file: ./__init__.py -> no verbs in function names!
file: ./dclnt.py -> top verbs: ('get', 6)
file: ./code_parser.py -> top verbs: ('get', 1)
file: ./code_analysator.py -> no verbs in function names!

```

## Requirements
```
python>=3.7.3
aiofiles==0.4.0
nltk==3.4.1
chardet==3.0.4
```

## NLTK dictionary installation
```
pip install nltk
```
Then install nltk averaged_perceptron_tagger dictionary through **nltk.download()**
```
python
>>>nltk.download('averaged_perceptron_tagger')
>>>exit()