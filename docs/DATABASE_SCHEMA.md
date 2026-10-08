# Database Schema

Default database: SQLite at `instance/smart_health.db`.

## user

| Column | Type | Notes |
| --- | --- | --- |
| id | Integer | Primary key |
| name | String(120) | Required |
| email | String(180) | Unique, indexed |
| password_hash | String(255) | Werkzeug password hash |
| role | String(30) | patient, doctor, admin |
| created_at | DateTime | UTC timestamp |

## prediction_history

| Column | Type | Notes |
| --- | --- | --- |
| id | Integer | Primary key |
| user_id | Integer | Foreign key to user |
| source | String(40) | symptoms, report, api |
| disease | String(100) | Predicted disease |
| confidence | Float | Probability/risk percentage |
| severity | String(40) | Low, Medium, High, Critical |
| doctor_type | String(120) | Recommended doctor |
| health_score | Integer | 0 to 100 score |
| inputs_json | JSON | Normalized model inputs or report values |
| result_json | JSON | Full recommendation output |
| created_at | DateTime | UTC timestamp |

## appointment

| Column | Type | Notes |
| --- | --- | --- |
| id | Integer | Primary key |
| user_id | Integer | Foreign key to user |
| doctor_type | String(120) | Requested specialist |
| preferred_date | Date | Requested date |
| preferred_time | String(20) | Requested time |
| reason | Text | Patient note |
| status | String(30) | Requested, Confirmed, Completed, Cancelled |
| created_at | DateTime | UTC timestamp |

## medication_reminder

| Column | Type | Notes |
| --- | --- | --- |
| id | Integer | Primary key |
| user_id | Integer | Foreign key to user |
| medicine_name | String(120) | Reminder label |
| dosage | String(80) | Optional dosage |
| reminder_time | String(20) | Local time string |
| note | String(255) | Optional note |
| is_active | Boolean | Active flag |
| created_at | DateTime | UTC timestamp |
