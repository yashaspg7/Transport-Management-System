# Comprehensive Vendor CRUD API Tests for Transport Management System
# Complete testing suite covering all vendor management endpoints and scenarios

# ==============================================================================
# Test 1: Create a New Vendor - Basic Success Case
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Test Logistics Inc",
    "contact_person": "John Doe",
    "email": "test-{{newUuid}}@example.com",
    "phone_number": "+1-555-1001",
    "is_active": true
}

HTTP 201
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.id" exists
jsonpath "$.company_name" == "Test Logistics Inc"
jsonpath "$.contact_person" == "John Doe"
jsonpath "$.email" contains "@example.com"
jsonpath "$.is_active" == true
jsonpath "$.created_at" exists
jsonpath "$.updated_at" exists
duration < 3000

[Captures]
vendor_id: jsonpath "$.id"
vendor_email: jsonpath "$.email"
created_at: jsonpath "$.created_at"

# ==============================================================================
# Test 2: Create Vendor - Minimal Required Fields
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Minimal Vendor Co",
    "email": "minimal-{{newUuid}}@example.com"
}

HTTP 201
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.id" exists
jsonpath "$.company_name" == "Minimal Vendor Co"
jsonpath "$.email" contains "@example.com"
jsonpath "$.contact_person" == null
jsonpath "$.phone_number" == null
jsonpath "$.is_active" == true
duration < 3000

[Captures]
minimal_vendor_id: jsonpath "$.id"

# ==============================================================================
# Test 3: Get Vendor by ID - Success
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/{{vendor_id}}
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.id" == "{{vendor_id}}"
jsonpath "$.company_name" == "Test Logistics Inc"
jsonpath "$.email" == "{{vendor_email}}"
jsonpath "$.is_active" == true
jsonpath "$.created_at" == "{{created_at}}"
duration < 1000

# ==============================================================================
# Test 4: Get Vendor by ID - Non-existent UUID
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/00000000-0000-0000-0000-000000000000
Accept: application/json

HTTP 404
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.detail" exists
jsonpath "$.detail" contains "not found"
duration < 1000

# ==============================================================================
# Test 5: List All Vendors - Default Pagination
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" isCollection
jsonpath "$" count >= 2
jsonpath "$[0].id" exists
jsonpath "$[0].company_name" exists
jsonpath "$[0].email" exists
duration < 2000

# ==============================================================================
# Test 6: List Vendors - Custom Pagination
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
skip: 0
limit: 1

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" isCollection
jsonpath "$" count <= 1
duration < 1000

# ==============================================================================
# Test 7: List Vendors - Active Only Filter
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
active_only: true
limit: 100

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" isCollection
duration < 2000

# ==============================================================================
# Test 8: Get Vendor Count
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/count
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.active_vendors_count" exists
jsonpath "$.active_vendors_count" >= 0
duration < 1000

# ==============================================================================
# Test 9: Search Vendors - Company Name
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: Test
skip: 0
limit: 10

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" isCollection
duration < 1000

# ==============================================================================
# Test 10: Search Vendors - No Results
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: NonExistentCompanyName12345
skip: 0
limit: 10

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" isCollection
jsonpath "$" count == 0
duration < 1000

# ==============================================================================
# Test 11: Get Vendor by Email - Success
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/email/{{vendor_email}}
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.id" == "{{vendor_id}}"
jsonpath "$.email" == "{{vendor_email}}"
duration < 1000

# ==============================================================================
# Test 12: Get Vendor by Email - Not Found
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/email/nonexistent@example.com
Accept: application/json

HTTP 404
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.detail" contains "not found"
duration < 1000

# ==============================================================================
# Test 13: Update Vendor - Partial Update
# ==============================================================================

PUT http://127.0.0.1:8000/api/v1/vendors/{{vendor_id}}
Content-Type: application/json
Accept: application/json

{
    "company_name": "Updated Test Logistics Inc",
    "contact_person": "Jane Smith"
}

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.id" == "{{vendor_id}}"
jsonpath "$.company_name" == "Updated Test Logistics Inc"
jsonpath "$.contact_person" == "Jane Smith"
jsonpath "$.email" == "{{vendor_email}}"
jsonpath "$.updated_at" > "{{created_at}}"
duration < 2000

