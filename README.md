# Test-History-Analyzer

## Usage
0. Install dependencies:
```
pip install -r requirements.txt
```
1. Current version: only works with projects written in Python and tested by pytest.
2. Get test history:
```
python src/tha.py GITHUB-REPO-URL
```
Test history (in descending order, first row is latest commit) will be in the [output/](https://github.com/hil-se/Test-History-Analyzer/tree/main/output) folder.
