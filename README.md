# Hospital Management System (REST API)

A comprehensive Hospital Management System built with Django REST Framework (DRF) and SimpleJWT. This system provides complete CRUD operations for departments, doctors, patients, appointments, prescriptions, medicines, and billing with role-based access control (RBAC).

## Features

- **User Roles & Authentication**: 
  - JWT-based authentication (`/api/v1/auth/login/` and `/api/v1/auth/refresh/`).
  - Roles supported: `Admin`, `Doctor`, `Patient`, and `Receptionist`.
- **Department Management**: Complete CRUD operations for hospital departments.
- **Doctor Management**: Manage doctor profiles, specializations, experiences, availability status, and assign them to departments.
- **Patient Management**: Profile details including age, gender, blood group, phone, and address. Patients may create and update their own profile; Admin/Receptionist manage all patient records.
- **CORS**: Allows the React frontend (`http://localhost:5173` / `http://127.0.0.1:5173`) to call this API.
- **Appointment System**: Schedule and manage patient appointments with doctors.
  - Automatic assignment of patient profile for patient-logged users.
  - Custom status transitions (`pending`, `approved`, `completed`, `cancelled`).
- **Prescription System**: Doctors can generate prescriptions with diagnoses, notes, and specific medicines (dosages and durations) once an appointment is marked as `completed`.
- **Medicine Inventory**: Inventory of medicines to be used in prescriptions.
- **Billing System**: Generate, track, and manage bills for patients.
- **Advanced Filtering, Searching & Ordering**: Custom filtering and searching across departments, doctors, appointments, medicines, and bills.
- **Pagination**: Standardized `PageNumberPagination` with page size of `10`.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hospital-management-api
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

---

## Authentication & Authorization

Protected endpoints require the `Authorization` header with the Bearer JWT token:
```http
Authorization: Bearer <access_token>
```

### JWT Endpoints

| Method | Endpoint | Description | Request Body |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/v1/auth/login/` | Obtain access and refresh tokens | `{"username": "...", "password": "..."}` |
| **POST** | `/api/v1/auth/refresh/` | Refresh expired access token | `{"refresh": "..."}` |

---

## API Endpoints (Version 1)

All primary resources are exposed under the `/api/v1/` prefix.

| Resource | Endpoint | Supported Methods | Allowed Roles |
| :--- | :--- | :--- | :--- |
| **User Registration** | `/api/v1/users/` | `POST` (Register), `GET`, `PUT`, `DELETE` | `POST`: Anyone<br>Other methods: Authenticated |
| **Departments** | `/api/v1/departments/` | `GET`, `POST`, `PUT`, `DELETE` | `GET`: Authenticated<br>Write (`POST`/`PUT`/`DELETE`): Admin |
| **Doctors** | `/api/v1/doctors/` | `GET`, `POST`, `PUT`, `DELETE` | `GET`: Authenticated<br>Write: Admin, Receptionist |
| **Patients** | `/api/v1/patients/` | `GET`, `POST`, `PUT`, `DELETE` | `GET`: Authenticated<br>Write: Admin, Receptionist<br>Patients: create/update own profile only |
| **Appointments** | `/api/v1/appointments/` | `GET`, `POST`, `PUT`, `DELETE` | **Role-Filtered** (Patients see their own; Doctors see theirs; Admins/Receptionists see all) |
| **Medicines** | `/api/v1/medicines/` | `GET`, `POST`, `PUT`, `DELETE` | `GET`: Authenticated<br>Write: Admin, Receptionist |
| **Prescriptions** | `/api/v1/prescriptions/` | `GET`, `POST`, `PUT`, `DELETE` | **Role-Filtered** (Patients see their own; Doctors see theirs; Admins/Receptionists see all) |
| **Bills** | `/api/v1/bills/` | `GET`, `POST`, `PUT`, `DELETE` | **Role-Filtered** (Patients see their own; Admins/Receptionists see all) |

### Custom Sub-Actions & Custom Methods

- **Doctors**:
  - `GET /api/v1/doctors/available/`: List all doctors currently marked as available.
- **Appointments**:
  - `PATCH /api/v1/appointments/{id}/approve/`: Approve a pending appointment.
  - `PATCH /api/v1/appointments/{id}/complete/`: Complete an approved appointment.
  - `PATCH /api/v1/appointments/{id}/cancel/`: Cancel an appointment.
- **Bills**:
  - `PATCH /api/v1/bills/{id}/mark_as_paid/`: Mark a patient's bill as paid.

---

## Validation & Business Logic Rules

The API enforces several critical validation and business rules at the serializer layer:

1. **Appointments**:
   - `appointment_date` cannot be in the past.
   - Selected doctor must be available (`is_available` must be `True`).
   - If a Patient registers an appointment, it is automatically assigned to their patient profile.
2. **Prescriptions**:
   - A prescription can only be created for an appointment with a `completed` status.
   - Only one prescription can be generated per appointment.
   - Prescriptions must include at least one medicine.
3. **Billing**:
   - Bill `amount` must be greater than zero.

---

## Filtering, Searching & Ordering

Advanced query parameter options are enabled on the following endpoints:

- **Doctors**:
  - Filter fields: `department`, `is_available`
  - Search fields: `user__first_name`, `user__last_name`, `specialization`, `phone`
- **Patients**:
  - Search fields: `user__first_name`, `user__last_name`, `phone`, `blood_group`
- **Appointments**:
  - Filter fields: `doctor`, `patient`, `appointment_date`, `status`
- **Medicines**:
  - Search fields: `name`, `unit`
- **Bills**:
  - Filter fields: `patient`, `paid`

---

## Technologies Used

- **Django 6.0.6** - Web framework
- **Django REST Framework** - API architecture & Serializers
- **djangorestframework-simplejwt** - Secure JWT authentication
- **django-filter** - Advanced query filtering capabilities
- **SQLite** - Default relational database
