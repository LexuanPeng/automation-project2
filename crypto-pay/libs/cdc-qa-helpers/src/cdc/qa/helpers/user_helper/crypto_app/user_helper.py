import logging
from dataclasses import dataclass
from enum import Enum, unique, auto
from pathlib import Path
from time import sleep
from typing import Union, Optional, List
from .feature_flags import AG, AU, BR, CA, MALTA, SG, TK, UK, US

import yaml
from requests import HTTPError

from cdc.qa.apis.jumio import JumioApi
from cdc.qa.apis.rails import RailsApi
from cdc.qa.apis.rails.data.jumio import DocumentType
from cdc.qa.helpers import RailsConsoleHelper

logger = logging.getLogger(__name__)


@dataclass
class User:
    email: str
    passcode: Union[str, int]
    name: str
    phone_number: str
    country_alpha_2: str
    country_alpha_3: str
    dob: str
    document_type: DocumentType
    payment_currency: str

    user_id: Optional[int] = None
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    town: Optional[str] = None
    state_code: Optional[str] = None
    postcode: Optional[str] = None
    zip_code: Optional[str] = None

    register_phone_number: Optional[str] = None
    entity_id: Optional[str] = None


@unique
class Entity(Enum):
    US = auto()
    SG = auto()
    MALTA = auto()
    UK = auto()
    CA = auto()
    AU = auto()
    BR = auto()
    AG = auto()
    TK = auto()


def get_user(email: str, passcode: Union[int, str], entity: Entity = Entity.US, profile: str = "profile_1") -> User:
    """Shortcut function to get 'User' based on the 'Entity'.

    Args:
        email: user email
        passcode: user passcode
        entity: user entity, see Entity()
        profile: select the user profile in yaml, e.g. "profile_1"

    Returns:
        User dataclass based on the entity and user profile selected.
    """

    entity = entity.name.lower()
    path = Path(__file__).resolve(strict=True).parents[2] / f"data/crypto_app/users/staging/{entity}.yaml"
    profiles = yaml.safe_load(open(path))
    try:
        user_data = profiles[profile]
    except KeyError:
        raise ValueError(f"Profile '{profile}' is not found.")
    user_data["document_type"] = DocumentType[user_data["document_type"]]
    return User(email=email, passcode=passcode, **user_data)


