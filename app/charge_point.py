import logging
from datetime import datetime
from ocpp.v16 import ChargePoint as BaseChargePoint
from ocpp.v16 import call_result, call
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.routing import on

logging.basicConfig(level=logging.INFO)


class ChargePoint(BaseChargePoint):
    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info(
            "Boot Notification received from Vendor: %s, Model: %s",
            charge_point_vendor,
            charge_point_model,
        )
        self.clear_charging_profile(1)
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted,
        )

    async def clear_charging_profile(self, connector_id):
        """Clearing charging profile for a connector"""
        print(connector_id, "clear clear clear clear clear clear")
        res = await self.call(call.ClearChargingProfilePayload(
                connector_id=connector_id
            ))
        print(res)
        return res