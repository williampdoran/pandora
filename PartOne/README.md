# PartOne: Order aggregation

Create your favorite python virtualEnv and activate it, install requirements (I used python 3.9.2, pyenv and pip):
```bash
cd <PATH>/pandora/PartOne
pip install -r src/main/python/requirements.txt
```
To run the main application, which will generate sample data and run the order calculation:
```bash
cd <PATH>/pandora/PartOne
PYTHONPATH=src/ python src/main/python/application.py
ls <PATH>/pandora/PartOne/output
```
This directory will contain generated products and orders data sets, and the final aggregated order data set
To run pytests:
```bash
cd <PATH>/pandora/PartOne
PYTHONPATH=src/main/python python -m pytest src/test/python/
```

## Assumptions:
- I made the assumption that individual product orders made on the same day by the same customer should be aggregated into the same order
- I also dropped any products that had a null category
- I assumed a normal distribution for any random choices of products, categories and customers
