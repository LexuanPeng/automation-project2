from dataclasses import dataclass, field
from enum import unique, Enum, auto
from typing import List, Optional


@unique
class Fiat(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    USD = auto()
    SGD = auto()
    EUR = auto()
    GBP = auto()
    HKD = auto()
    CAD = auto()
    BRL = auto()
    AUD = auto()


@dataclass(frozen=True)
class FiatWalletInfo:
    fiat: Fiat
    deposit_methods: Optional[List[str]] = field(init=False)
    term_id: Optional[str] = field(init=False)

    def __post_init__(self):
        if self.fiat is Fiat.USD:
            object.__setattr__(self, "deposit_methods", ["van", "us_wire_transfer"])
            object.__setattr__(self, "term_id", "use_viban_agreement")
        elif self.fiat is Fiat.EUR:
            object.__setattr__(self, "deposit_methods", ["sepa"])
            object.__setattr__(self, "term_id", "use_viban_agreement")
        elif self.fiat is Fiat.CAD:
            object.__setattr__(self, "deposit_methods", ["ca_interac_etransfer"])
            object.__setattr__(self, "term_id", "use_viban_agreement")
        elif self.fiat is Fiat.BRL:
            object.__setattr__(self, "deposit_methods", ["br_cmp", "br_doc", "br_pix", "br_ted"])
            object.__setattr__(self, "term_id", "use_viban_agreement")
        elif self.fiat is Fiat.AUD:
            object.__setattr__(self, "deposit_methods", ["au_bpay", "au_npp"])
            object.__setattr__(self, "term_id", "use_viban_agreement")
        else:
            object.__setattr__(self, "deposit_methods", None)
            object.__setattr__(self, "term_id", None)
