---
skill:
  id: skill-15-data-modeling
  name: Data Modeling
  category: architecture
  version: "2.0.0"

laws:
  implements:
    - id: BUS-3.1
      title: Data Classification Law
    - id: BUS-3.2
      title: Data Quality Law
    - id: BUS-3.4
      title: Data Retention Law
  references:
    - id: ENG-2.1
      title: Domain-Driven Design Law
    - id: BUS-3.3
      title: Data Lineage Law

triggers:
  phrases:
    - "Design the schema"
    - "Database modeling"
    - "Data migration"
    - "Entity relationships"

followed_by:
  - skill-04-business-domain-modeling
  - skill-06-atomic-tdd
---

# Skill: Data Modeling

> **Purpose:** Design database schemas that accurately represent the domain, perform efficiently, and evolve gracefully over time.

---

## Purpose

Data Modeling is the practice of translating business concepts into database structures. This skill ensures:

1. **Accuracy** - Schema reflects the true domain model
2. **Performance** - Queries execute efficiently at scale
3. **Integrity** - Data constraints prevent invalid states
4. **Evolvability** - Schema can change without breaking systems
5. **Clarity** - Structure is understandable and documented

**Key principle:** Data outlives code. Bad schema decisions haunt for years. Good ones enable everything.

---

## When to Invoke

Invoke this skill when:

- Designing new features requiring data storage
- Performance issues traced to database
- Adding relationships between entities
- Planning data migrations
- Reviewing schema changes
- Choosing between SQL and NoSQL

**Trigger phrases:**
- "What should the table structure look like?"
- "How do we model this relationship?"
- "This query is too slow"
- "We need to migrate the data"
- "Should this be normalized?"

---

## Constitutional Foundation

### Engineering Constitution
- **Article II, Section 2.1** - Simplicity: Schema should be as simple as possible
- **Article III, Section 3.1** - Quality: Data integrity enforced
- **Article IV, Section 4.1** - Test-First: Migrations tested before apply

### Business Constitution
- **Article II, Section 2.1** - Business Rules: Constraints reflect business rules
- **Article III, Section 3.1** - Data Governance: Data properly structured

---

## Relational Data Modeling

### Normalization

**Normal Forms:**

| Form | Rule | Purpose |
|------|------|---------|
| **1NF** | Atomic values, no repeating groups | Basic structure |
| **2NF** | 1NF + no partial dependencies | Remove redundancy |
| **3NF** | 2NF + no transitive dependencies | Clean design |
| **BCNF** | Every determinant is a key | Strict integrity |

**Example - Normalizing an Order:**

```sql
-- Unnormalized (BAD)
CREATE TABLE orders_denorm (
    order_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_address TEXT,
    product1_name VARCHAR(100),
    product1_price DECIMAL,
    product1_qty INT,
    product2_name VARCHAR(100),
    product2_price DECIMAL,
    product2_qty INT
    -- What about product 3? 4? 100?
);

-- Normalized (GOOD)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    street TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    type VARCHAR(20) DEFAULT 'shipping'
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    shipping_address_id INT REFERENCES addresses(id),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL
);
```

### When to Denormalize

**Acceptable denormalization:**

```sql
-- Denormalized for read performance
CREATE TABLE order_summaries (
    order_id INT PRIMARY KEY REFERENCES orders(id),
    customer_name VARCHAR(100),  -- Denormalized
    item_count INT,              -- Computed
    total_amount DECIMAL(10,2),  -- Computed
    last_updated TIMESTAMP
);

-- Updated via trigger or application code
-- Trade-off: Write complexity for read speed
```

**Denormalize when:**
- Read performance is critical
- Data is relatively static
- Update complexity is manageable
- Consistency can be maintained

---

### Relationships

**One-to-Many:**
```sql
-- A customer has many orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id),
    -- customer_id is the foreign key
);
```

**Many-to-Many:**
```sql
-- Products can be in many categories
-- Categories can have many products
CREATE TABLE product_categories (
    product_id INT REFERENCES products(id),
    category_id INT REFERENCES categories(id),
    PRIMARY KEY (product_id, category_id)
);
```

**One-to-One:**
```sql
-- User has one profile (optional)
CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY REFERENCES users(id),
    bio TEXT,
    avatar_url TEXT
);
```

---

### Constraints

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,

    -- NOT NULL - Required field
    name VARCHAR(100) NOT NULL,

    -- UNIQUE - No duplicates
    sku VARCHAR(50) UNIQUE NOT NULL,

    -- CHECK - Business rule
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),

    -- ENUM via CHECK
    status VARCHAR(20) NOT NULL
        CHECK (status IN ('draft', 'active', 'discontinued')),

    -- Compound UNIQUE
    UNIQUE (vendor_id, vendor_sku)
);

