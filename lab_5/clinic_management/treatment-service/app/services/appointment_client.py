import httpx
import logging

from app.core.config import settings
from app.core.exceptions import EntityNotFoundException, ServiceUnavailableException
from app.schemas.external import ExternalVisitResponse

logger = logging.getLogger(__name__)


class AppointmentClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
        self.base_url = settings.APPOINTMENT_SERVICE_URL

    async def get_visit(self, visit_id: int) -> ExternalVisitResponse:
        url = f"{self.base_url}{settings.API_PREFIX}/visits/{visit_id}"
        try:
            response = await self._client.get(url)
            if response.status_code == 404:
                raise EntityNotFoundException("Visit", visit_id)
            response.raise_for_status()
            logger.info(f"Got visit {visit_id} from appointment-service")
            return ExternalVisitResponse(**response.json())
        except httpx.TimeoutException:
            raise ServiceUnavailableException("appointment-service", "timeout")
        except httpx.ConnectError:
            raise ServiceUnavailableException("appointment-service", "connection refused")
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTPStatusError from appointment-service: {exc}")
            raise ServiceUnavailableException("appointment-service", f"status {exc.response.status_code}")

    async def get_visits_by_patient(self, patient_id: int) -> list[ExternalVisitResponse]:
        url = f"{self.base_url}{settings.API_PREFIX}/visits?patient_id={patient_id}"
        try:
            response = await self._client.get(url)
            # If patient doesn't exist, appointment service might return 404, or just empty list.
            if response.status_code == 404:
                 raise EntityNotFoundException("Patient", patient_id)
            response.raise_for_status()
            logger.info(f"Got visits for patient {patient_id} from appointment-service")
            return [ExternalVisitResponse(**v) for v in response.json()]
        except httpx.TimeoutException:
            raise ServiceUnavailableException("appointment-service", "timeout")
        except httpx.ConnectError:
            raise ServiceUnavailableException("appointment-service", "connection refused")
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTPStatusError from appointment-service: {exc}")
            raise ServiceUnavailableException("appointment-service", f"status {exc.response.status_code}")
