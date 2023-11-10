# Alumni_Database_Management

## Database Structure

The project is developed using MySQL version 8.0.34. Below is the list of tables in the database:

- `alumni`
- `alumni_audit`
- `batch`
- `degree`
- `donations`
- `playground_jobopening`
- `playground_user`
- `publications`
- `work`
  

Specifically, note the following:

- `playground_jobopening`: This table is related to the job opening feature of the project. It includes a built-in event that automatically removes job listings once the deadline is reached.

- `alumni_audit`: This is an optional log table, and triggers are implemented for its functioning.

- `playground_user`: This database stores the login credentials

## Project Overview

The project incorporates several features:

1. **User Role Management:**
   - The user role (alumni/student) is determined based on the SRN year field.
   - Students do not have edit or delete control.

2. **Password Management:**
   - Passwords are managed through the `playground_user` table.

3. **CRUD Operations:**
   - Pages are provided for basic CRUD operations.
   - SQL enthusiasts can enter their own queries, but update, delete, and create operations are restricted for non-alumni users.
   - The system allows downloading query results in CSV format.

4. **Job Opening Portal:**
   - A dedicated portal for job openings (`playground_jobopening` table).
   - Role controls apply, ensuring proper access restrictions.
   - usage of MySQL events to check for deadline

5. **Email Sending:**
   - There is a facility to send emails without specifying the email address. Only the first name and last name are required.
   - Email functionality is implemented using SMTP. Users replicating this project should have an email account and generate an application passkey/password.

6. **Batch-Specific Alumni Listing:**
   - Options are provided to view alumni of batches 2020 and 2021
   - usage of MySQL procedures.

7. **Write your own query!:**
   - Option to write your own sql queries and query from the database , the update ,delete , create regulation for non-alumni applies here too

## Instructions for Replication:

- Ensure you are using MySQL version 8.0.34.
- For email functionality, set up an email account and obtain an application passkey/password.
    reference :- https://knowledge.workspace.google.com/kb/how-to-generate-an-app-passwords-000009237
    Note : for gmail users only
- Configure the necessary settings in the project for email integration.
- The project includes built-in triggers for audit logging. Ensure that triggers are enabled in your MySQL environment.

:)
