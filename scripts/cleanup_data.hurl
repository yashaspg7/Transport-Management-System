# Database Cleanup Script for Transport Management System
# Removes all seeded vendor data to reset the database to a clean state

# ==============================================================================
# Step 1: Check Current Database State
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/count
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.active_vendors_count" exists

[Captures]
initial_count: jsonpath "$.active_vendors_count"

# ==============================================================================
# Step 2: Clean Up Seed Data Vendors
# ==============================================================================

# Swift Transport Solutions
GET http://127.0.0.1:8000/api/v1/vendors/email/john.smith@swifttransport.com
Accept: application/json

HTTP *
[Captures]
swift_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{swift_id}}
[QueryStringParams]
permanent: true

HTTP *

# Global Logistics Corp
GET http://127.0.0.1:8000/api/v1/vendors/email/sarah.j@globallogistics.com
Accept: application/json

HTTP *
[Captures]
global_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{global_id}}
[QueryStringParams]
permanent: true

HTTP *

# Metro Freight Services
GET http://127.0.0.1:8000/api/v1/vendors/email/m.davis@metrofreight.com
Accept: application/json

HTTP *
[Captures]
metro_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{metro_id}}
[QueryStringParams]
permanent: true

HTTP *

# Express Cargo Ltd
GET http://127.0.0.1:8000/api/v1/vendors/email/emily.wilson@expresscargo.com
Accept: application/json

HTTP *
[Captures]
express_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{express_id}}
[QueryStringParams]
permanent: true

HTTP *

# Prime Shipping Co
GET http://127.0.0.1:8000/api/v1/vendors/email/r.brown@primeshipping.com
Accept: application/json

HTTP *
[Captures]
prime_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{prime_id}}
[QueryStringParams]
permanent: true

HTTP *

# Reliable Transport Inc
GET http://127.0.0.1:8000/api/v1/vendors/email/l.anderson@reliabletransport.com
Accept: application/json

HTTP *
[Captures]
reliable_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{reliable_id}}
[QueryStringParams]
permanent: true

HTTP *

# Fast Track Logistics
GET http://127.0.0.1:8000/api/v1/vendors/email/d.martinez@fasttrack.com
Accept: application/json

HTTP *
[Captures]
fasttrack_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{fasttrack_id}}
[QueryStringParams]
permanent: true

HTTP *

# Blue Ocean Shipping
GET http://127.0.0.1:8000/api/v1/vendors/email/j.taylor@blueocean.com
Accept: application/json

HTTP *
[Captures]
blueocean_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{blueocean_id}}
[QueryStringParams]
permanent: true

HTTP *

# Mountain View Transport
GET http://127.0.0.1:8000/api/v1/vendors/email/c.lee@mountainview.com
Accept: application/json

HTTP *
[Captures]
mountain_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{mountain_id}}
[QueryStringParams]
permanent: true

HTTP *

# City Express Delivery
GET http://127.0.0.1:8000/api/v1/vendors/email/a.clark@cityexpress.com
Accept: application/json

HTTP *
[Captures]
city_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{city_id}}
[QueryStringParams]
permanent: true

HTTP *

# Interstate Cargo Solutions
GET http://127.0.0.1:8000/api/v1/vendors/email/k.rodriguez@interstate.com
Accept: application/json

HTTP *
[Captures]
interstate_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{interstate_id}}
[QueryStringParams]
permanent: true

HTTP *

# Atlantic Freight Lines
GET http://127.0.0.1:8000/api/v1/vendors/email/m.garcia@atlanticfreight.com
Accept: application/json

HTTP *
[Captures]
atlantic_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{atlantic_id}}
[QueryStringParams]
permanent: true

HTTP *

# West Coast Logistics
GET http://127.0.0.1:8000/api/v1/vendors/email/t.anderson@westcoast.com
Accept: application/json

HTTP *
[Captures]
westcoast_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{westcoast_id}}
[QueryStringParams]
permanent: true

HTTP *

# Northern Transport Co
GET http://127.0.0.1:8000/api/v1/vendors/email/info@northerntransport.com
Accept: application/json

HTTP *
[Captures]
northern_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{northern_id}}
[QueryStringParams]
permanent: true

HTTP *

# Southern Shipping Services
GET http://127.0.0.1:8000/api/v1/vendors/email/m.thompson@southernship.com
Accept: application/json

HTTP *
[Captures]
southern_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{southern_id}}
[QueryStringParams]
permanent: true

HTTP *

# Coastal Maritime Transport
GET http://127.0.0.1:8000/api/v1/vendors/email/p.wilson@coastalmaritime.com
Accept: application/json

HTTP *
[Captures]
coastal_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{coastal_id}}
[QueryStringParams]
permanent: true

HTTP *

# Desert Eagle Freight
GET http://127.0.0.1:8000/api/v1/vendors/email/carlos.mendez@deserteagle.com
Accept: application/json

HTTP *
[Captures]
desert_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{desert_id}}
[QueryStringParams]
permanent: true

HTTP *

# Lakeside Logistics Hub
GET http://127.0.0.1:8000/api/v1/vendors/email/rachel.green@lakesidelogistics.com
Accept: application/json

HTTP *
[Captures]
lakeside_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{lakeside_id}}
[QueryStringParams]
permanent: true

HTTP *

# Valley Transport Network
GET http://127.0.0.1:8000/api/v1/vendors/email/s.park@valleytransport.com
Accept: application/json

HTTP *
[Captures]
valley_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{valley_id}}
[QueryStringParams]
permanent: true

HTTP *

# Skyline Cargo Services
GET http://127.0.0.1:8000/api/v1/vendors/email/diana.foster@skylinecargo.com
Accept: application/json

HTTP *
[Captures]
skyline_id: jsonpath "$.id"

DELETE http://127.0.0.1:8000/api/v1/vendors/{{skyline_id}}
[QueryStringParams]
permanent: true

HTTP *

# ==============================================================================
# Step 3: Clean Up Any Remaining Test Vendors
# ==============================================================================

# Search for any remaining test vendors
GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: Test
limit: 100

HTTP 200
[Asserts]
jsonpath "$" isCollection

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: Performance
limit: 100

HTTP 200
[Asserts]
jsonpath "$" isCollection

GET http://127.0.0.1:8000/api/v1/vendors/search/
Accept: application/json
[QueryStringParams]
q: example.com
limit: 100

HTTP 200
[Asserts]
jsonpath "$" isCollection

# ==============================================================================
# Step 4: Final Verification
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/count
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.active_vendors_count" exists

[Captures]
final_count: jsonpath "$.active_vendors_count"

GET http://127.0.0.1:8000/api/v1/vendors/
Accept: application/json
[QueryStringParams]
active_only: false
limit: 100

HTTP 200
[Asserts]
jsonpath "$" isCollection

# ==============================================================================
# Step 5: Health Check After Cleanup
# ==============================================================================

GET http://127.0.0.1:8000/health
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.status" == "healthy"
jsonpath "$.service" == "Transport-Management-System"

# ==============================================================================
# Cleanup Complete
# All seeded vendor data has been removed from the database
# Database is now clean and ready for fresh data
# ==============================================================================