def create_user(
    user: User,
    accept_terms: bool = True,
    submit_required_personal_information: bool = True,
    disable_sms_verification: bool = True,
    skip_upload_kyc_docs_if_needed: bool = False,
    rails_api: Optional[RailsApi] = None,
    rails_console_helper: Optional[RailsConsoleHelper] = None,
    jumio_api: Optional[JumioApi] = None,
    update_address: bool = True,
    verify_phone_number: bool = False,
    **kwargs,
) -> User:
    """Function to sign up a user account on Main App and an API flow for the steps are mentioned in this guide:
    https://mcoproduct.atlassian.net/wiki/spaces/PQA/pages/2267775385/Simple+Sign+up+guide+on+Main+App+for+new+joiner

    The phone numbers other than US, UK, EU & SG will be rejected when calling `rails_api.user.phone_update()`.
    Therefore, this function will create an account using US's phone number, then set to targeted phone number. phone
    country and entity id. Refer to
    https://mcoproduct.atlassian.net/wiki/spaces/PQA/pages/2137300738/BRL+Entity+Migration &
    https://mcoproduct.atlassian.net/wiki/spaces/PQA/pages/2178057258/Create+Brazil+Testing+Account+or+other+countries+without+phone+number+to+receive+SMS+on+Staging
     for more information

    Args:
        user: the user dataclass
        accept_terms: accept T&C, so the user won't need to accept the T&C on UI
        submit_required_personal_information: submit the required personal information for user via api in prior, so the
         user won't need to submit personal information on Home page
        disable_sms_verification: when the app asks for SMS OTP. the OTP input by the user will not be verified
        skip_upload_kyc_docs_if_needed: manual Jumio api will be skipped if it fails to call
        rails_api: RailsApi from 'cdc.qa.apis'
        rails_console_helper: RailsConsoleHelper from 'cdc.qa.helpers'
        jumio_api: JumioApi from 'cdc.qa.apis'
        update_address: update_address
        verify_phone_number: verify phone number by calling Rails API

    Returns:
        User: the user dataclass used to create Crypto app user account.
    """

    rails_api = rails_api or RailsApi()
    rails_console_helper = rails_console_helper or RailsConsoleHelper()
    jumio_api = jumio_api or JumioApi()

    passcode = str(user.passcode)
    country_alpha_3 = user.country_alpha_3.upper()

    rails_api.user.auth(user.email)
    magic_token = rails_console_helper.get_magic_token(user.email)
    rails_api.auth.authenticate(user.email, magic_token)
    rails_api.user.passcode_update(passcode)

    if rails_api._env == "stg":
        # Rails access token will be populated again after verify passcode and phone number
        rails_api.auth.set_token(rails_console_helper.get_rails_access_token(user.email))

    rails_api.user.terms_update(True)
    rails_api.user.newsletter_update(False)
    rails_api.user.name_update(user.name)

    try:
        user_id = rails_api.account.get_user_id()
        user.user_id = user_id
    except ValueError:
        logger.debug("Trying to get User ID via rails console...")
        user_id = rails_console_helper.get_user_id(user.email)

    if user.document_type is DocumentType.ID_CARD:
        if rails_api._env == "stg":
            upload_urls = rails_api.manual_jumio.get_upload_jumio_pic_urls(country_alpha_3)
            kyc_pic_path = Path(__file__).resolve(strict=True).parents[2] / "data/crypto_app/users/kyc_pic_01.jpg"
            for url in [upload_urls.liveness, upload_urls.selfie, upload_urls.id_card_back, upload_urls.id_card_front]:
                jumio_api.file.upload(url.path, url.query_params, kyc_pic_path)
    elif user.document_type is DocumentType.PASSPORT:
        raise NotImplementedError
    elif user.document_type is DocumentType.DRIVING_LICENSE:
        raise NotImplementedError
    else:
        raise ValueError(f"Upload {user.document_type.name} flow is not available yet.")

    try:
        sleep(1)
        rails_api.manual_jumio.create(country_alpha_3, user.document_type)
        sleep(1)

    except HTTPError as e:
        if skip_upload_kyc_docs_if_needed:
            logger.warning("Failed to call '/api/manual_jumio/create', skip uploading kyc docs.")
        else:
            raise e

    register_phone_number = user.register_phone_number or user.phone_number
    if verify_phone_number:
        rails_api.user.phone_update(register_phone_number)
        rails_api.user.phone_verify(rails_console_helper.get_user_sms_otp(user.email))
    else:
        if user.register_phone_number:
            rails_console_helper.set_user_phone_and_phone_country(user.email, user.phone_number, country_alpha_3)
        else:
            rails_console_helper.update_phone_number(user.email, user.phone_number)
        if user.entity_id:
            rails_console_helper.set_user_entity(user.email, user.entity_id, country_alpha_3)

    default_feature_flags = get_default_feature_flags(user)
    rails_console_helper.approve_user(user_id, defaults_features=default_feature_flags)
    rails_console_helper.update_document_issuing_country(user.email, country_alpha_3)
    rails_api.user.payment_currency_update(user.payment_currency)

    if accept_terms:
        rails_api.terms.accept_terms()

    if submit_required_personal_information:
        info = rails_api.app.features_required_personal_information().required_personal_information

        if update_address:
            # Update address for SG users
            if info.app_access and "sg_address:submit" in info.app_access:
                rails_api.address.update(
                    address_1=user.address_1,
                    address_2=user.address_2,
                    city=user.city,
                    country=user.country,
                    postcode=user.postcode,
                    zip_code=user.zip_code,
                )

            # Update address for AU users
            if info.fiat_withdrawal and "residential_address:submit" in info.fiat_withdrawal:
                rails_api.address.residential_address_create(
                    address_1=user.address_1,
                    address_2=user.address_2,
                    country=user.country,
                    postcode=user.postcode,
                    state=user.state_code,
                    town=user.town,
                )

            # Update address for Turkey Users
            if info.app_access and "account_creation:submit" in info.app_access:
                rails_api.kyc_info.submit_turkey_user_residential_address()

    if disable_sms_verification:
        rails_console_helper.set_sms_verification_status(user.user_id, False)

    return user


def get_whitelist_phone_number(entity: Entity = Entity.US):
    entity = entity.name.lower()
    path = Path(__file__).resolve(strict=True).parents[2] / f"data/crypto_app/users/staging/{entity}.yaml"
    data = yaml.safe_load(open(path))
    try:
        phone_number_list = data["whitelist_phone_number_list"]
    except KeyError:
        raise ValueError("data['whitelist_phone_number_list'] was not found.")

    return phone_number_list


def get_default_feature_flags(user: User) -> List[str]:
    country = user.country_alpha_2
    if country == "AR":
        return AG
    elif country == "BR":
        return BR
    elif country == "AU":
        return AU
    elif country == "CA":
        return CA
    elif country == "PO":
        return MALTA
    elif country == "SG":
        return SG
    elif country == "TR":
        return TK
    elif country == "GB":
        return UK
    else:
        return US
