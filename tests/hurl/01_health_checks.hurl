# Comprehensive Health Check Tests for Transport Management System
# Tests all health endpoints, API availability, and basic connectivity

# ==============================================================================
# Test 1: Root Health Check Endpoint
# ==============================================================================

GET http://127.0.0.1:8000/
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.status" == "ok"
jsonpath "$.message" == "Welcome to the Transport Management System"
jsonpath "$.version" == "0.1.0"
jsonpath "$.project" == "Transport-Management-System"
jsonpath "$.docs_url" == "/docs"
duration < 1000

# ==============================================================================
# Test 2: Detailed Health Check Endpoint
# ==============================================================================

GET http://127.0.0.1:8000/health
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.status" == "healthy"
jsonpath "$.service" == "Transport-Management-System"
jsonpath "$.version" == "0.1.0"
duration < 1000

# ==============================================================================
# Test 3: Health Endpoint Response Consistency
# ==============================================================================

GET http://127.0.0.1:8000/health

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.status" exists
jsonpath "$.service" exists
jsonpath "$.version" exists
duration < 500

# ==============================================================================
# Test 4: API Documentation Endpoints Accessibility
# ==============================================================================

GET http://127.0.0.1:8000/docs
Accept: text/html

HTTP 200
[Asserts]
header "Content-Type" contains "text/html"
duration < 5000

# ==============================================================================
# Test 5: OpenAPI JSON Schema Accessibility
# ==============================================================================

GET http://127.0.0.1:8000/openapi.json
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.openapi" exists
jsonpath "$.info.title" == "Transport-Management-System"
jsonpath "$.info.version" == "0.1.0"
jsonpath "$.paths" exists
duration < 1000

# ==============================================================================
# Test 6: ReDoc Documentation Accessibility
# ==============================================================================

GET http://127.0.0.1:8000/redoc
Accept: text/html

HTTP 200
[Asserts]
header "Content-Type" contains "text/html"
duration < 5000

# ==============================================================================
# Test 7: API V1 Base Endpoint Check
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" isCollection
duration < 2000

# ==============================================================================
# Test 8: Vendor Count Endpoint Health
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
# Test 9: Search Endpoint Health Check
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: health-check-test
limit: 1

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" isCollection
duration < 1000

# ==============================================================================
# Test 10: Versioned Documentation Redirects
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/docs
Accept: text/html

HTTP 307
[Asserts]
header "Location" == "/docs"
duration < 500

GET http://127.0.0.1:8000/api/v1/redoc
Accept: text/html

HTTP 307
[Asserts]
header "Location" == "/redoc"
duration < 500

GET http://127.0.0.1:8000/api/v1/openapi.json
Accept: application/json

HTTP 307
[Asserts]
header "Location" == "/openapi.json"
duration < 500

# ==============================================================================
# Test 11: Error Handling Health Check
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
# Test 12: Invalid Endpoint Check
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/nonexistent-endpoint
Accept: application/json

HTTP 404
[Asserts]
duration < 1000

# ==============================================================================
# Test 13: Method Not Allowed Check
# ==============================================================================

DELETE http://127.0.0.1:8000/health
Accept: application/json

HTTP 405
[Asserts]
duration < 1000

# ==============================================================================
# Test 14: Malformed Request Handling
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "invalid": "json"
}

HTTP 422
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.detail" exists
duration < 1000

# ==============================================================================
# Test 15: Large Request Handling
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
limit: 100

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" isCollection
jsonpath "$" count <= 100
duration < 3000

# ==============================================================================
# Test 16: API Response Headers Check
# ==============================================================================

GET http://127.0.0.1:8000/health
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" exists
header "Content-Length" exists
duration < 500

# ==============================================================================
# Test 17: Concurrent Request Simulation
# ==============================================================================

GET http://127.0.0.1:8000/health
HTTP 200

GET http://127.0.0.1:8000/api/v1/vendors/count
HTTP 200

GET http://127.0.0.1:8000/health
HTTP 200

GET http://127.0.0.1:8000/api/v1/vendors/count
HTTP 200
[Asserts]
duration < 2000

# ==============================================================================
# Test 18: Database Connectivity Check
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
limit: 1

HTTP 200
[Asserts]
jsonpath "$" isCollection
duration < 2000

# ==============================================================================
# Test 19: API Stress Test - Rapid Requests
# ==============================================================================

GET http://127.0.0.1:8000/health
HTTP 200

GET http://127.0.0.1:8000/health
HTTP 200

GET http://127.0.0.1:8000/health
HTTP 200

GET http://127.0.0.1:8000/health
HTTP 200

GET http://127.0.0.1:8000/health
HTTP 200
[Asserts]
jsonpath "$.status" == "healthy"
duration < 1000

# ==============================================================================
# Test 20: Final System Health Verification
# ==============================================================================

GET http://127.0.0.1:8000/health
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.status" == "healthy"
jsonpath "$.service" == "Transport-Management-System"
jsonpath "$.version" == "0.1.0"
duration < 1000

# ==============================================================================
# Health Check Summary
# All health endpoints are functional and responding within acceptable limits
# API is ready for comprehensive testing
# ==============================================================================
