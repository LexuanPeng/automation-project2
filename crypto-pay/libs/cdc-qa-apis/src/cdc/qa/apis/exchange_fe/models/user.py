from decimal import Decimal
from pydantic import Field
from ..fe_models import FeExchangeRequest, FeExchangeResponse, FrozenBaseModel


class UpdateFeeCoinOpenRequest(FeExchangeRequest):
    useFeeCoinOpen: str = Field(description="1 - enable earn rebates, 0 - disable earn rebates ")


class UpdateFeeCoinOpenResponse(FeExchangeResponse):
    pass


class StakingInfoDataDetail(FrozenBaseModel):
    can_unstake: bool
    can_unstake_in_days: int
    deposit_bonus_period: str
    dynamic_coin_bonus_amount: str
    dynamic_coin_bonus_remaining_days: str
    id: int
    min_staking_days: int
    open_reward_session: bool
    past_trading_volume: str
    staked_before: bool
    staking_amount: str
    staking_currency: str = Field(description="Staking currency, default is CRO")
    staking_delta_to_tier_2: str
    total_deposit_bonus: str
    trading_volume_tier: str = Field(description="user trading volume tier")
    user_created_duration: str
    uuid: str = Field(description="user uuid")


class StakingInfoResponse(FeExchangeResponse):
    data: StakingInfoDataDetail = Field(description="staking info data")


# user/withdrawal_info
class WithdrawalInfoDataDetail(FrozenBaseModel):
    LimitAmount24h: Decimal = Field(alias="24hLimitAmount")
    LimitCurrency24h: str = Field(alias="24hLimitCurrency")
    last24hAmountInBtc: Decimal
    last24hAmountInUsd: Decimal
    userTier: int


class WithdrawalInfoResponse(FeExchangeResponse):
    data: WithdrawalInfoDataDetail = Field(description="staking info data")
