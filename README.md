# Text Summarization End to End Project

## Install text-summerization as package
```
pip install .
```
If not work
```
python setup.py sdist
```

## Train the model
```
python src/pipeline/train_model.py
```
After the model is trained. Initiate the web application
```
flask app
```
or 
```
python app.py
```