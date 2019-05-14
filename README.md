# CodeAnalysator

**codea_analysator.py** was done as Otus course homework to refactor given code which scans folders with Python source code files to check usage of english verbs in functions names. Results of analysis are printed to console. Maximum number of files which can be processed is limited by 200. 

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
file: ./inac_api/flask_app/apps/fttb_mobile/views.py -> top verbs: ('get', 27), ('add', 15), ('run', 2), ('find', 1)
file: ./inac_api/flask_app/helpers/stubs/iptv/iptv_calc_pkg.py -> top verbs: ('get', 2), ('add', 1)
file: ./inac_api/flask_app/apps/fttb_mobile/common.py -> top verbs: ('get', 6), ('save', 1)
file: ./inac_api/flask_app/helpers/tv/iptv.py -> top verbs: ('get', 3)
file: ./inac_api/flask_app/apps/fttb_mobile/base_schemas.py -> no verbs in function names!
...
--- processed 200 files ---
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