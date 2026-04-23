/**
 * Scalix SDK — Example 04: Database Integration (TypeScript)
 *
 * Create an agent that can query a database.
 *
 * Local mode: uses SQLite on your machine.
 * Cloud mode: uses ScalixDB (managed Postgres).
 *
 * Prerequisites:
 *   npm install scalix better-sqlite3
 *   export SCALIX_API_KEY=your-key
 */

import { Agent, Tool, Database } from 'scalix';

// Create a local database and seed it
const db = new Database();

await db.execute(`
  CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
  )
`);

await db.execute(`
  INSERT OR IGNORE INTO products (id, name, category, price, stock) VALUES
  (1, 'Laptop Pro', 'Electronics', 1299.99, 45),
  (2, 'Wireless Mouse', 'Electronics', 29.99, 200),
  (3, 'Standing Desk', 'Furniture', 549.00, 30),
  (4, 'Monitor 4K', 'Electronics', 449.99, 80),
  (5, 'Ergonomic Chair', 'Furniture', 899.00, 15)
`);

const agent = new Agent({
  model: 'scalix-advanced',
  instructions:
    'You are a business analyst. Use SQL queries to answer questions about the data.',
  tools: [Tool.sql()],
});

const result = await agent.run(
  'What is the total value of electronics inventory (price × stock)?',
);
console.log(result.output);
