"""
Comprehensive API Test Script for Clinic Management System — Lab 3
Covers all endpoints: GET all, GET by id, POST, PUT, DELETE, PATCH actions, 404, 409, 422
Idempotent — can be run multiple times thanks to unique emails via timestamp.
"""
import sys
import datetime
import time
import requests

BASE_URL = "http://127.0.0.1:8000"
API = f"{BASE_URL}/api"

# Унікальний суфікс для кожного запуску → унікальні email
UNIQUE = str(int(time.time()))

# Counters
passed = 0
failed = 0


def ok(name):
    global passed
    passed += 1
    print(f"  ✅ PASS  {name}")


def fail(name, reason):
    global failed
    failed += 1
    print(f"  ❌ FAIL  {name}")
    print(f"            → {reason}")


def assert_status(name, response, expected):
    if response.status_code == expected:
        ok(name)
        return True
    else:
        fail(name, f"Expected HTTP {expected}, got {response.status_code}. Body: {response.text[:200]}")
        return False


def assert_field(name, data, field, expected_value=None):
    if field not in data:
        fail(name, f"Field '{field}' not found in response: {data}")
        return False
    if expected_value is not None and data[field] != expected_value:
        fail(name, f"Field '{field}': expected '{expected_value}', got '{data[field]}'")
        return False
    ok(name)
    return True


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ═══════════════════════════════════════════════════════════════════════════
#                              TESTS
# ═══════════════════════════════════════════════════════════════════════════

def test_health():
    section("HEALTH CHECK")
    r = requests.get(f"{BASE_URL}/health")
    assert_status("GET /health → 200", r, 200)


def test_doctors(ids: dict):
    section("DOCTORS")

    # --- CREATE ---
    r = requests.post(f"{API}/doctors", json={
        "first_name": "Gregory", "last_name": "House",
        "specialization": "Diagnostician",
        "hourly_rate": 100.50, "phone": f"+1234{UNIQUE[:6]}",
        "email": f"house_{UNIQUE}@clinic.com"
    })
    if not assert_status("POST /doctors → 201", r, 201):
        return
    assert_field("Doctor has id", r.json(), "id")
    ids["doctor_id"] = r.json()["id"]

    # Second doctor for specialization filter + delete test
    r2 = requests.post(f"{API}/doctors", json={
        "first_name": "James", "last_name": "Wilson",
        "specialization": "Oncologist",
        "hourly_rate": 120.00, "phone": f"+1112{UNIQUE[:6]}",
        "email": f"wilson_{UNIQUE}@clinic.com"
    })
    assert_status("POST /doctors (2nd doctor) → 201", r2, 201)
    ids["doctor2_id"] = r2.json()["id"] if r2.status_code == 201 else None

    # --- DUPLICATE EMAIL → 409 ---
    r = requests.post(f"{API}/doctors", json={
        "first_name": "Dup", "last_name": "Doctor",
        "specialization": "Test",
        "hourly_rate": 50.00, "phone": "+9999999999",
        "email": f"house_{UNIQUE}@clinic.com"
    })
    assert_status("POST /doctors (duplicate email) → 409", r, 409)

    # --- GET ALL ---
    r = requests.get(f"{API}/doctors")
    assert_status("GET /doctors → 200", r, 200)
    if r.status_code == 200 and isinstance(r.json(), list):
        ok("GET /doctors returns list")

    # --- GET by ID ---
    r = requests.get(f"{API}/doctors/{ids['doctor_id']}")
    assert_status("GET /doctors/:id → 200", r, 200)
    assert_field("Doctor id matches", r.json(), "id", ids["doctor_id"])

    # --- GET by ID – 404 ---
    r = requests.get(f"{API}/doctors/99999")
    assert_status("GET /doctors/99999 → 404", r, 404)

    # --- GET by specialization ---
    r = requests.get(f"{API}/doctors?specialization=Diagnostician")
    assert_status("GET /doctors?specialization= → 200", r, 200)
    if r.status_code == 200:
        if len(r.json()) >= 1 and r.json()[0]["specialization"] == "Diagnostician":
            ok("Specialization filter returns correct doctor")
        else:
            fail("Specialization filter", f"Unexpected result: {r.json()}")

    # --- UPDATE ---
    r = requests.put(f"{API}/doctors/{ids['doctor_id']}", json={
        "last_name": "House MD",
        "hourly_rate": 110.00,
    })
    assert_status("PUT /doctors/:id → 200", r, 200)
    assert_field("Updated last_name", r.json(), "last_name", "House MD")

    # --- DELETE 2nd doctor ---
    if ids.get("doctor2_id"):
        r = requests.delete(f"{API}/doctors/{ids['doctor2_id']}")
        assert_status("DELETE /doctors/:id → 204", r, 204)
        r = requests.get(f"{API}/doctors/{ids['doctor2_id']}")
        assert_status("GET deleted doctor → 404", r, 404)


