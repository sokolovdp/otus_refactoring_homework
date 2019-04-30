# CodeAnalysator

**codea_analysator.py** was done as home work to refactor code which scans folders with Python source code files to check usage  of english verbs in functions names.
Results of analysis are printed to console. 

## Usage
```
usage: codeanalysator.py 
```

## Use as standalone program
```
python codeanalysator.py 

```
## Sample output to console
```
 file= /home/dmitrii/ws/proj/otus_refactoring_homework/django/test.py verbs= ['get', 'get', 'get', 'get', 'get', 'get'] top verbs= [('get', 6)]
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