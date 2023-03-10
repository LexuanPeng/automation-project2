# `QA Tools API` Documentation

## Data Manager
``` python
api_key = "service_api_key"
secret_key = "service_secret_key"
host = "https://oqsta-meta.3ona.co/api/"
qatool_services = QAToolsApiServices(api_key=api_key, secret_key=secret_key, host=host)

service_id = 1 # service_id

# get datas
resp = rest_s.data_manager.get_service_datas(service_id=service_id, is_lock=0)
data_list = resp.data.result

data_id = 1 # data ID get from data detail
# lock data
rest_s.data_manager.lock_data(service_id=service_id, 65, data_id=data_id)
# release data
rest_s.data_manager.release_data(service_id=service_id, data_id=data_id)
```