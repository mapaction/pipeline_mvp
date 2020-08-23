# pipeline_mvp

## Running

1. Create a crash move folder (CMR) by cloning 
   [this](https://github.com/mapaction/default-crash-move-folder)
   repository, and changing the name of the `20YYiso3nn` directory to the relevant value

2. Modify `run.yaml` CMF configuration details

3. To run pipeline:
    ``` bash
    dagster pipeline execute -f main.py -c run.yaml -c config/yem.yaml
    ```

4. To run dagit (for debugging):
    ```bash
    dagit -f main.py
    ```
    To get the config parameters, run
    ```bash
    cat run.yaml config/yem.yaml 
    ```
    and copy and paste the results into the playground tab. 
    
5. To run dagit and see materializations:
    1. Set up a postgres DB
    2. Create a file `dagster.yaml` and populate it as suggested 
    [here](https://docs.dagster.io/_apidocs/libraries/dagster_postgres)
    3. Install `dagster_postgres`:
    ```
    pip install dagster_postgres 
    ```
    4. Run the following:
    ```bash
    DAGSTER_HOME=$dagster_home dagit -f main.py
    ```
   where `$dagster_home` is the directory containing `dagster.yaml`
   
## Testing

In the top-level directory, execute:
```
pytest
```
 