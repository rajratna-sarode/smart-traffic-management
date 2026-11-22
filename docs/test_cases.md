# Test cases and results

These are execution procedures and expected outcomes, not represented as passed: MongoDB was not reachable during project creation, so no live test result is claimed. Start MongoDB, initialize and seed, then execute each case and record the actual result in the final column for the college report.

| # | Test | Procedure | Expected result | Actual result |
|---|---|---|---|---|
| 1 | Vehicle registration | POST valid vehicle to `/api/vehicles/` | 201 and one MongoDB document | Not run: MongoDB unavailable |
| 2 | Duplicate registration | POST same registration again | 409, one record remains | Not run: MongoDB unavailable |
| 3 | Vehicle search | GET `/api/vehicles/?q=KA05` | Matching registration rows | Not run: MongoDB unavailable |
| 4 | Vehicle update | PUT changed mobile to vehicle id | 200 and changed field | Not run: MongoDB unavailable |
| 5 | Vehicle delete | DELETE vehicle without live booking | 200 and record removed | Not run: MongoDB unavailable |
| 6 | Slot creation | POST valid Car slot | 201 and slot appears in GET | Not run: MongoDB unavailable |
| 7 | Booking creation | POST registered vehicle, matching slot, future valid interval | 201; duration and amount calculated | Not run: MongoDB unavailable |
| 8 | Booking update | PUT another valid time to confirmed booking | 200; times and charge updated | Not run: MongoDB unavailable |
| 9 | Booking cancellation | PATCH status `cancelled` | 200; no longer blocks availability | Not run: MongoDB unavailable |
| 10 | Overlap prevention | Create second confirmed booking overlapping same slot | 409; second document not created | Not run: MongoDB unavailable |
| 11 | Availability | GET availability across booked interval | conflicting slot excluded | Not run: MongoDB unavailable |
| 12 | Index and aggregation | Run init, inspect `getIndexes()`, call aggregation endpoint | Indexes present, live grouped output returned | Not run: MongoDB unavailable |

## UI walkthrough

With Flask and MongoDB running, open the dashboard, register a vehicle, add a matching slot, and create a reservation. Confirm the list updates without a page reload, check the success/error toast, then try overlapping time windows to see backend conflict rejection. Capture screenshots directly from the running app for the college submission; do not use mock screenshots.