[Captures]
updated_at: jsonpath "$.updated_at"

# ==============================================================================
# Test 14: Update Vendor - Full Update
# ==============================================================================

PUT http://127.0.0.1:8000/api/v1/vendors/{{minimal_vendor_id}}
Content-Type: application/json
Accept: application/json

{
    "company_name": "Fully Updated Minimal Vendor",
    "contact_person": "Updated Contact Person",
    "email": "updated-{{newUuid}}@example.com",
    "phone_number": "+1-555-1002",
    "is_active": true
}

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.company_name" == "Fully Updated Minimal Vendor"
jsonpath "$.contact_person" == "Updated Contact Person"
jsonpath "$.phone_number" == "+1-555-1002"
jsonpath "$.is_active" == true
duration < 2000

# ==============================================================================
# Test 15: Update Vendor - Non-existent ID
# ==============================================================================

PUT http://127.0.0.1:8000/api/v1/vendors/00000000-0000-0000-0000-000000000000
Content-Type: application/json
Accept: application/json

{
    "company_name": "Non-existent Vendor"
}

HTTP 404
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.detail" contains "not found"
duration < 1000

# ==============================================================================
# Test 16: Verify Update Persistence
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/{{vendor_id}}
Accept: application/json

HTTP 200
[Asserts]
jsonpath "$.company_name" == "Updated Test Logistics Inc"
jsonpath "$.contact_person" == "Jane Smith"
jsonpath "$.updated_at" == "{{updated_at}}"
duration < 1000

# ==============================================================================
# Test 17: Create Vendor - Duplicate Email (Should Fail)
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Duplicate Email Test",
    "contact_person": "Duplicate Person",
    "email": "{{vendor_email}}",
    "phone_number": "+1-555-1003",
    "is_active": true
}

HTTP 409
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.detail" contains "email already exists"
duration < 2000

# ==============================================================================
# Test 18: Create Vendor - Invalid Email Format
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Invalid Email Test",
    "email": "invalid-email-format",
    "phone_number": "+1-555-1004"
}

HTTP 422
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.detail" exists
duration < 2000

# ==============================================================================
# Test 19: Create Vendor - Empty Company Name
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "",
    "email": "empty-{{newUuid}}@example.com"
}

HTTP 422
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.detail" exists
duration < 2000

# ==============================================================================
# Test 20: Create Vendor - Missing Required Fields
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "contact_person": "Missing Required Fields"
}

HTTP 422
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.detail" exists
duration < 2000

# ==============================================================================
# Test 21: Update Vendor - Duplicate Email Constraint
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Temp Vendor for Duplicate Test",
    "email": "temp-{{newUuid}}@example.com"
}

HTTP 201
[Captures]
temp_vendor_id: jsonpath "$.id"

PUT http://127.0.0.1:8000/api/v1/vendors/{{temp_vendor_id}}
Content-Type: application/json
Accept: application/json

{
    "email": "{{vendor_email}}"
}

HTTP 409
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.detail" contains "email already exists"
duration < 2000

# ==============================================================================
# Test 22: Soft Delete Vendor (Default DELETE)
# ==============================================================================

DELETE http://127.0.0.1:8000/api/v1/vendors/{{temp_vendor_id}}

HTTP 204
[Asserts]
duration < 1000

# ==============================================================================
# Test 23: Verify Soft Delete - Vendor Still Exists but Inactive
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/{{temp_vendor_id}}
Accept: application/json

HTTP 200
[Asserts]
jsonpath "$.id" == "{{temp_vendor_id}}"
jsonpath "$.is_active" == false
duration < 1000

# ==============================================================================
# Test 24: Create Vendor for Permanent Delete Test
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Temp Vendor for Permanent Delete",
    "email": "permanent-{{newUuid}}@example.com"
}

HTTP 201
[Captures]
permanent_delete_id: jsonpath "$.id"

# ==============================================================================
# Test 25: Permanent Delete Vendor
# ==============================================================================

DELETE http://127.0.0.1:8000/api/v1/vendors/{{permanent_delete_id}}
[QueryStringParams]
permanent: true

HTTP 204
[Asserts]
duration < 1000