def test_patients(ids: dict):
    section("PATIENTS")

    # --- CREATE ---
    r = requests.post(f"{API}/patients", json={
        "first_name": "John", "last_name": "Doe",
        "date_of_birth": "1990-05-15",
        "phone": f"+1987{UNIQUE[:6]}", "email": f"john_{UNIQUE}@example.com"
    })
    if not assert_status("POST /patients → 201", r, 201):
        return
    assert_field("Patient has id", r.json(), "id")
    ids["patient_id"] = r.json()["id"]

    # --- CREATE second patient for delete test ---
    r2 = requests.post(f"{API}/patients", json={
        "first_name": "Jane", "last_name": "Smith",
        "date_of_birth": "1985-03-22",
        "phone": f"+1555{UNIQUE[:6]}", "email": f"jane_{UNIQUE}@example.com"
    })
    assert_status("POST /patients (2nd for delete) → 201", r2, 201)
    delete_patient_id = r2.json()["id"] if r2.status_code == 201 else None

    # --- DUPLICATE EMAIL → 409 ---
    r = requests.post(f"{API}/patients", json={
        "first_name": "Dup", "last_name": "Patient",
        "date_of_birth": "2000-01-01",
        "phone": "+1000000000", "email": f"john_{UNIQUE}@example.com"
    })
    assert_status("POST /patients (duplicate email) → 409", r, 409)

    # --- GET ALL ---
    r = requests.get(f"{API}/patients")
    assert_status("GET /patients → 200", r, 200)
    if r.status_code == 200 and len(r.json()) >= 2:
        ok("GET /patients list not empty")

    # --- GET by ID ---
    r = requests.get(f"{API}/patients/{ids['patient_id']}")
    assert_status("GET /patients/:id → 200", r, 200)
    assert_field("Patient first_name matches", r.json(), "first_name", "John")

    # --- GET by ID – 404 ---
    r = requests.get(f"{API}/patients/99999")
    assert_status("GET /patients/99999 → 404", r, 404)

    # --- UPDATE ---
    r = requests.put(f"{API}/patients/{ids['patient_id']}", json={
        "first_name": "Johnny",
    })
    assert_status("PUT /patients/:id → 200", r, 200)
    assert_field("Updated first_name", r.json(), "first_name", "Johnny")

    # --- DELETE ---
    if delete_patient_id:
        r = requests.delete(f"{API}/patients/{delete_patient_id}")
        assert_status("DELETE /patients/:id → 204", r, 204)
        r = requests.get(f"{API}/patients/{delete_patient_id}")
        assert_status("GET deleted patient → 404", r, 404)


