# Seed Data for Transport Management System
# Creates sample vendor data for testing and development

# ==============================================================================
# Seed Vendor 1: Swift Transport Solutions
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Swift Transport Solutions",
    "contact_person": "John Smith",
    "email": "john.smith@swifttransport.com",
    "phone_number": "+1-555-0101",
    "is_active": true
}

HTTP *
[Asserts]
duration < 5000

# ==============================================================================
# Seed Vendor 2: Global Logistics Corp
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Global Logistics Corp",
    "contact_person": "Sarah Johnson",
    "email": "sarah.j@globallogistics.com",
    "phone_number": "+1-555-0102",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 3: Metro Freight Services
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Metro Freight Services",
    "contact_person": "Michael Davis",
    "email": "m.davis@metrofreight.com",
    "phone_number": "+1-555-0103",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 4: Express Cargo Ltd
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Express Cargo Ltd",
    "contact_person": "Emily Wilson",
    "email": "emily.wilson@expresscargo.com",
    "phone_number": "+1-555-0104",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 5: Prime Shipping Co
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Prime Shipping Co",
    "contact_person": "Robert Brown",
    "email": "r.brown@primeshipping.com",
    "phone_number": "+1-555-0105",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 6: Reliable Transport Inc
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Reliable Transport Inc",
    "contact_person": "Lisa Anderson",
    "email": "l.anderson@reliabletransport.com",
    "phone_number": "+1-555-0106",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 7: Fast Track Logistics
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Fast Track Logistics",
    "contact_person": "David Martinez",
    "email": "d.martinez@fasttrack.com",
    "phone_number": "+1-555-0107",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 8: Blue Ocean Shipping (Inactive)
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Blue Ocean Shipping",
    "contact_person": "Jennifer Taylor",
    "email": "j.taylor@blueocean.com",
    "phone_number": "+1-555-0108",
    "is_active": false
}

HTTP *

# ==============================================================================
# Seed Vendor 9: Mountain View Transport
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Mountain View Transport",
    "contact_person": "Christopher Lee",
    "email": "c.lee@mountainview.com",
    "phone_number": "+1-555-0109",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 10: City Express Delivery
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "City Express Delivery",
    "contact_person": "Amanda Clark",
    "email": "a.clark@cityexpress.com",
    "phone_number": "+1-555-0110",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 11: Interstate Cargo Solutions
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Interstate Cargo Solutions",
    "contact_person": "Kevin Rodriguez",
    "email": "k.rodriguez@interstate.com",
    "phone_number": "+1-555-0111",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 12: Atlantic Freight Lines
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Atlantic Freight Lines",
    "contact_person": "Michelle Garcia",
    "email": "m.garcia@atlanticfreight.com",
    "phone_number": "+1-555-0112",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 13: West Coast Logistics
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "West Coast Logistics",
    "contact_person": "Thomas Anderson",
    "email": "t.anderson@westcoast.com",
    "phone_number": "+1-555-0113",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 14: Northern Transport Co (Minimal Data)
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Northern Transport Co",
    "email": "info@northerntransport.com"
}

HTTP *

# ==============================================================================
# Seed Vendor 15: Southern Shipping Services (Inactive)
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Southern Shipping Services",
    "contact_person": "Mark Thompson",
    "email": "m.thompson@southernship.com",
    "phone_number": "+1-555-0115",
    "is_active": false
}

HTTP *

# ==============================================================================
# Seed Vendor 16: Coastal Maritime Transport
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Coastal Maritime Transport",
    "contact_person": "Patricia Wilson",
    "email": "p.wilson@coastalmaritime.com",
    "phone_number": "+1-555-0116",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 17: Desert Eagle Freight
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Desert Eagle Freight",
    "contact_person": "Carlos Mendez",
    "email": "carlos.mendez@deserteagle.com",
    "phone_number": "+1-555-0117",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 18: Lakeside Logistics Hub
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Lakeside Logistics Hub",
    "contact_person": "Rachel Green",
    "email": "rachel.green@lakesidelogistics.com",
    "phone_number": "+1-555-0118",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 19: Valley Transport Network
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Valley Transport Network",
    "contact_person": "Steven Park",
    "email": "s.park@valleytransport.com",
    "phone_number": "+1-555-0119",
    "is_active": true
}

HTTP *

# ==============================================================================
# Seed Vendor 20: Skyline Cargo Services (No phone)
# ==============================================================================

POST http://127.0.0.1:8000/api/v1/vendors/
Content-Type: application/json
Accept: application/json

{
    "company_name": "Skyline Cargo Services",
    "contact_person": "Diana Foster",
    "email": "diana.foster@skylinecargo.com",
    "is_active": true
}

HTTP *

# ==============================================================================
# Verify Seeding - Get Final Vendor Count
# ==============================================================================

GET http://127.0.0.1:8000/api/v1/vendors/count
Accept: application/json

HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.active_vendors_count" exists
jsonpath "$.active_vendors_count" >= 15

# ==============================================================================
# Seed Data Summary
# Successfully seeded 20 sample vendors with diverse data patterns:
# - Active and inactive vendors
# - Vendors with complete and minimal data
# - Various contact information patterns
# - Realistic company names and contact details
# ==============================================================================
