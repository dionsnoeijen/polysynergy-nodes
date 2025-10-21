import pytest
import sqlite3
import tempfile
import os

from polysynergy_nodes.sql.sqlite_connection_node import SQLiteConnectionNode
from polysynergy_nodes.sql.base_sql_connection import BaseSqlConnection


@pytest.fixture
def sample_database():
    """Create a temporary SQLite database with sample CRM data"""
    # Create temporary database file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db')
    db_path = temp_file.name
    temp_file.close()

    # Create database and populate with sample data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create customers table
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            company TEXT,
            status TEXT DEFAULT 'active',
            total_spent REAL DEFAULT 0.0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert sample data
    sample_customers = [
        ('John Doe', 'john@example.com', 'Acme Corp', 'active', 1250.00),
        ('Jane Smith', 'jane@example.com', 'Tech Solutions', 'active', 890.50),
        ('Bob Johnson', 'bob@example.com', 'Startup Inc', 'inactive', 450.00),
        ('Alice Williams', 'alice@example.com', 'Enterprise Ltd', 'active', 3200.00),
        ('Charlie Brown', 'charlie@example.com', 'Small Biz', 'active', 125.00),
    ]

    cursor.executemany(
        "INSERT INTO customers (name, email, company, status, total_spent) VALUES (?, ?, ?, ?, ?)",
        sample_customers
    )

    conn.commit()
    conn.close()

    yield db_path

    # Cleanup
    os.unlink(db_path)


@pytest.mark.asyncio
async def test_sqlite_connection_service(sample_database):
    """Test SQLite Connection service node"""
    node = SQLiteConnectionNode()
    node.database_file = sample_database

    connection = await node.provide_instance()

    # Check that we got a proper connection instance
    assert connection is not None
    assert isinstance(connection, BaseSqlConnection)
    assert connection.database_type == "sqlite"
    assert node.instance is not None


@pytest.mark.asyncio
async def test_sqlite_connection_execute_query(sample_database):
    """Test executing query through SQLite connection"""
    node = SQLiteConnectionNode()
    node.database_file = sample_database

    connection = await node.provide_instance()

    # Execute a SELECT query
    results = await connection.execute_query("SELECT * FROM customers WHERE status = 'active' ORDER BY total_spent DESC")

    # Check results
    assert len(results) == 4  # 4 active customers
    assert results[0]['name'] == 'Alice Williams'  # Highest spender
    assert results[0]['total_spent'] == 3200.00


@pytest.mark.asyncio
async def test_sqlite_connection_with_parameters(sample_database):
    """Test parameterized query through SQLite connection"""
    node = SQLiteConnectionNode()
    node.database_file = sample_database

    connection = await node.provide_instance()

    # Execute parameterized query
    results = await connection.execute_query(
        "SELECT * FROM customers WHERE email = :email",
        {"email": "john@example.com"}
    )

    # Check results
    assert len(results) == 1
    assert results[0]['name'] == 'John Doe'
    assert results[0]['email'] == 'john@example.com'


@pytest.mark.asyncio
async def test_sqlite_connection_aggregation(sample_database):
    """Test aggregation query through SQLite connection"""
    node = SQLiteConnectionNode()
    node.database_file = sample_database

    connection = await node.provide_instance()

    # Execute aggregation query
    results = await connection.execute_query("""
        SELECT
            status,
            COUNT(*) as customer_count,
            SUM(total_spent) as total_revenue,
            AVG(total_spent) as avg_spent
        FROM customers
        GROUP BY status
        ORDER BY total_revenue DESC
    """)

    # Check results
    assert len(results) == 2  # 2 statuses (active, inactive)

    # Check active customers aggregation
    active_row = next(r for r in results if r['status'] == 'active')
    assert active_row['customer_count'] == 4
    assert active_row['total_revenue'] == 5465.50  # Sum of 4 active customers


@pytest.mark.asyncio
async def test_sqlite_connection_empty_results(sample_database):
    """Test query with no matching results"""
    node = SQLiteConnectionNode()
    node.database_file = sample_database

    connection = await node.provide_instance()

    # Query with no matches
    results = await connection.execute_query("SELECT * FROM customers WHERE email = 'nonexistent@example.com'")

    # Should return empty list
    assert results == []


@pytest.mark.asyncio
async def test_sqlite_connection_invalid_query(sample_database):
    """Test invalid SQL query"""
    node = SQLiteConnectionNode()
    node.database_file = sample_database

    connection = await node.provide_instance()

    # Query with syntax error
    with pytest.raises(Exception):
        await connection.execute_query("SELECT * FORM customers")  # FORM instead of FROM


@pytest.mark.asyncio
async def test_sqlite_connection_missing_file():
    """Test SQLite connection with missing database file"""
    node = SQLiteConnectionNode()
    node.database_file = ""

    # Should raise ValueError
    with pytest.raises(ValueError, match="database_file is required"):
        await node.provide_instance()
