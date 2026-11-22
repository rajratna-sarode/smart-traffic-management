# Aggregation pipelines

Run after `use smart_parking_db`. Output values vary with database contents; these are pipeline examples and illustrative output shapes, not claimed run results. For reporting windows, supply actual `ISODate` bounds to `$match`.

## 1. Booking status summary

```javascript
db.bookings.aggregate([{$group:{_id:"$status",count:{$sum:1}}},{$sort:{_id:1}}])
```
Sample shape: `[{_id:"cancelled",count:3},{_id:"completed",count:12}]`.

## 2. Slot utilization for a selected reporting period

Utilization is total confirmed/active overlap hours divided by all non-maintenance slot-hours in the period. Each booking's overlap is clipped to the reporting interval; cancelled bookings do not count. This example uses `$lookup`, `$match`, `$project`, `$group`, `$sum`, `$min`, and `$max`.

```javascript
const from=ISODate("2026-11-01T00:00:00Z"), to=ISODate("2026-11-08T00:00:00Z");
db.parking_slots.aggregate([
 {$match:{status:{$ne:"Maintenance"}}},
 {$lookup:{from:"bookings",let:{sid:"$_id"},pipeline:[{$match:{$expr:{$and:[{$eq:["$slot_id","$$sid"]},{$in:["$status",["confirmed","active"]]},{$lt:["$start_time",to]},{$gt:["$end_time",from]}]}}},{$project:{hours:{$divide:[{$subtract:[{$min:["$end_time",to]},{$max:["$start_time",from]}]},3600000]}}}],as:"period_bookings"}},
 {$project:{occupied_hours:{$sum:"$period_bookings.hours"},available_hours:{$literal:168}}},
 {$group:{_id:null,occupied_hours:{$sum:"$occupied_hours"},available_hours:{$sum:"$available_hours"}}},
 {$project:{_id:0,occupied_hours:1,available_hours:1,utilization_percent:{$multiply:[{$divide:["$occupied_hours","$available_hours"]},100]}}}
])
```
Sample shape: `[{occupied_hours:42,available_hours:3024,utilization_percent:1.3889}]`. For a partial period or variable slot hours, replace 168 with actual period hours; exclude slots under maintenance during the interval for precise historical reporting.

## 3. Completed parking revenue

```javascript
db.bookings.aggregate([{$match:{status:"completed"}},{$group:{_id:null,revenue:{$sum:"$total_amount"},bookings:{$sum:1}}},{$project:{_id:0,revenue:1,bookings:1}}])
```
Sample shape: `[{revenue:1230,bookings:12}]`.

## 4. Revenue by parking slot

```javascript
db.bookings.aggregate([{$match:{status:"completed"}},{$group:{_id:"$slot_number",revenue:{$sum:"$total_amount"},completed_bookings:{$sum:1}}},{$sort:{revenue:-1}},{$project:{slot_number:"$_id",_id:0,revenue:1,completed_bookings:1}}])
```
Sample shape: `[{slot_number:"C01",revenue:360,completed_bookings:3}]`.

## 5. Average, minimum and maximum duration

```javascript
db.bookings.aggregate([{$match:{status:"completed"}},{$group:{_id:null,average_hours:{$avg:"$duration_hours"},min_hours:{$min:"$duration_hours"},max_hours:{$max:"$duration_hours"},count:{$sum:1}}},{$project:{_id:0,average_hours:1,min_hours:1,max_hours:1,count:1}}])
```
Sample shape: `[{average_hours:2.5,min_hours:1,max_hours:4,count:12}]`.

`GET /api/dashboard/aggregations` executes status summary, completed revenue, revenue by slot and duration statistics on live data. The period utilization pipeline is documented above because it requires reporting-period bounds.
