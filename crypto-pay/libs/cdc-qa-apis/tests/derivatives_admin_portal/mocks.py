from pytest import fixture


@fixture
def mock_admin_help_placeholder(requests_mock):
    requests_mock.get(
        "https://dstg-internal-ui.x.3ona.co/global00a01/v1/admin/help/placeholder",
        json=[
            {"instId": 306, "symbol": "ADAUSD-PERP"},
            {"instId": 321, "symbol": "ALGOUSD-PERP"},
            {"instId": 10003, "symbol": "BTCUSD-211231"},
            {"instId": 303, "symbol": "BTCUSD-PERP"},
        ],
    )


@fixture
def mock_all_ps_admin_instrument_id(requests_mock):
    requests_mock.get(
        "https://dstg-internal-ui.x.3ona.co/global00a01/v1/admin/help/placeholder",
        json=[
            {"instId": 4, "symbol": "USD_Stable_Coin"},
        ],
    )


@fixture
def mock_incorrect_admin_help_placeholder(requests_mock):
    requests_mock.get(
        "https://dstg-internal-ui.x.3ona.co/global00a01/v1/admin/help/placeholder",
        json=[{"instId2": 306, "symbol2": "ADAUSD-PERP"}],
    )


@fixture
def mock_admin_get_account_id(requests_mock):
    requests_mock.post(
        "https://dstg-internal-ui.x.3ona.co/acct00a01/v1/admin/",
        json=[
            {
                "success": True,
                "host": "acct00a01",
                "service": "ACCOUNT_SERVICE",
                "result": '[["96a0d316-3e6c-402b-8a9a-57c543d11861",true,"3a346895-cf38-476a-b2c8-1ca8463bdba0",'
                '"","DERIVATIVES","USER",true,true,false,"No record (likely 0)",1620713061000,'
                "1620713061615]] ",
            }
        ],
    )


@fixture
def mock_admin_global_get_account_shard_name(requests_mock):
    requests_mock.post(
        "https://dstg-internal-ui.x.3ona.co/global00a01/v1/admin/",
        json=[
            {
                "success": True,
                "host": "global00a01",
                "service": "AUTH_SERVICE",
                "result": '[["3a346895-cf38-476a-b2c8-1ca8463bdba0","96a0d316-3e6c-402b-8a9a-57c543d11861",'
                '"3a346895-cf38-476a-b2c8-1ca8463bdba0",6,386,2,"INSTITUTIONAL"]]',
            }
        ],
    )


@fixture
def mock_admin_transfer_to_deriv(requests_mock):
    requests_mock.post(
        "https://dstg-internal-ui.x.3ona.co/acct00a01/v1/admin/",
        json=[
            [
                {
                    "success": False,
                    "host": "acct00a01",
                    "service": "POSITION_SERVICE3",
                    "result": "Outside this shard's scope",
                },
                {
                    "success": False,
                    "host": "acct00a01",
                    "service": "POSITION_SERVICE0",
                    "result": "Outside this shard's scope",
                },
                {
                    "success": False,
                    "host": "acct00a01",
                    "service": "POSITION_SERVICE1",
                    "result": "Outside this shard's scope",
                },
                {"success": True, "host": "acct00a01", "service": "POSITION_SERVICE2", "result": ""},
            ]
        ],
    )


@fixture
def mock_get_config(requests_mock):
    requests_mock.post(
        "https://dstg-internal-ui.x.3ona.co/global00a01/v1/admin/",
        json=[
            {
                "success": True,
                "host": "10.215.168.88",
                "service": "REFDATA_SERVICE",
                "result": '[["(Not subscribed)","{\\"clusterShardInfoList\\":[{\\"clusterType\\":\\"PRODUCT\\",'
                '\\"partitionSize\\":2,\\"shardDetails\\":[{\\"streamId\\":7400,\\"hosts\\":'
                '[\\"product00a01\\",\\"product00s01\\"],\\"filterDataDetails\\":[\\"BTC|PERP|FUTURE|'
                'WARRANT|OPTION,DAI,USDT\\",\\"DOT|PERP,UNI|PERP,ENJ|PERP,LTC|PERP,MATIC|PERP,ALGO|PERP,SUSHI|PERP,'
                'CRV|PERP,CHZ|PERP,AAVE|PERP,THETA|PERP,BCH|PERP,ATOM|PERP,FLOW|PERP,YFI|PERP\\",\\"ANKR|PERP,'
                "SNX|PERP,KAVA|PERP,IOTX|PERP,WAVES|PERP,LPT|PERP,NU|PERP,ADA|PERP,CRO|PERP,LINK|PERP,DOGE|PERP,"
                'VET|PERP,XRP|PERP,KSM|PERP\\",\\"XTZ|PERP,CELR|PERP,QNT|PERP,NEAR|PERP,AGLD|PERP,ONE|PERP,'
                'OMG|PERP,ILV|PERP,GALA|PERP,SAND|PERP,RUNE|PERP,GRT|PERP,HBAR|PERP,FIL|PERP\\"]},'
                '{\\"streamId\\":7401,\\"hosts\\":[\\"product01a01\\",\\"product01s01\\"],'
                '\\"filterDataDetails\\":[\\"ETH|PERP|FUTURE|WARRANT|OPTION\\",\\"1INCH|PERP,EFI|PERP,AVAX|PERP,'
                "ALICE|PERP,YGG|PERP,FTM|PERP,ICP|PERP,DYDX|PERP,SHIB|PERP,ENS|PERP,CHR|PERP,ZIL|PERP,ICX|PERP,"
                'MKR|PERP,DERC|PERP,KLAY|PERP\\",\\"SOL|PERP,BOSON|PERP,COMP|PERP,AXS|PERP,MANA|PERP,EGLD|PERP,'
                'XLM|PERP,LUNA|PERP,HOT|PERP,AUDIO|PERP,PLA|PERP,EOS|PERP,AR|PERP,HNT|PERP\\",\\"WAXP|PERP,'
                "BAT|PERP,LRC|PERP,STORJ|PERP,GTC|PERP,SC|PERP,SRM|PERP,SKL|PERP,BAND|PERP,RAY|PERP,QTUM|PERP,"
                "CTSI|PERP,IMX|PERP,OCEAN|PERP,OGN|PERP,APE-dpre|PERP,APE|PERP,RSR|PERP,NKN|PERP,BAL|PERP,"
                'BAL-dpre|PERP,RSR-dpre|PERP,NKN-dpre|PERP\\"]}]}]}",1648098971415]]',
            }
        ],
    )
