def test_upload_urls_validator():
    from cdc.qa.apis.rails.models.manual_jumio import UploadUrls

    urls = UploadUrls.parse_raw(
        """
        {
            "liveness":"https://random.domain.com/some-path/liveness.jpg?X-Amz-Expires=780\\u0026X-Amz-Date=20210629T102347Z\\u0026X-Amz-Algorithm=AWS4-HMAC-SHA256\\u0026X-Amz-Credential=RANDOMAWSCRED/123456\\u0026X-Amz-SignedHeaders=host\\u0026X-Amz-Signature=ea13a3a20377c48f7fc89782d91ae34f",
            "selfie":"https://random.domain.com/some-path/selfie.jpg?X-Amz-Expires=780\\u0026X-Amz-Date=20210629T102347Z\\u0026X-Amz-Algorithm=AWS4-HMAC-SHA256\\u0026X-Amz-Credential=RANDOMAWSCRED/123456\\u0026X-Amz-SignedHeaders=host\\u0026X-Amz-Signature=0cf1a5d8794efd9c965785d6651ebd3c",
            "id_card_front":"https://random.domain.com/some-path/id_card_front.jpg?X-Amz-Expires=780\\u0026X-Amz-Date=20210629T102347Z\\u0026X-Amz-Algorithm=AWS4-HMAC-SHA256\\u0026X-Amz-Credential=RANDOMAWSCRED/123456\\u0026X-Amz-SignedHeaders=host\\u0026X-Amz-Signature=a291b6f3ac8b3d858509234ca2ad3e7e",
            "id_card_back":"https://random.domain.com/some-path/id_card_back.jpg?X-Amz-Expires=780\\u0026X-Amz-Date=20210629T102347Z\\u0026X-Amz-Algorithm=AWS4-HMAC-SHA256\\u0026X-Amz-Credential=RANDOMAWSCRED/123456\\u0026X-Amz-SignedHeaders=host\\u0026X-Amz-Signature=30d69181245ea9d5e60567f7f8c009b2",
            "driver_license_front":"https://random.domain.com/some-path/driver_license_front.jpg?X-Amz-Expires=780\\u0026X-Amz-Date=20210629T102347Z\\u0026X-Amz-Algorithm=AWS4-HMAC-SHA256\\u0026X-Amz-Credential=RANDOMAWSCRED/123456\\u0026X-Amz-SignedHeaders=host\\u0026X-Amz-Signature=77e8e59b546437dad11e3120b1269fd8",
            "driver_license_back":"https://random.domain.com/some-path/driver_license_back.jpg?X-Amz-Expires=780\\u0026X-Amz-Date=20210629T102347Z\\u0026X-Amz-Algorithm=AWS4-HMAC-SHA256\\u0026X-Amz-Credential=RANDOMAWSCRED/123456\\u0026X-Amz-SignedHeaders=host\\u0026X-Amz-Signature=41b0794f5437b9acef0a3469990e5bd4"
        }
        """  # noqa:E501
    )

    assert urls.liveness.host == "https://random.domain.com"
    assert urls.liveness.path == "/some-path/liveness.jpg"
    assert urls.liveness.query_params == {
        "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
        "X-Amz-Credential": "RANDOMAWSCRED/123456",
        "X-Amz-Date": "20210629T102347Z",
        "X-Amz-Expires": "780",
        "X-Amz-Signature": "ea13a3a20377c48f7fc89782d91ae34f",
        "X-Amz-SignedHeaders": "host",
    }
