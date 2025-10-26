# Database Systems

Database systems organize and manage data efficiently for storage and retrieval.

## Types of Databases

### Relational Databases (SQL)

Store data in **tables with relationships**.

#### Popular RDBMS

- **MySQL**: Open-source, widely used
- **PostgreSQL**: Advanced features, ACID compliance
- **Oracle**: Enterprise-grade
- **SQL Server**: Microsoft's database
- **SQLite**: Lightweight, embedded

#### SQL Basics

```sql
-- Create table
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data
INSERT INTO users (id, username, email)
VALUES (1, 'john_doe', 'john@example.com');

-- Query data
SELECT * FROM users WHERE username = 'john_doe';

-- Join tables
SELECT orders.*, users.username
FROM orders
JOIN users ON orders.user_id = users.id;
```

#### Key Concepts

- **Primary Key**: Unique identifier
- **Foreign Key**: References another table
- **Indexes**: Speed up queries
- **Normalization**: Reduce redundancy
- **Transactions**: ACID properties

### NoSQL Databases

Non-relational databases for **flexible data models**.

#### Document Databases

Store data as JSON-like documents:

- **MongoDB**: Most popular
- CouchDB
- Firebase Firestore

```javascript
// MongoDB example
db.users.insertOne({
    username: "john_doe",
    email: "john@example.com",
    profile: {
        age: 30,
        city: "New York"
    },
    tags: ["developer", "music"]
});
```

#### Key-Value Stores

Simple key-value pairs:

- **Redis**: In-memory, fast
- Memcached: Caching
- DynamoDB: AWS managed

#### Column-Family Stores

Organize data in columns:

- **Cassandra**: Distributed, scalable
- HBase: Hadoop ecosystem
- ScyllaDB: High performance

#### Graph Databases

Store relationships as **first-class citizens**:

- **Neo4j**: Property graph
- ArangoDB: Multi-model
- Amazon Neptune

**Use Cases:**
- Social networks
- Recommendation engines
- Fraud detection

## Database Design

### Normalization

Organize data to reduce redundancy:

- **1NF**: Atomic values
- **2NF**: No partial dependencies
- **3NF**: No transitive dependencies
- **BCNF**: Boyce-Codd Normal Form

### Denormalization

Deliberately add redundancy for **performance**.

## Indexing

Speed up data retrieval:

### Types of Indexes

- **B-Tree**: Balanced tree, default
- **Hash Index**: Equality comparisons
- **Full-Text Index**: Text search
- **Spatial Index**: Geographic data

### Trade-offs

- Faster reads
- Slower writes
- More storage

## Query Optimization

### Execution Plans

Analyze how database executes queries:

```sql
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';
```

### Optimization Techniques

- Use appropriate indexes
- Avoid SELECT *
- **Limit result sets**
- Use JOINs efficiently
- Partition large tables

## Transactions

### ACID Properties

- **Atomicity**: All or nothing
- **Consistency**: Valid state
- **Isolation**: Concurrent execution
- **Durability**: Permanent changes

### Isolation Levels

- Read Uncommitted
- Read Committed
- Repeatable Read
- **Serializable**

## Scalability

### Vertical Scaling

Add more resources to a single server:

- More CPU
- More RAM
- Faster storage

**Limitations:** Hardware limits

### Horizontal Scaling

Add more servers:

#### Replication

Copy data across servers:

- **Master-Slave**: One writer, multiple readers
- **Master-Master**: Multiple writers

#### Sharding

Partition data across servers:

- Range-based
- Hash-based
- **Geographic**

## Caching

Store frequently accessed data in memory:

- **Redis**: Advanced caching
- Memcached: Simple caching
- Application-level caching

### Cache Strategies

- **Cache-Aside**: Load on miss
- **Write-Through**: Write to cache and DB
- **Write-Behind**: Async write to DB

## Backup and Recovery

### Backup Types

- **Full Backup**: Complete copy
- **Incremental**: Changes since last backup
- **Differential**: Changes since last full backup

### Recovery Strategies

- Point-in-Time Recovery
- **Disaster Recovery Plan**
- Regular backup testing

## Security

- **Authentication**: Verify identity
- **Authorization**: Control access
- **Encryption**: Protect data at rest and in transit
- SQL Injection prevention
- Regular security audits
