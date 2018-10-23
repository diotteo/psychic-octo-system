# High level requirements

1. Simplicity. Integration needs to be dead simple.
2. Resilient to network failures or crashes.
3. Near real time replication of data across Geolocation. Writes need to be in real time.
4. Data consistency across regions
5. Locality of reference, data should almost always be available from the closest region
6. Flexible Schema
7. Cache can expire

# Comments on requirements

In general, we are lacking a lot of details to implement the right solution. Below are a non-exhaustive list organized by related requirement.

1. Simplicity
	It is difficult to design a drop-in solution without knowing what the solution will interface with. What are entries going to look like? Can they be really large files? Do we need to supply them directly or can it be provided through a URL (on nearby storage) to it? Is a specific programming language interface required? Do we need to handle various text encodings?
2. Resiliency to crashes and network failures
	How resilient and what do we need to be resilient about? If all nodes in a geographic location are down, is it better to answer from far away or to bypass the cache? Are we stateful? Can a client seemlessly switch to a different node midway through an exchange by just repeating its last message?
3. Near real time replicaton and real time writes
	How can writes be done in real time (suggesting no networking jitter) as part of a geo distributed system? How can we guarantee that the replication channel (between nodes) is faster than whatever channel a third-party could use to communicate to a reader halfway around the world that the writer on this end is finished? And then make sure the remote node doesn't answer its local (from its perspective) client before it is notified of the updated value? More to the point: if our network is so fast at propagating updates, why do we even need to geo distribute the cache in the first place?
4. Data consistency
	Same as above, how can we guarantee data consistency without knowing what network layer technology we're using (IP is best effort and packet-switched so it doesn't guarantee delivery or even delivery order)
5. Locality of reference
	No comment
6. Flexibility of schema
	What kind of flexibility are we looking for? Do we want to be able to store any type of [structured] document or is the flexibility meant for metadata we'd want to associate with some entries?
7. Cache expiry
	No comment

# Design

Elements are key-document pairs, where the key is a string and the document a JSON object (NoSQL approach)

Client anycasts READ or WRITE request (key-only included). First respondent is chosen.

Servers reply to READ requests if they hold the key, in which case they send its content
Servers reply to WRITE requests to signal availability and inform the client of their unicast address.
	Client then connects reliably (unicast, TCP) to the server and transfer the data.
Servers handle spreading the writes to other shards themselves (UPDATE requests).
Servers maintain a list of peers in the swarm with eventual drop off after timeout.

# Design limitations

* Client-side writes are fast but replication time is best effort and dependent on the state of the network. Neither has real time guarantees.
* Data is only eventually consistent across geolocation.
* There is no guarantee of locality of reference given that a write may have happened on one shard halfway across the world, on the other side of a network split. Plus, maybe the entry timed out before the split was resolved
* Without knowing what the lower layers guarantee us, it is not possible to guarantee real time, localized reference to consistent data. That doesn't sound possible for a system using the Internet Protocol (IP) at least.

# Implementation

The current implementation is a Proof-of-Concept that doesn't implement the design as specified. It does not deal with network issues, does not recover from crashes and it isn't distributed. It does fulfill the following properties however:

1. Simplicity: it is a very simple piece of code, so it is very easy to understand and integrate into anything
3. Replication is a noop so it is instantaneous. Writes are very fast.
4. Data is always consistent because there is only one source of truth
5. Data is always available from the closest region because there is only 1 region
6. Flexibility of schema: the proof of concept expects data to be encoded UTF-8 but does no parsing beyond that on the document values so we're very close to perfect flexibility
7. Cache expires on a timer. Entries cannot be manually expired however
