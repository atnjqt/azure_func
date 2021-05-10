# Flask Python API Example

This Python Flask app leverages the `ryp2` module to pass a pandas dataframe to the R module BCRA (more info [here](https://cran.r-project.org/web/packages/BCRA/index.html))

## Build the app

```
cd app

docker build --tag flask-bcra-app .
```


- When you are ready to run locally:

``` bash

docker run --publish 5000:5000 -d flask-bcra-app

```

- This is combined together in 

```bash

./deploy.sh

```

_________


## API in browser

In browser you can navigate to the main hello world

The api for 9 cols of BCRA input is the real goal

Example string --> http://0.0.0.0:5000/api/example_df?id=0&T1=40&T2=45&N_Biop=1&HypPlas=99&AgeMen=14a&Age1st=24&N_Rels=1&Race=1



_________


### R to Python example 

notebook here --> [flask-app-testing.ipynb](./flask-app-testing.ipynb)