-- Partial unique index
CREATE UNIQUE INDEX active_user_email
    ON users(email)
    WHERE deleted_at IS NULL;
```

---

### Indexing

**Index Types:**

| Type | Use Case | Example |
|------|----------|---------|
| **B-tree** | Default, equality and range | `WHERE price > 100` |
| **Hash** | Equality only | `WHERE id = 123` |
| **GiST** | Geometric, full-text | `WHERE location @> point` |
| **GIN** | Arrays, JSONB | `WHERE tags @> ARRAY['sale']` |

**Indexing Strategy:**

```sql
-- Primary key (automatic index)
CREATE TABLE orders (
    id SERIAL PRIMARY KEY
);

-- Foreign keys (create explicitly)
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Query patterns
-- For: WHERE status = 'pending' AND created_at > '2024-01-01'
CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- Covering index (includes all needed columns)
-- For: SELECT id, status, total FROM orders WHERE customer_id = ?
CREATE INDEX idx_orders_customer_covering
    ON orders(customer_id)
    INCLUDE (status, total);

-- Partial index (filtered)
-- For: WHERE status = 'pending' (only 5% of orders)
CREATE INDEX idx_orders_pending
    ON orders(created_at)
    WHERE status = 'pending';
```

**Index Anti-Patterns:**

```sql
-- BAD: Index on low-cardinality column
CREATE INDEX idx_users_active ON users(is_active);  -- Only true/false

-- BAD: Too many indexes (slows writes)
CREATE INDEX idx1 ON orders(a);
CREATE INDEX idx2 ON orders(b);
CREATE INDEX idx3 ON orders(a, b);  -- Redundant with idx1

-- BAD: Wrong column order in composite index
-- Query: WHERE status = 'pending' AND customer_id = 123
CREATE INDEX idx ON orders(status, customer_id);  -- Less efficient
CREATE INDEX idx ON orders(customer_id, status);  -- More efficient
```

---

## Schema Migration

### Migration Best Practices

```python
# migrations/20240115_001_add_order_notes.py

def upgrade(db):
    """Add notes column to orders table."""
    db.execute("""
        ALTER TABLE orders
        ADD COLUMN notes TEXT;
    """)

def downgrade(db):
    """Remove notes column from orders table."""
    db.execute("""
        ALTER TABLE orders
        DROP COLUMN notes;
    """)
```

### Safe Migration Patterns

**Adding a column:**
```sql
-- Safe: Add nullable column
ALTER TABLE orders ADD COLUMN notes TEXT;

-- Later: Add default, make non-null
ALTER TABLE orders ALTER COLUMN notes SET DEFAULT '';
UPDATE orders SET notes = '' WHERE notes IS NULL;
ALTER TABLE orders ALTER COLUMN notes SET NOT NULL;
```

**Renaming a column:**
```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);

-- Step 2: Backfill data
UPDATE users SET full_name = name;

-- Step 3: Update application to write to both
-- Step 4: Update application to read from new
-- Step 5: Stop writing to old column
-- Step 6: Drop old column
ALTER TABLE users DROP COLUMN name;
```

**Adding an index:**
```sql
-- CONCURRENTLY: Doesn't lock table (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_orders_customer
    ON orders(customer_id);
```

### Dangerous Migrations

```sql
-- DANGEROUS: Locks table during backfill
ALTER TABLE orders ADD COLUMN total DECIMAL NOT NULL DEFAULT 0;

-- SAFE: Three-step process
ALTER TABLE orders ADD COLUMN total DECIMAL;
UPDATE orders SET total = calculate_total(id);  -- In batches
ALTER TABLE orders ALTER COLUMN total SET NOT NULL;

-- DANGEROUS: Dropping column with dependent code
ALTER TABLE users DROP COLUMN legacy_id;

-- SAFE: Deprecation period first
-- 1. Stop writing to column
-- 2. Deploy code that doesn't read column
-- 3. Drop column
```

---

## NoSQL Considerations

### When to Use NoSQL

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Complex relationships | SQL | JOINs are powerful |
| ACID transactions | SQL | Strong consistency |
| Flexible schema | Document DB | Schema-less |
| High write volume | Wide-column | Write-optimized |
| Caching | Key-value | Simple, fast |
| Graph relationships | Graph DB | Traversal queries |

### Document Database Modeling

```javascript
// MongoDB example - Embedding vs. Referencing

