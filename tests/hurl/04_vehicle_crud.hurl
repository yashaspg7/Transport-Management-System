# ==============================================================================
# Vehicle API Integration Tests
# Tests creation, validation, fetching, and ensures database cleanup
# ==============================================================================

# ==============================================================================
# Test 1: Create a Prerequisite Vendor
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
  "company_name": "Vehicle Test Logistics {{newUuid}}",
  "email": "test_{{newUuid}}@example.com"
}

HTTP 201
[Captures]
vendor_id: jsonpath "$.id"
[Asserts]
duration < 2000

# ==============================================================================
# Test 2: Create a Vehicle
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vehicles/
Content-Type: application/json
Accept: application/json

{
  "vendor_id": "{{vendor_id}}",
  "registration_number": "REG-{{newUuid}}",
  "make": "Volvo",
  "model": "FH16",
  "capacity": 20.0,
  "status": "Idle"
}

HTTP 201
[Captures]
vehicle_id: jsonpath "$.id"
[Asserts]
jsonpath "$.vendor_id" == "{{vendor_id}}"
duration < 2000

# ==============================================================================
# Test 3A: Duplicate Registration Check - Initial Creation
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vehicles/
Content-Type: application/json
Accept: application/json

{
  "vendor_id": "{{vendor_id}}",
  "registration_number": "DUP-{{newUuid}}",
  "make": "Tata",
  "model": "Prima"
}

HTTP 201
[Captures]
dup_reg: jsonpath "$.registration_number"
dup_vehicle_id: jsonpath "$.id"
[Asserts]
duration < 2000

# ==============================================================================
# Test 3B: Duplicate Registration Check - Rejection
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vehicles/
Content-Type: application/json
Accept: application/json

{
  "vendor_id": "{{vendor_id}}",
  "registration_number": "{{dup_reg}}",
  "make": "Tata",
  "model": "Prima"
}

HTTP 400
[Asserts]
jsonpath "$.detail" == "A vehicle with this registration number already exists."
duration < 1000

# ==============================================================================
# Test 4: Fetch the Vehicle by ID
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vehicles/{{vehicle_id}}
Accept: application/json

HTTP 200
[Asserts]
jsonpath "$.id" == "{{vehicle_id}}"
duration < 1000

# ==============================================================================
# Test 5: Teardown - Delete Test Vehicles
# ==============================================================================

DELETE http://127.0.0.1:8000/api/v1/vehicles/{{vehicle_id}}?permanent=true
Accept: application/json

HTTP 204
[Asserts]
duration < 2000

DELETE http://127.0.0.1:8000/api/v1/vehicles/{{dup_vehicle_id}}?permanent=true
Accept: application/json

HTTP 204
[Asserts]
duration < 2000

# ==============================================================================
# Test 6: Teardown - Delete Test Vendor
# ==============================================================================

DELETE http://127.0.0.1:8000/api/v1/vendors/{{vendor_id}}?permanent=true
Accept: application/json

HTTP 204
[Asserts]
duration < 2000

# ==============================================================================
# Cleanup Summary
# All test data successfully removed from the database
# ==============================================================================