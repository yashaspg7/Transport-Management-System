# Performance and Load Testing for Transport Management System
# Tests API performance, response times, and load handling capabilities

# ==============================================================================
# Test 1: Response Time Baseline - Single Request
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
limit: 10

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
duration < 1000
jsonpath "$" isCollection

# ==============================================================================
# Test 2: Large Dataset Retrieval Performance
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
skip: 0
limit: 100

HTTP 200
[Asserts]
duration < 5000
jsonpath "$" isCollection
jsonpath "$" count <= 100

# ==============================================================================
# Test 3: Create Vendor Performance Baseline
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Performance Test Vendor 1",
    "contact_person": "Perf Tester",
    "email": "perf1@example.com",
    "phone_number": "+1-555-2001",
    "is_active": true
}

HTTP 201
[Asserts]
duration < 5000
jsonpath "$.id" exists

[Captures]
perf_vendor_id_1: jsonpath "$.id"

# ==============================================================================
# Test 4: Rapid Sequential Create Requests
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Performance Test Vendor 2",
    "contact_person": "Perf Tester 2",
    "email": "perf2@example.com",
    "phone_number": "+1-555-2002",
    "is_active": true
}

HTTP 201
[Asserts]
duration < 5000

[Captures]
perf_vendor_id_2: jsonpath "$.id"

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Performance Test Vendor 3",
    "contact_person": "Perf Tester 3",
    "email": "perf3@example.com",
    "phone_number": "+1-555-2003",
    "is_active": true
}

HTTP 201
[Asserts]
duration < 5000

[Captures]
perf_vendor_id_3: jsonpath "$.id"

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Performance Test Vendor 4",
    "contact_person": "Perf Tester 4",
    "email": "perf4@example.com",
    "phone_number": "+1-555-2004",
    "is_active": true
}

HTTP 201
[Asserts]
duration < 5000

[Captures]
perf_vendor_id_4: jsonpath "$.id"

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Performance Test Vendor 5",
    "contact_person": "Perf Tester 5",
    "email": "perf5@example.com",
    "phone_number": "+1-555-2005",
    "is_active": true
}

HTTP 201
[Asserts]
duration < 5000

[Captures]
perf_vendor_id_5: jsonpath "$.id"

# ==============================================================================
# Test 5: Large Payload Performance Test
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Large Payload Performance Test Company With Very Long Name That Exceeds Normal Length But Still Within Limits To Test Performance Impact",
    "contact_person": "Very Long Contact Person Name That Tests The Performance Impact Of Large String Fields In Database Operations And JSON Serialization",
    "email": "very.long.email.address.for.performance.testing@example.com",
    "phone_number": "+1-555-LARGE",
    "is_active": true
}

HTTP 201
[Asserts]
duration < 5000
jsonpath "$.company_name" contains "Large Payload"

[Captures]
large_payload_vendor_id: jsonpath "$.id"

# ==============================================================================
# Test 6: Rapid Read Operations Performance
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_1}}
Accept: application/json

HTTP 200
[Asserts]
duration < 1000

GET http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_5}}
Accept: application/json

HTTP 200
[Asserts]
duration < 1000

GET http://127.0.0.1:8000/api/v1/vendors/{{large_payload_vendor_id}}
Accept: application/json

HTTP 200
[Asserts]
duration < 1000

# ==============================================================================
# Test 7: Search Performance with Various Query Lengths
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: P
limit: 50

HTTP 200
[Asserts]
duration < 5000
jsonpath "$" isCollection

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: Performance
limit: 50

HTTP 200
[Asserts]
duration < 5000
jsonpath "$" isCollection

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: Performance Test Company
limit: 50

HTTP 200
[Asserts]
duration < 5000
jsonpath "$" isCollection

# ==============================================================================
# Test 8: Update Performance Test
# ==============================================================================

PUT http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_1}}
Content-Type: application/json
Accept: application/json

{
    "company_name": "Updated Performance Test Vendor 1",
    "contact_person": "Updated Perf Tester",
    "phone_number": "+1-555-UPD1"
}

HTTP 200
[Asserts]
duration < 5000
jsonpath "$.company_name" == "Updated Performance Test Vendor 1"

# ==============================================================================
# Test 9: Large Update Payload Performance
# ==============================================================================

PUT http://127.0.0.1:8000/api/v1/vendors/{{large_payload_vendor_id}}
Content-Type: application/json
Accept: application/json

