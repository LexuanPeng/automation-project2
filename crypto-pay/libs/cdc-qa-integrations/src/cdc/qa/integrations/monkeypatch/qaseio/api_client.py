from qaseio.model_utils import (
    ModelNormal,
    file_type,
)

from qaseio.api_client import Endpoint


def patched__gather_params(self, kwargs):
    params = {"body": None, "collection_format": {}, "file": {}, "form": [], "header": {}, "path": {}, "query": []}

    for param_name, param_value in kwargs.items():
        param_location = self.location_map.get(param_name)
        if param_location is None:
            continue
        if param_location:
            if param_location == "body":
                params["body"] = param_value
                continue
            base_name = self.attribute_map[param_name]
            if param_location == "form" and self.openapi_types[param_name] == (file_type,):
                params["file"][base_name] = [param_value]
            elif param_location == "form" and self.openapi_types[param_name] == ([file_type],):
                # param_value is already a list
                params["file"][base_name] = param_value
            elif param_location in {"form", "query"}:
                if isinstance(param_value, ModelNormal):
                    param_values = [(f"{base_name}[{k}]", v) for k, v in param_value.to_dict().items()]
                    params[param_location].extend(param_values)
                else:
                    param_value_full = (base_name, param_value)
                    params[param_location].append(param_value_full)
            if param_location not in {"form", "query"}:
                params[param_location][base_name] = param_value
            collection_format = self.collection_format_map.get(param_name)
            if collection_format:
                params["collection_format"][base_name] = collection_format

    return params


Endpoint._Endpoint__gather_params = patched__gather_params  # type: ignore
