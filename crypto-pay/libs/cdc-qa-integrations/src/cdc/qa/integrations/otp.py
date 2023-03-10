import pyotp


# ? Is it really necessary to make this a standalone function...?
def get_totp(seed: str) -> str:
    """Get current TOTP given the seed.

    Args:
        seed (str): The seed to generate TOTP.

    Returns:
        str: TOTP based on current device time.
    """
    return pyotp.TOTP(seed).now()
