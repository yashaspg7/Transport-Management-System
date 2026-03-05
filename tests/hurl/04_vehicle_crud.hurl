# 1. Create a prerequisite Vendor
POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
{
  "company_name": "Vehicle Test Logistics {{newUuid}}",
  "email": "test_{{newUuid}}@example.com"
}
HTTP 201
[Captures]
vendor_id: jsonpath "$.id"

# 2. Create a Vehicle
POST http://127.0.0.1:8000/api/v1/vehicles/
Content-Type: application/json
{
  "vendor_id": "{{vendor_id}}",
  "registration_number": "REG-{{newUuid}}",
  "make": "Volvo",
  "model": "FH16",
  "capacity": 20.0,
  "status": "Active"
}
HTTP 201
[Captures]
vehicle_id: jsonpath "$.id"
[Asserts]
jsonpath "$.vendor_id" == "{{vendor_id}}"

# 3. Duplicate Registration Test (The "Logic" Check)
# Request A: Create a vehicle with a specific unique registration
POST http://127.0.0.1:8000/api/v1/vehicles/
Content-Type: application/json
{
  "vendor_id": "{{vendor_id}}",
  "registration_number": "DUP-{{newUuid}}",
  "make": "Tata",
  "model": "Prima"
}
HTTP 201
[Captures]
# IMPORTANT: Capture must be immediately after the status code
dup_reg: jsonpath "$.registration_number"

# Request B: Attempt to use that same registration again
POST http://127.0.0.1:8000/api/v1/vehicles/
Content-Type: application/json
{
  "vendor_id": "{{vendor_id}}",
  "registration_number": "{{dup_reg}}",
  "make": "Tata",
  "model": "Prima"
}
HTTP 400
[Asserts]
jsonpath "$.detail" == "A vehicle with this registration number already exists."

# 4. Fetch the Vehicle by ID
GET http://127.0.0.1:8000/api/v1/vehicles/{{vehicle_id}}
HTTP 200
[Asserts]
jsonpath "$.id" == "{{vehicle_id}}"