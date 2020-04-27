## Stonks

A PoC implementation of the Command Query Responsibility Segregation (CQRS) framework, applied to stocks and trading.

This uses Serverless AWS DynamoDB with Lambda, with pynamo and python3. The goal is to rewrite this in Scala, so I can learn scala.

## Explanations and stuff

The best explanation is by example, so I'll be taking you through what happens end-to-end when a user creates a `Trade`.

First off, the architecture.

Lambda -> Dynamo
Event, Consumer tables and model
Dynamo Event Stream
Etc

Creating a Trade

- `Trade` create command is triggered
- `Trade` event is validated and saved
  - User only gets notification that event was accepted
  - `Holding` and `Cash` models will need to update
- Dynamo event stream on events table is triggered
  - If event is `INSERT` then it's a new event
- Trigger relevant consumers - `Holding` and `Cash`
  - Holding
    - Changes yadda yadda
  - Cash
    - Changes yadda yadda
  - If consumer fails to update the Consumer table, it's ok as long as the event saved
- `Holding` and `Cash` are updated in table
- User queries `Cash`
- Cash returned by query on consumer
- Oh no Cash is wrong!
  - Reason: one consumer didn't succesfully update db
  - Solution: reconciling
    - We can get the correct values by processing the events
    - All consumers have `reconciledTo` field, `eventId` of last event on a successful reconciliation
    - On consume, `version` field is updated to `eventId`, `reconciledTo` only on reconcile
    - 'Soft' reconcile to reconcile from `reconciledTo`
    - 'Hard' reconcile to do entire event log (or from a hard reset point)
    - `consumer` table is effectively transient, as long as you have the events you can rebuild
  - Soft reconcile when `version` and `reconciledTo` drift too far, or user requests a reconcile
  - Hard or soft reconcile on cron job depending on needs

