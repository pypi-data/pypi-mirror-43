# Readme prun #

`prun` is a convenience app for working with virtual environments.
Use `prun` within a folder structure that has a virtual environment folder.`
It will automatically add the  

The code below shows how to use `prun`.
First a local virtual environment is created in the `.venv` folder.
```
python -m virtualenv .venv
```

Running the following command from the command shell will show that the 
`<venv>/Scripts (win)` or `<venv>/bin` (osx, linux) is added to the path.
The path to the python executable of the local virtual environment should be shown.
```
prun which python
```


`prun` can be used to install python packages in the local virtual environment.
```
prun pip install numpy
```



When executing `prun` without any extra command line arguments, 
the python of the virtual environment will be executed.
```
prun
```


