# Crypto.com QA Pay UI Automation

A monorepo containing all automated testing projects for crypto.com related products.

## Project Structure

```
├── common
│   ├── api         # Api helper for UI automation
│   ├── fixture     # Common fixture for pytest
│   └── utils       # Common utils
├── configs         # Config files
├── libs            # Submodule repo
├── pages       
│   ├── api         # Saving api test module
│   └── staging     # Saving web staging test module - page
├── report          # Report folder
├── test_cases      
│   └── staging     # Saving web staging bdd cases
└── test_resource   
    ├── data        # Saving test data
    ├── graphql     # Saving api helper gql
    └── objects     # saving web test page objects
└── README.md
```

## Running tests

Change working directory to desired project (e.g. `projects/crypto-pay`)

```sh
cd projects/crypto-pay
```
Install dependencies

```sh
poetry install
```

Use python run in projects/crypto-pay/main.py

```sh
# main.py arguments helper

#("--tag", type=str, help="Test tag")
#("--thread", type=str, help="Thread count", default="1")
#("--host_port", type=str, help="Remote host port", default="localhost:4444")
#("--qase_test_run_id", type=str, help="Qase test run id")
#("--env", type=str, help="Env", default="staging")
#("--qase", type=str, help="If push test step to qase", default="false")
#("--rerun", type=str, help="Rerun the failed cases: true, latest, false", default="false")
#("--data_env", type=str, help="Set the test data resource env folder", default="staging")

poetry run python main.py --tag ${tag} --host_port ${host_port} --thread ${thread} --env ${env} --qase ${qase} --rerun ${rerun} --data_env ${data_env}
```

Use make to run target defined in `Makefile`

```sh
make smoke

smoke:
  poetry run \
  python main.py \
  --tag smoke \
  --host_port localhost:4444 \
  --thread 20 \
  --env staging \
  --data_env staging \
  --qase true \
  --rerun true
```