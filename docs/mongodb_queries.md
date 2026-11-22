# MongoDB CRUD and indexing reference

Run the examples in `mongosh` after `use smart_parking_db`. The Flask application performs the equivalent operations through PyMongo against the configured MongoDB database.

## Sample documents

```javascript
// vehicles
{ _id: ObjectId("..."), owner_name: "Asha Rao", registration_number: "KA05MN1001", vehicle_type: "Car", mobile: "9000000001", created_at: ISODate("..."), updated_at: ISODate("...") }
// parking_slots
{ _id: ObjectId("..."), slot_number: "C01", slot_type: "Car", floor: 0, hourly_rate: 60, status: "Available", created_at: ISODate("...") }
// bookings
{ _id: ObjectId("..."), vehicle_id: ObjectId("..."), vehicle_number: "KA05MN1001", slot_id: ObjectId("..."), slot_number: "C01", start_time: ISODate("..."), end_time: ISODate("..."), duration_hours: 2, hourly_rate: 60, total_amount: 120, status: "completed", created_at: ISODate("..."), updated_at: ISODate("...") }
// users (reserved for optional authenticated users; no login is currently implemented)
{ _id: ObjectId("..."), name: "Parking Admin", email: "admin@example.test", created_at: ISODate("...") }
```

## CRUD demonstrations

```javascript
// CREATE: insertOne and insertMany
db.vehicles.insertOne({owner_name:"Asha Rao",registration_number:"KA05MN1001",vehicle_type:"Car",mobile:"9000000001",created_at:new Date(),updated_at:new Date()})
db.parking_slots.insertMany([{slot_number:"C01",slot_type:"Car",floor:0,hourly_rate:60,status:"Available",created_at:new Date()},{slot_number:"B01",slot_type:"Bike",floor:0,hourly_rate:25,status:"Available",created_at:new Date()}])
// READ: find, findOne, filtering, projection, sorting
db.vehicles.find({vehicle_type:"Car"},{owner_name:1,registration_number:1,_id:0}).sort({created_at:-1})
db.vehicles.findOne({registration_number:"KA05MN1001"})
db.parking_slots.find({slot_type:"Car",status:"Available"}).sort({floor:1,slot_number:1})
// UPDATE: updateOne/updateMany, $set, $inc
db.vehicles.updateOne({registration_number:"KA05MN1001"},{$set:{mobile:"9111111111",updated_at:new Date()}})
db.parking_slots.updateMany({floor:0,status:"Available"},{$inc:{hourly_rate:5}})
db.parking_slots.updateOne({slot_number:"C01"},{$set:{status:"Maintenance"}})
// DELETE: deleteOne/deleteMany (only after checking booking references)
db.vehicles.deleteOne({registration_number:"KA05MN1001"})
db.bookings.deleteMany({status:"cancelled",created_at:{$lt:new Date("2020-01-01")}})
```

## Indexes and query plans

```javascript
db.vehicles.createIndex({registration_number:1},{unique:true,name:"uq_vehicle_registration"})
db.vehicles.createIndex({mobile:1},{name:"ix_vehicle_mobile"})
db.bookings.createIndex({vehicle_number:1,start_time:-1},{name:"ix_booking_vehicle_time"})
db.bookings.createIndex({slot_id:1,status:1,start_time:1,end_time:1},{name:"ix_booking_conflict"})
db.vehicles.getIndexes()
db.bookings.find({vehicle_number:"KA05MN1001"}).sort({start_time:-1}).explain("executionStats")
```

The unique registration index also supports registration searches and prevents duplicate plate numbers. The single-field mobile index supports owner contact lookup; compound booking indexes support vehicle history and overlap checks. Initialization creates these indexes idempotently.
