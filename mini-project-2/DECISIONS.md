# DECISIONS.md

### 1. What is an ODM and why do we use Beanie instead of writing raw MongoDB queries?

An **ODM (Object Document Mapper)** acts as an abstraction that saves us from writing complex manual queries; instead, we can interact with the database using standard Python models. We use **Beanie** because it makes development easier by allowing seamless data validation through **Pydantic** models.

---

### 2. What is the role of the Database class — why wrap Beanie methods inside it instead of calling them directly in routes?

The **Database class** manages all database operations in one centralized place. By wrapping Beanie methods inside this class instead of calling them directly in the routes, we keep the code modular. If we want to make changes to the database or switch the whole database entirely, we only need to change this one file.

---

### 3. What happens if `initialize_database()` is not called on startup? What would break and why?

The application will start, but **Beanie** will not know which database to connect to or how to map the models. Consequently, the app will eventually crash the moment you try to use any routes that require database interaction.

---

### 4. What is the difference between the `Event` document and the `EventUpdate` model, and why are they two separate classes?

The **`Event` document** inherits from Beanie’s `Document` class and typically requires all fields to be present for the database. The **`EventUpdate` model** is a Pydantic `BaseModel` where fields are typically **Optional**. They are separate classes so that users can update specific fields without being forced to provide the entire document every time.
