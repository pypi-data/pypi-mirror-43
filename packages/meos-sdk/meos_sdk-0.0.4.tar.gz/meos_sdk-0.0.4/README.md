## Running the examples

```
pip install -e .
meos_sdk run -a examples.hello_world.app
```

## Running a production grade server
Meos uses `uWsgi` under the hood to run a server in production environment. To run this server set the `--debug` flag to `0`.
```
pip install -e .
meos_sdk run -a examples.hello_world.app --debug 0
```