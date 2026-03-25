# Decisions

## Pydantic Field Types

- `int` for IDs: Ensures numeric, non-null primary keys.
- `str` for names/courses: Handles text safely.
- `Semester` enum: Restricts to valid terms.
- `List[Enrolement]`: Nested for relationships.

## Validation Rules

- `gt=0` on IDs: Prevents invalid/negative keys.
- `min_length=2, max_length=50` on strings: Blocks empty or huge inputs.

## Async Usage

GET /students/ uses `await asyncio.sleep(1)` to mimic real DB query delay.

## Database

### 1. What is @contextmanager and why do we use it instead of a plain function here?

The `@contextmanager` decorator allows us to define a function (like `managed_db`) that can be used with the Python `with` statement. We use it here to ensure that the database connection is reliably opened and, most importantly, closed automatically even if an error occurs during execution. In a plain function, we would have to manually call `.close()` in every single route, which is error-prone and leads to resource leaks.

### 2. What does check_same_thread=False do and why is it necessary in a FastAPI application?

By default, SQLite restricts connection access to the single thread that created it. However, FastAPI is an asynchronous framework where different parts of a request might be handled by different threads in a thread pool. Setting `check_same_thread=False` tells SQLite to allow the connection to be shared across these threads, preventing "SQLite objects created in a thread can only be used in that same thread" errors.

### 3. What happens to your data when the server restarts — with the old list vs. with SQLite?

With the old in-memory Python list, all data is stored in the RAM allocated to the running script; once the server stops or restarts, that memory is wiped, and all data is lost. With SQLite, the data is written to a physical file on the disk (`sqlite.db`). This ensures "persistence," meaning the data survives server restarts, crashes, or power failures, as it is read back from the file when the application starts up again.
