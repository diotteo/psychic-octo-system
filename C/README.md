# Design

Elements are key-document pairs, where the key is a string and the document a JSON object (NoSQL approach)

Client anycasts READ or WRITE request (key-only included). First respondent is chosen.

Servers reply to READ requests if they hold the key, in which case they send its content
Servers reply to WRITE requests to signal availability and inform the client of their unicast address.
	Client then connects reliably (unicast, TCP) to the server and transfer the data.
Servers handle spreading the writes to other shards themselves (UPDATE requests).
Servers maintain a list of peers in the swarm with eventual drop off after timeout.

# Design limitations

* Client-side writes are fast but replication time is best effort and dependent on the state of the network.
* Data is only eventually consistent across geolocation.
* There is no guarantee of locality of reference given that a write may have happened on one shard halfway across the world, on the other side of a network split. Plus, maybe the entry timed out before the split was resolved
* Because of data hazards (WAW, WAR, RAW) as well as the potential for network failures, it is not possible to guarantee data consistency while also guaranteeing write times.

# Implementation

The current implementation is a Proof-of-Concept that doesn't implement the design as specified. It does not deal with network issues or sharding. These aspects of the solution are expected to be dealt with by leveraging a third-party product such as MongoDB as well as a good deal of network architecture engineering and computer system administration. These are considered outside the scope of a software library.
