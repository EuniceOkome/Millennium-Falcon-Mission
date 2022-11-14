# Millennium-Falcon-Mission
Giskard technical test

## Here are some details on the documents of this project
This project has been mainly made in python.

* The back-end files are located in the folder GetOdds.
* The front-end files are located in the folder Front. It suffices to run main.py to access the webpage url.
* The CLI files are located in the folder CLI. 

I suggest two ways to use the CLI. Once we reach the file directory, we can run the commands by calling python
```
$ python CLI.py ../examples/millennium-falcon.json ../examples/empire2.json                 
81
```
or through a virtual environment:

```
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install --editable .
$ give-me-the-odds ../examples/millennium-falcon.json ../examples/empire2.json
81
$ deactivate
```