{
    "company_name": "Updated Large Payload Performance Test Company With Even Longer Name That Tests The Performance Impact Of Large Updates And Database Write Operations",
    "contact_person": "Updated Very Long Contact Person Name That Tests Update Performance With Large String Fields And JSON Processing Overhead",
    "phone_number": "+1-555-UPDLRG"
}

HTTP 200
[Asserts]
duration < 5000
jsonpath "$.company_name" contains "Updated Large Payload"

# ==============================================================================
# Test 10: Pagination Performance Under Load
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
skip: 0
limit: 50

HTTP 200
[Asserts]
duration < 5000

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
skip: 50
limit: 50

HTTP 200
[Asserts]
duration < 5000

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
skip: 100
limit: 50

HTTP 200
[Asserts]
duration < 5000

# ==============================================================================
# Test 11: Concurrent-like Sequential Operations
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/count
Accept: application/json

HTTP 200
[Asserts]
duration < 1000

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
active_only: true
limit: 20

HTTP 200
[Asserts]
duration < 1000

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: Test
limit: 20

HTTP 200
[Asserts]
duration < 1000

# ==============================================================================
# Test 12: Memory Pressure Test - Large Result Set
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
skip: 0
limit: 1000

HTTP 200
[Asserts]
duration < 10000
jsonpath "$" isCollection

# ==============================================================================
# Test 13: Database Connection Pool Test
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_1}}
Accept: application/json

HTTP 200

GET http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_5}}
Accept: application/json

HTTP 200

GET http://127.0.0.1:8000/api/v1/vendors/{{large_payload_vendor_id}}
Accept: application/json

HTTP 200

GET http://127.0.0.1:8000/api/v1/vendors/count
Accept: application/json

HTTP 200

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
limit: 5

HTTP 200
[Asserts]
# All requests should complete within reasonable time
duration < 5000

# ==============================================================================
# Test 14: API Health Under Load
# ==============================================================================

GET http://127.0.0.1:8000/health
Accept: application/json

HTTP 200
[Asserts]
duration < 1000
jsonpath "$.status" == "healthy"

# ==============================================================================
# Test 15: Error Handling Performance
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/00000000-0000-0000-0000-000000000000
Accept: application/json

HTTP 404
[Asserts]
duration < 1000
jsonpath "$.detail" contains "not found"

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "",
    "email": "invalid-email"
}

HTTP 422
[Asserts]
duration < 1000
jsonpath "$.detail" exists

# ==============================================================================
# Test 16: Cleanup Performance Test
# ==============================================================================

DELETE http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_1}}
[QueryStringParams]
permanent: true

HTTP 204
[Asserts]
duration < 1000

DELETE http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_2}}
[QueryStringParams]
permanent: true

HTTP 204
[Asserts]
duration < 1000

DELETE http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_3}}
[QueryStringParams]
permanent: true

HTTP 204
[Asserts]
duration < 1000

DELETE http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_4}}
[QueryStringParams]
permanent: true

HTTP 204
[Asserts]
duration < 1000

DELETE http://127.0.0.1:8000/api/v1/vendors/{{perf_vendor_id_5}}
[QueryStringParams]
permanent: true

HTTP 204
[Asserts]
duration < 1000

DELETE http://127.0.0.1:8000/api/v1/vendors/{{large_payload_vendor_id}}
[QueryStringParams]
permanent: true

HTTP 204
[Asserts]
duration < 1000

# ==============================================================================
# Test 17: Post-Cleanup Verification Performance
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/count
Accept: application/json

HTTP 200
[Asserts]
duration < 1000
jsonpath "$.active_vendors_count" exists

# ==============================================================================
# Test 18: Stress Test - Rapid Fire Requests
# ==============================================================================

GET http://127.0.0.1:8000/health
HTTP 200

GET http://127.0.0.1:8000/api/v1/vendors/count
HTTP 200

GET http://127.0.0.1:8000/health
HTTP 200

GET http://127.0.0.1:8000/api/v1/vendors/count
HTTP 200

GET http://127.0.0.1:8000/health
HTTP 200

GET http://127.0.0.1:8000/api/v1/vendors/count
HTTP 200
[Asserts]
# Final stress test assertion
duration < 5000
jsonpath "$.active_vendors_count" exists

# ==============================================================================
# Performance Test Summary
# All tests completed - Review durations and optimize bottlenecks
# ==============================================================================
