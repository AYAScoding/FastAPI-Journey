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
