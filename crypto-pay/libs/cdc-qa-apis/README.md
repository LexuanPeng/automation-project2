# Crypto.com QA API Libraries Collection
This package contains multiple sub-packages, each interacting with the API provided by their respective product.

## Supported APIs
| API | Sub-package | Doc | Maintainer |
|:-:|:-:|:-:|:-:|
| [One Exchange API](https://exchange-docs.crypto.com/exchange/v1/rest-ws/index.html) | `exchange_oex` | [Here](src/crypto/qa/apis/exchange_oex/README.md) | [@MaxBai-crypto](https://github.com/MaxBai-crypto) |
| [Exchange V2 API](https://exchange-docs.crypto.com/spot/index.html#introduction) | `exchange` | [Here](src/crypto/qa/apis/exchange/README.md) | [@MaxBai-crypto](https://github.com/MaxBai-crypto) |
| [Exchange Derivatives API](https://exchange-docs.crypto.com/derivatives/index.html#introduction) | `exchange_derivatives` | [Here](src/crypto/qa/apis/exchange_derivatives/README.md) | [@MaxBai-crypto](https://github.com/MaxBai-crypto) |
| Exchange Derivatives Admin | `derivatives_admin_portal` | [Here](src/crypto/qa/apis/derivatives_admin_portal/README.md) | [@MaxBai-crypto](https://github.com/MaxBai-crypto) |
| Rails API | `rails` | [Here](src/crypto/qa/apis/rails/README.md) | [@ash-cryptocom](https://github.com/ash-cryptocom) |
| Jumio API | `jumio` | [Here](src/crypto/qa/apis/jumio/README.md) | [@ash-cryptocom](https://github.com/ash-cryptocom) |
| Plaid API | `plaid` | [Here](src/crypto/qa/apis/plaid/README.md) | [@ash-cryptocom](https://github.com/ash-cryptocom) |
| Crypto Pay API | `crypto_pay` | [Here](src/crypto/qa/apis/crypto_pay/README.md) | [@benhe-crypto](https://github.com/benhe-crypto) |
| Exchange Frontend API | `exchange_fe` | [Here](src/crypto/qa/apis/exchange_fe/README.md) | [@evelynwang-crypto](https://github.com/evelynwang-crypto) |
| QA Tools API | `qa_tools` | [Here](src/crypto/qa/apis/qa_tools/README.md) | [@MaxBai-crypto](https://github.com/MaxBai-crypto) |
| Crypto NFT API | `crypto_nft` | [Here](src/crypto/qa/apis/crypto_nft/README.md) | [@Evading-crypto](https://github.com/Evading-crypto) |
| Crypto NFT Admin API | `crypto_nft_admin` | [Here](src/crypto/qa/apis/crypto_nft_admin/README.md) | [@TommyHan-crypto](https://github.com/qatommy99) |

## General Usage
1. Add and install this package as a dependency (using [Poetry](https://python-poetry.org/))
    - In `pyproject.toml`, add the following line under `[tool.poetry.dependencies]`:
        ```toml
        cdc-qa-apis = {path = "../../libs/cdc-qa-apis", develop = true}
        ```
    - Install the package with the following command:
        ```sh
        poetry install
        ```
2. Import the required sub-package
    ```python
    from cdc.qa.apis import exchange
    ```
3. Use the sub-package as per each sub-package's instructions. It usually involves constructing an `Api` instance and using the methods provided.

    Here is an example on using the `exchange` sub-package.

    ```python
    from cdc.qa.apis import exchange

    api = exchange.ExchangeApi(api_key="your key", secret_key="your secret")
    result = api.rest.public.book.get_book(instrument_name="BTC_USDT")
    print(result.data[0].bids)
    ```
    > See [Supported APIs](#supported-apis) for a list of documentations on each sub-package.

## Further Reading
- (For maintainer) [Defining an API](docs/defining_api.md)
