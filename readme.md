# CodeAnalysator

**codea_analysator.py** was done as home work to refactor code which scans folders with Python source code files to check usage  of english verbs in functions names. Results of analysis are printed to console. 

## Usage
```
usage: code_analysator.py [-h] [--dir FOLDER] [--top MAX_TOP]

analyses use of verbs in functions names

optional arguments:
  -h, --help     show this help message and exit
  --dir FOLDER   folder with code to analyse
  --top MAX_TOP  number of top used words, default=10
```

## Sample output to console
```
file: ./flask/test.py -> verbs ['get', 'get', 'get', 'get', 'get', 'get']  top verbs[('get', 6)]
file: ./__init__.py -> no verbs in function names!
file: ./dclnt.py -> verbs ['get', 'get', 'get', 'get', 'get', 'get']  top verbs[('get', 6)]
file: ./code_analysator.py -> no verbs in function names!
file: ./django/test.py -> verbs ['get', 'get', 'get', 'get', 'get', 'get']  top verbs[('get', 6)]
file: ./data_out.py -> no verbs in function names!
file: ./setup.py -> no verbs in function names!
file: ./code_parser.py -> verbs ['get']  top verbs[('get', 1)]
 
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