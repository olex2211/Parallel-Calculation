import httpx
import logging

from app.core.config import settings
from app.core.exceptions import EntityNotFoundException, ServiceUnavailableException
from app.schemas.external import ExternalPrescriptionResponse

logger = logging.getLogger(__name__)


class TreatmentClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
        self.base_url = settings.TREATMENT_SERVICE_URL

    async def get_prescriptions_by_visit(self, visit_id: int) -> list[ExternalPrescriptionResponse]:
        # First we need to find the diagnosis_id for this visit_id
        diagnosis_url = f"{self.base_url}{settings.API_PREFIX}/diagnoses?visit_id={visit_id}"
        try:
            diag_response = await self._client.get(diagnosis_url)
            diag_response.raise_for_status()
            diagnoses = diag_response.json()
            if not diagnoses:
                return []
            diagnosis_id = diagnoses[0]["id"]
            
            # Now fetch prescriptions
            rx_url = f"{self.base_url}{settings.API_PREFIX}/prescriptions?diagnosis_id={diagnosis_id}"
            rx_response = await self._client.get(rx_url)
            rx_response.raise_for_status()
            
            logger.info(f"Got prescriptions for visit {visit_id} from treatment-service")
            return [ExternalPrescriptionResponse(**p) for p in rx_response.json()]
            
        except httpx.TimeoutException:
            raise ServiceUnavailableException("treatment-service", "timeout")
        except httpx.ConnectError:
            raise ServiceUnavailableException("treatment-service", "connection refused")
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTPStatusError from treatment-service: {exc}")
            raise ServiceUnavailableException("treatment-service", f"status {exc.response.status_code}")
