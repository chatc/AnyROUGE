### AnyROUGE
A python wrapper for the original Perl version ROUGE score evaluator.

### Dependency
pyrouge
nltk

### Usage
python AnyROUGE.py (the file path is hard-coded in the python file)

### Setup ini

- create a file `~/.pyrouge/settings.ini`
- Write the absolute path of the ROUGE155 to this file, e.g.
```
[pyrouge settings]
home_dir=PATH_TO_FOLDER/ThirdParty/ROUGE/ROUGE-1.5.5/
```