def test_visits(ids: dict):
    section("VISITS")
    future = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)).isoformat()
    future2 = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)).isoformat()

    # --- CREATE ---
    r = requests.post(f"{API}/visits", json={
        "patient_id": ids["patient_id"],
        "doctor_id": ids["doctor_id"],
        "scheduled_at": future,
        "duration_minutes": 30,
        "reason": "Leg pain consultation"
    })
    if not assert_status("POST /visits → 201", r, 201):
        return
    assert_field("Visit has id", r.json(), "id")
    assert_field("Visit status is scheduled", r.json(), "status", "scheduled")
    ids["visit_id"] = r.json()["id"]

    # --- CONFLICT visit (same doctor, same time) → 409 ---
    r = requests.post(f"{API}/visits", json={
        "patient_id": ids["patient_id"],
        "doctor_id": ids["doctor_id"],
        "scheduled_at": future,
        "duration_minutes": 30,
        "reason": "Overlapping visit"
    })
    assert_status("POST /visits (conflict) → 409", r, 409)

    # --- VISIT IN THE PAST → 422 ---
    r = requests.post(f"{API}/visits", json={
        "patient_id": ids["patient_id"],
        "doctor_id": ids["doctor_id"],
        "scheduled_at": "2020-01-01T00:00:00Z",
        "duration_minutes": 30,
        "reason": "Past visit"
    })
    assert_status("POST /visits (past time) → 422", r, 422)

    # --- CREATE second visit for cancel test ---
    r2 = requests.post(f"{API}/visits", json={
        "patient_id": ids["patient_id"],
        "doctor_id": ids["doctor_id"],
        "scheduled_at": future2,
        "duration_minutes": 45,
        "reason": "Follow up"
    })
    assert_status("POST /visits (2nd for cancel) → 201", r2, 201)
    cancel_visit_id = r2.json()["id"] if r2.status_code == 201 else None

    # --- GET ALL ---
    r = requests.get(f"{API}/visits")
    assert_status("GET /visits → 200", r, 200)

    # --- GET by patient_id filter ---
    r = requests.get(f"{API}/visits?patient_id={ids['patient_id']}")
    assert_status("GET /visits?patient_id= → 200", r, 200)
    if r.status_code == 200 and len(r.json()) >= 1:
        ok("Patient visits filter returned results")

    # --- GET by doctor_id filter ---
    r = requests.get(f"{API}/visits?doctor_id={ids['doctor_id']}")
    assert_status("GET /visits?doctor_id= → 200", r, 200)

    # --- GET by ID ---
    r = requests.get(f"{API}/visits/{ids['visit_id']}")
    assert_status("GET /visits/:id → 200", r, 200)
    assert_field("Visit patient_id matches", r.json(), "patient_id", ids["patient_id"])

    # --- GET by ID – 404 ---
    r = requests.get(f"{API}/visits/99999")
    assert_status("GET /visits/99999 → 404", r, 404)

    # --- COMPLETE ---
    r = requests.patch(f"{API}/visits/{ids['visit_id']}/complete")
    assert_status("PATCH /visits/:id/complete → 200", r, 200)
    assert_field("Visit status is completed", r.json(), "status", "completed")

    # --- CANCEL second visit ---
    if cancel_visit_id:
        r = requests.patch(f"{API}/visits/{cancel_visit_id}/cancel")
        assert_status("PATCH /visits/:id/cancel → 200", r, 200)
        assert_field("Visit status is cancelled", r.json(), "status", "cancelled")

    # --- COMPLETE on cancelled → 422 ---
    if cancel_visit_id:
        r = requests.patch(f"{API}/visits/{cancel_visit_id}/complete")
        assert_status("PATCH /visits/:id/complete on cancelled → 422", r, 422)

    # --- COMPLETE on non-existent → 404 ---
    r = requests.patch(f"{API}/visits/99999/complete")
    assert_status("PATCH /visits/99999/complete → 404", r, 404)


def test_diagnoses(ids: dict):
    section("DIAGNOSES")

    # Creating diagnosis on a non-completed visit → 422
    future3 = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=6)).isoformat()
    r_tmp = requests.post(f"{API}/visits", json={
        "patient_id": ids["patient_id"],
        "doctor_id": ids["doctor_id"],
        "scheduled_at": future3,
        "duration_minutes": 20,
        "reason": "Temp visit for diagnosis test"
    })
    if r_tmp.status_code == 201:
        tmp_visit_id = r_tmp.json()["id"]
        r = requests.post(f"{API}/diagnoses", json={
            "visit_id": tmp_visit_id,
            "icd_code": "A00.0",
            "title": "Cholera",
            "severity": "severe"
        })
        assert_status("POST /diagnoses on non-completed visit → 422", r, 422)

    # --- CREATE on completed visit ---
    r = requests.post(f"{API}/diagnoses", json={
        "visit_id": ids["visit_id"],
        "icd_code": "M79.6",
        "title": "Pain in limb",
        "severity": "moderate",
        "description": "Chronic leg pain"
    })
    if not assert_status("POST /diagnoses (on completed visit) → 201", r, 201):
        return
    assert_field("Diagnosis has id", r.json(), "id")
    ids["diagnosis_id"] = r.json()["id"]

    # --- DUPLICATE diagnosis → 422 ---
    r = requests.post(f"{API}/diagnoses", json={
        "visit_id": ids["visit_id"],
        "icd_code": "J06.9",
        "title": "ARI",
        "severity": "mild"
    })
    assert_status("POST /diagnoses (duplicate) → 422", r, 422)

    # --- GET ALL ---
    r = requests.get(f"{API}/diagnoses")
    assert_status("GET /diagnoses → 200", r, 200)

    # --- GET by ID ---
    r = requests.get(f"{API}/diagnoses/{ids['diagnosis_id']}")
    assert_status("GET /diagnoses/:id → 200", r, 200)
    assert_field("Diagnosis icd_code matches", r.json(), "icd_code", "M79.6")

    # --- GET by ID – 404 ---
    r = requests.get(f"{API}/diagnoses/99999")
    assert_status("GET /diagnoses/99999 → 404", r, 404)

    # --- GET by visit_id filter ---
    r = requests.get(f"{API}/diagnoses?visit_id={ids['visit_id']}")
    assert_status("GET /diagnoses?visit_id= → 200", r, 200)


