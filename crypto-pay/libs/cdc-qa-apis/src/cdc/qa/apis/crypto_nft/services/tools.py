def compare_dict(params_dict: dict, request_dict: dict) -> dict:
    if request_dict.get("variables", False):
        request_dict["variables"] = params_dict
    return request_dict
