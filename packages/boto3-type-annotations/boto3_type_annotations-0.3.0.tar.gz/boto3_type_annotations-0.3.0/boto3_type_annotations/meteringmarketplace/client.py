from typing import Optional
from typing import List
from botocore.client import BaseClient
from botocore.paginate import Paginator
from typing import Dict
from datetime import datetime
from typing import Union
from botocore.waiter import Waiter


class Client(BaseClient):
    def batch_meter_usage(self, UsageRecords: List, ProductCode: str) -> Dict:
        pass

    def can_paginate(self, operation_name: str = None):
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None, HttpMethod: str = None):
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    def meter_usage(self, ProductCode: str, Timestamp: datetime, UsageDimension: str, UsageQuantity: int, DryRun: bool) -> Dict:
        pass

    def register_usage(self, ProductCode: str, PublicKeyVersion: int, Nonce: str = None) -> Dict:
        pass

    def resolve_customer(self, RegistrationToken: str) -> Dict:
        pass
