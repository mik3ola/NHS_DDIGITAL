from typing import Any, Dict
from aws_lambda_powertools import Logger


ADDRESS_CHANGE_KEY = "address"
PHONE_CHANGE_KEY = "phone"
POSTCODE_CHANGE_KEY = "postcode"
PUBLICNAME_CHANGE_KEY = "public_name"
WEBSITE_CHANGE_KEY = "website"
OPENING_DATES_KEY = "opening_dates"
OPENING_DAYS_KEY = "opening_days"

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"

logger = Logger(child=True)


class ChangeRequest:
    changes: Dict[str, Any]

    def __init__(self, service_id: int, changes: Any = None):
        correlation_id = logger.get_correlation_id()

        self.reference = correlation_id
        self.system = "DoS Integration"
        self.message = f"DoS Integration CR. correlation-id: {correlation_id}"
        self.service_id = str(service_id)
        self.changes = changes
        if self.changes is None:
            self.changes = {}

    def create_payload(self) -> Dict[str, Any]:
        """Creates the payload for the change request

        Returns:
            Dict[str, Any]: The change request payload
        """
        return {
            "reference": self.reference,
            "system": self.system,
            "message": self.message,
            "service_id": self.service_id,
            "changes": self.changes,
        }
