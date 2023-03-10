import requests
from dataclasses import dataclass, field
from .services.drops import DropsService
from .services.pack import PackService
from .services.dropasset import DropAssetService
from .services.category import CategoryService
from .services.collection import CollectionService
from .services.dropaccess import DropAccessService
from .services.nftbrand import BrandService

__all__ = [
    "DropsService",
    "PackService",
    "DropAssetService",
    "CategoryService",
    "CollectionService",
    "DropAccessService",
    "BrandService",
]


@dataclass(frozen=True)
class NFTRestService:
    host: str = field(default="https://vsta-nft-custodial-backend-admin.3ona.co")
    session: requests.Session = field(default_factory=requests.Session)
    nft_token: str = field(default="")

    drops: DropsService = field(init=False)
    pack: PackService = field(init=False)
    dropasset: DropAssetService = field(init=False)
    category: CategoryService = field(init=False)
    collection: CollectionService = field(init=False)
    dropaccess: DropAccessService = field(init=False)
    nftbrand: BrandService = field(init=False)

    def __post_init__(self):
        services = {
            "drops": DropsService,
            "pack": PackService,
            "dropasset": DropAssetService,
            "category": CategoryService,
            "collection": CollectionService,
            "dropaccess": DropAccessService,
            "nftbrand": BrandService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, nft_token=self.nft_token))
