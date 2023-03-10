GetCollectionsPage = """
query GetCollectionsPage($cacheId: ID,
$search: String,
$first: Int,
$skip: Int,
$sort: SingleFieldSort,
$withStats: Boolean!,
$categories: [ID!],
$networks: [SupportedNetwork!],
$isSortFieldZeroLast: Boolean!,
$timeRange: TimeRange,
$hideEmpty: Boolean,
$verifiedOnly: Boolean) {
  public(cacheId: $cacheId) {
    collections(
      search: $search
      first: $first
      skip: $skip
      sort: $sort
      categories: $categories
      networks: $networks
      isSortFieldZeroLast: $isSortFieldZeroLast
      timeRange: $timeRange
      hideEmpty: $hideEmpty
      verifiedOnly: $verifiedOnly
    ) {
      ...CollectionStatsData
      __typename
    }
    __typename
  }
}

fragment CollectionStatsData on Collection {
  id
  creator {
    username
    __typename
  }
  name
  logo {
    url
    __typename
  }
  metrics {
    listedCollectiblesCount
    owners
    items
    editionsCount
    totalSalesDecimal
    minSaleListingPriceDecimal
    __typename
  }
  priceAlert {
    id
    __typename
  }
  verified
  stats @include(if: $withStats) {
    floorPriceDecimal
    allDayBuyerCount
    oneDayBuyerCount
    oneDayFloorPriceDecimal
    oneDayFloorPriceDecimalChange
    oneDayVolumeDecimal
    oneDayVolumeDecimalChange
    sevenDayBuyerCount
    sevenDayFloorPriceDecimal
    sevenDayFloorPriceDecimalChange
    sevenDayVolumeDecimal
    sevenDayVolumeDecimalChange
    thirtyDayBuyerCount
    thirtyDayFloorPriceDecimal
    thirtyDayFloorPriceDecimalChange
    thirtyDayVolumeDecimal
    thirtyDayVolumeDecimalChange
    __typename
  }
  watched
  __typename
}
"""