// Embedding (denormalized) - Good for:
// - Data accessed together
// - One-to-few relationships
{
  "_id": "order_123",
  "customer": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "items": [
    { "product": "Widget", "quantity": 2, "price": 19.99 },
    { "product": "Gadget", "quantity": 1, "price": 49.99 }
  ]
}

// Referencing (normalized) - Good for:
// - Large/growing subdocuments
// - Many-to-many relationships
// - Frequently updated data
{
  "_id": "order_123",
  "customer_id": "cust_456",  // Reference
  "item_ids": ["item_1", "item_2"]  // References
}
```

---

## Query Optimization

### EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT o.id, o.total, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending'
  AND o.created_at > '2024-01-01';

-- Output analysis:
-- Seq Scan = Bad (full table scan)
-- Index Scan = Good (using index)
-- Nested Loop = Check for missing indexes on join
-- Hash Join = Usually efficient for large tables
```

### Common Query Optimizations

```sql
-- BAD: N+1 query pattern
SELECT * FROM orders;  -- Returns 100 orders
-- Then for each order:
SELECT * FROM order_items WHERE order_id = ?;  -- 100 queries!

-- GOOD: JOIN or subquery
SELECT o.*, oi.*
FROM orders o
JOIN order_items oi ON oi.order_id = o.id;

-- BAD: SELECT *
SELECT * FROM orders;  -- Fetches all columns

-- GOOD: Select only needed columns
SELECT id, status, total FROM orders;

-- BAD: LIKE with leading wildcard
SELECT * FROM products WHERE name LIKE '%widget%';

-- GOOD: Full-text search
SELECT * FROM products
WHERE to_tsvector('english', name) @@ to_tsquery('widget');
```

---

## Good Examples

### Example 1: E-Commerce Schema

```sql
-- Well-designed e-commerce schema

-- Customers
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products with proper constraints
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'active', 'discontinued')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders with proper relationships
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id),
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status) WHERE status = 'pending';

-- Order items with referential integrity
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    UNIQUE (order_id, product_id)
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: No Constraints

```sql
-- BAD: No integrity constraints
CREATE TABLE orders (
    id INT,
    customer_id INT,  -- No FK
    total VARCHAR(50),  -- Wrong type
    status TEXT  -- No validation
);

-- Invalid data is possible:
INSERT INTO orders VALUES (1, 99999, 'lots of money', 'whatever');
```

**Correct approach:** Use appropriate types, constraints, and foreign keys.

---

### Anti-Pattern 2: Entity-Attribute-Value (EAV)

```sql
-- BAD: EAV pattern
CREATE TABLE product_attributes (
    product_id INT,
    attribute_name VARCHAR(100),
    attribute_value TEXT
);

-- Queries become nightmares:
SELECT
    p.id,
    MAX(CASE WHEN a.attribute_name = 'color' THEN a.attribute_value END) as color,
    MAX(CASE WHEN a.attribute_name = 'size' THEN a.attribute_value END) as size
FROM products p
JOIN product_attributes a ON a.product_id = p.id
GROUP BY p.id;
```

**Correct approach:** Use proper columns or JSONB for flexible attributes.

---

### Anti-Pattern 3: God Table

```sql
-- BAD: One table to rule them all
CREATE TABLE entities (
    id INT,
    type VARCHAR(50),  -- 'user', 'product', 'order', etc.
    name VARCHAR(200),
    email VARCHAR(200),  -- Only for users
    price DECIMAL,       -- Only for products
    status VARCHAR(50),
    data JSONB          -- Everything else
);
```

**Correct approach:** Separate tables for separate concepts.

---

## Quality Checklist

Before considering data model complete:

### Design
- [ ] Tables represent clear domain concepts
- [ ] Relationships properly defined with FKs
- [ ] Appropriate normalization level
- [ ] Constraints enforce business rules

### Performance
- [ ] Indexes support query patterns
- [ ] No obvious N+1 query patterns
- [ ] Large tables have partitioning strategy
- [ ] EXPLAIN ANALYZE run on key queries

### Evolution
- [ ] Migration scripts created and tested
- [ ] Rollback scripts prepared
- [ ] No destructive changes without deprecation

### Documentation
- [ ] Schema documented (ERD or similar)
- [ ] Column purposes explained
- [ ] Constraints rationale documented

---

## Skill Interactions

### Preceded By
- **04-Business Domain Modeling** - Domain model informs schema
- **05-Business Rules** - Rules become constraints

### Followed By
- **06-Atomic TDD** - Repository tests validate schema
- **12-API Design** - API reflects data model

### Related Skills
- **09-Refactoring** - Schema refactoring patterns
- **13-Observability** - Query performance monitoring
