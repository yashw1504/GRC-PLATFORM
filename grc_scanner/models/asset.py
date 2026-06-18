from dataclasses import dataclass


@dataclass
class Asset:

    asset_id: str

    asset_name: str

    asset_type: str

    owner: str = ""

    environment: str = ""

    criticality: str = "Medium"