def test_prescriptions(ids: dict):
    section("PRESCRIPTIONS")

    # --- CREATE ---
    r = requests.post(f"{API}/prescriptions", json={
        "diagnosis_id": ids["diagnosis_id"],
        "medication_name": "Ibuprofen",
        "dosage": "400mg",
        "frequency": "Twice a day",
        "duration_days": 5,
        "cost": 15.50
    })
    if not assert_status("POST /prescriptions → 201", r, 201):
        return
    assert_field("Prescription has id", r.json(), "id")
    ids["prescription_id"] = r.json()["id"]

    # Second prescription for delete test
    r2 = requests.post(f"{API}/prescriptions", json={
        "diagnosis_id": ids["diagnosis_id"],
        "medication_name": "Paracetamol",
        "dosage": "500mg",
        "frequency": "Three times a day",
        "duration_days": 3,
        "cost": 8.00
    })
    assert_status("POST /prescriptions (2nd) → 201", r2, 201)
    delete_presc_id = r2.json()["id"] if r2.status_code == 201 else None

    # --- GET ALL ---
    r = requests.get(f"{API}/prescriptions")
    assert_status("GET /prescriptions → 200", r, 200)
    if r.status_code == 200 and len(r.json()) >= 2:
        ok("GET /prescriptions list has >= 2 items")

    # --- GET by ID ---
    r = requests.get(f"{API}/prescriptions/{ids['prescription_id']}")
    assert_status("GET /prescriptions/:id → 200", r, 200)
    assert_field("Prescription medication matches", r.json(), "medication_name", "Ibuprofen")

    # --- GET by ID – 404 ---
    r = requests.get(f"{API}/prescriptions/99999")
    assert_status("GET /prescriptions/99999 → 404", r, 404)

    # --- GET by diagnosis_id filter ---
    r = requests.get(f"{API}/prescriptions?diagnosis_id={ids['diagnosis_id']}")
    assert_status("GET /prescriptions?diagnosis_id= → 200", r, 200)
    if r.status_code == 200 and len(r.json()) >= 2:
        ok("Prescription filter by diagnosis_id returned >= 2 items")

    # --- DELETE ---
    if delete_presc_id:
        r = requests.delete(f"{API}/prescriptions/{delete_presc_id}")
        assert_status("DELETE /prescriptions/:id → 204", r, 204)
        r = requests.get(f"{API}/prescriptions/{delete_presc_id}")
        assert_status("GET deleted prescription → 404", r, 404)


