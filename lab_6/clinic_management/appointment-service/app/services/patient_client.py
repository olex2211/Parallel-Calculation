import httpx
import logging

from app.core.config import settings
from app.core.exceptions import EntityNotFoundException, ServiceUnavailableException
from app.schemas.external import ExternalDoctorResponse, ExternalPatientResponse

logger = logging.getLogger(__name__)


class PatientClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
        self.base_url = settings.PATIENT_SERVICE_URL

    async def get_patient(self, patient_id: int) -> ExternalPatientResponse:
        url = f"{self.base_url}{settings.API_PREFIX}/patients/{patient_id}"
        try:
            response = await self._client.get(url)
            if response.status_code == 404:
                raise EntityNotFoundException("Patient", patient_id)
            response.raise_for_status()
            logger.info(f"Got patient {patient_id} from patient-service")
            return ExternalPatientResponse(**response.json())
        except httpx.TimeoutException:
            raise ServiceUnavailableException("patient-service", "timeout")
        except httpx.ConnectError:
            raise ServiceUnavailableException("patient-service", "connection refused")
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTPStatusError from patient-service: {exc}")
            raise ServiceUnavailableException("patient-service", f"status {exc.response.status_code}")

    async def get_doctor(self, doctor_id: int) -> ExternalDoctorResponse:
        url = f"{self.base_url}{settings.API_PREFIX}/doctors/{doctor_id}"
        try:
            response = await self._client.get(url)
            if response.status_code == 404:
                raise EntityNotFoundException("Doctor", doctor_id)
            response.raise_for_status()
            logger.info(f"Got doctor {doctor_id} from patient-service")
            return ExternalDoctorResponse(**response.json())
        except httpx.TimeoutException:
            raise ServiceUnavailableException("patient-service", "timeout")
        except httpx.ConnectError:
            raise ServiceUnavailableException("patient-service", "connection refused")
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTPStatusError from patient-service: {exc}")
            raise ServiceUnavailableException("patient-service", f"status {exc.response.status_code}")