# ==============================================================================
# Test 26: Verify Permanent Delete - Vendor Should Not Exist
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/{{permanent_delete_id}}
Accept: application/json

HTTP 404
[Asserts]
jsonpath "$.detail" contains "not found"
duration < 1000

# ==============================================================================
# Test 27: Delete Non-existent Vendor
# ==============================================================================

DELETE http://127.0.0.1:8000/api/v1/vendors/00000000-0000-0000-0000-000000000000

HTTP 404
[Asserts]
duration < 1000

# ==============================================================================
# Test 28: Invalid Pagination Parameters - Negative Skip
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
skip: -1
limit: 10

HTTP 422
[Asserts]
jsonpath "$.detail" exists
duration < 1000

# ==============================================================================
# Test 29: Invalid Pagination Parameters - Zero Limit
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
skip: 0
limit: 0

HTTP 422
[Asserts]
jsonpath "$.detail" exists
duration < 1000

# ==============================================================================
# Test 30: Invalid Pagination Parameters - Excessive Limit
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
skip: 0
limit: 10000

HTTP 422
[Asserts]
jsonpath "$.detail" exists
duration < 1000

# ==============================================================================
# Test 31: Search with Empty Query Parameter
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q:
skip: 0
limit: 10

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" isCollection
jsonpath "$" count == 0
body == "[]"

# ==============================================================================
# Test 32: Performance Test - Create Multiple Vendors
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Performance Test Vendor 1",
    "email": "perf1-{{newUuid}}@example.com"
}

HTTP 201
[Asserts]
duration < 3000

[Captures]
perf_test_vendor_id_1: jsonpath "$.id"

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Performance Test Vendor 2",
    "email": "perf2-{{newUuid}}@example.com"
}

HTTP 201
[Asserts]
duration < 3000

[Captures]
perf_test_vendor_id_2: jsonpath "$.id"

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Performance Test Vendor 3",
    "email": "perf3-{{newUuid}}@example.com"
}

HTTP 201
[Asserts]
duration < 3000

[Captures]
perf_test_vendor_id_3: jsonpath "$.id"

# ==============================================================================
# Test 33: Final Vendor Count Verification
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/count
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.active_vendors_count" exists
jsonpath "$.active_vendors_count" >= 0
duration < 1000

# ==============================================================================
# Test 34: Search Performance Test
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: Performance
skip: 0
limit: 50

HTTP 200
[Asserts]
jsonpath "$" isCollection
jsonpath "$" count >= 3
duration < 2000

# ==============================================================================
# Test 35: Large Company Name Handling
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Very Long Company Name That Tests Maximum Length Limits And String Handling Capabilities",
    "email": "long-name-{{newUuid}}@example.com"
}

HTTP 201
[Asserts]
jsonpath "$.company_name" exists
duration < 3000

[Captures]
long_name_vendor_id: jsonpath "$.id"

# ==============================================================================
# Test 36: Clean up Test Data (Permanent Delete)
# ==============================================================================

DELETE http://127.0.0.1:8000/api/v1/vendors/{{vendor_id}}
[QueryStringParams]
permanent: true

HTTP 204

DELETE http://127.0.0.1:8000/api/v1/vendors/{{minimal_vendor_id}}
[QueryStringParams]
permanent: true

HTTP 204

DELETE http://127.0.0.1:8000/api/v1/vendors/{{long_name_vendor_id}}
[QueryStringParams]
permanent: true

HTTP 204

DELETE http://127.0.0.1:8000/api/v1/vendors/{{perf_test_vendor_id_1}}
[QueryStringParams]
permanent: true

HTTP 204

DELETE http://127.0.0.1:8000/api/v1/vendors/{{perf_test_vendor_id_2}}
[QueryStringParams]
permanent: true

HTTP 204

DELETE http://127.0.0.1:8000/api/v1/vendors/{{perf_test_vendor_id_3}}
[QueryStringParams]
permanent: true

HTTP 204

DELETE http://127.0.0.1:8000/api/v1/vendors/{{temp_vendor_id}}
[QueryStringParams]
permanent: true

HTTP 204

# ==============================================================================
# Comprehensive Vendor CRUD Test Suite Complete
# All major API endpoints, error scenarios, and edge cases covered
# ==============================================================================