def test_payments(ids: dict):
    section("PAYMENTS")

    # --- CREATE on non-completed visit → 422 ---
    future4 = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)).isoformat()
    r_tmp = requests.post(f"{API}/visits", json={
        "patient_id": ids["patient_id"],
        "doctor_id": ids["doctor_id"],
        "scheduled_at": future4,
        "duration_minutes": 20,
        "reason": "Uncompleted visit"
    })
    if r_tmp.status_code == 201:
        r = requests.post(f"{API}/payments", json={"visit_id": r_tmp.json()["id"]})
        assert_status("POST /payments on non-completed visit → 422", r, 422)

    # --- CREATE ---
    r = requests.post(f"{API}/payments", json={"visit_id": ids["visit_id"]})
    if not assert_status("POST /payments → 201", r, 201):
        return
    assert_field("Payment has id", r.json(), "id")
    assert_field("Payment has amount", r.json(), "amount")
    assert_field("Payment status is pending", r.json(), "status", "pending")
    ids["payment_id"] = r.json()["id"]

    # --- DUPLICATE payment → 422 ---
    r = requests.post(f"{API}/payments", json={"visit_id": ids["visit_id"]})
    assert_status("POST /payments (duplicate) → 422", r, 422)

    # --- GET ALL ---
    r = requests.get(f"{API}/payments")
    assert_status("GET /payments → 200", r, 200)

    # --- GET by ID ---
    r = requests.get(f"{API}/payments/{ids['payment_id']}")
    assert_status("GET /payments/:id → 200", r, 200)
    assert_field("Payment visit_id matches", r.json(), "visit_id", ids["visit_id"])

    # --- GET by ID – 404 ---
    r = requests.get(f"{API}/payments/99999")
    assert_status("GET /payments/99999 → 404", r, 404)

    # --- GET by patient_id filter ---
    r = requests.get(f"{API}/payments?patient_id={ids['patient_id']}")
    assert_status("GET /payments?patient_id= → 200", r, 200)
    if r.status_code == 200 and len(r.json()) >= 1:
        ok("Payment filter by patient_id returned result")

    # --- CANCEL ---
    r = requests.patch(f"{API}/payments/{ids['payment_id']}/cancel")
    assert_status("PATCH /payments/:id/cancel → 200", r, 200)
    assert_field("Payment status is cancelled", r.json(), "status", "cancelled")

    # --- PAY a cancelled payment → 422 ---
    r = requests.patch(f"{API}/payments/{ids['payment_id']}/pay")
    assert_status("PATCH /payments/:id/pay on cancelled → 422", r, 422)


def test_treatment_history(ids: dict):
    section("TREATMENT HISTORY")

    # --- GET for patient_id ---
    r = requests.get(f"{API}/treatment-history/{ids['patient_id']}")
    assert_status("GET /treatment-history/:patient_id → 200", r, 200)
    if r.status_code == 200:
        data = r.json()
        assert_field("History has patient_id", data, "patient_id", ids["patient_id"])
        assert_field("History has total_visits", data, "total_visits")
        assert_field("History has visits list", data, "visits")
        if data.get("visits") and len(data["visits"]) > 0:
            first = data["visits"][0]
            assert_field("Visit in history has diagnosis field", first, "diagnosis")
            assert_field("Visit in history has prescriptions field", first, "prescriptions")

    # --- GET for non-existent patient → 404 ---
    r = requests.get(f"{API}/treatment-history/99999")
    assert_status("GET /treatment-history/99999 → 404", r, 404)


# ═══════════════════════════════════════════════════════════════════════════
#                              MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    try:
        requests.get(BASE_URL, timeout=3)
    except requests.ConnectionError:
        print(f"\n❌  Cannot connect to server at {BASE_URL}")
        print("   Start the server: uvicorn app.main:app --reload")
        sys.exit(1)

    print(f"\n  Run ID: {UNIQUE}  (unique suffix for emails)\n")

    ids = {}  # shared state, filled by each test step

    test_health()
    test_doctors(ids)
    test_patients(ids)

    # Guard: if setup failed we cannot test dependent endpoints
    if "doctor_id" not in ids or "patient_id" not in ids:
        print("\n❌  Doctor or Patient creation failed – aborting remaining tests.")
        sys.exit(1)

    test_visits(ids)

    if "visit_id" not in ids:
        print("\n❌  Visit creation failed – aborting remaining tests.")
        sys.exit(1)

    test_diagnoses(ids)

    if "diagnosis_id" not in ids:
        print("\n❌  Diagnosis creation failed – aborting remaining tests.")
        sys.exit(1)

    test_prescriptions(ids)
    test_payments(ids)
    test_treatment_history(ids)

    # ── Summary ──────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*60}")
    print(f"  RESULTS: {passed}/{total} passed  |  {failed} failed")
    print(f"{'='*60}\n")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
