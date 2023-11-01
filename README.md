# Markdown syntax guide

# QRCode Processor

## Description

This demo Python application provides a main functionality centered around QR code scanning and data management. Users can upload QR codes, which in turn are used to update specific records in the database. 

**Authenticated Users**: Can view data and upload QR codes.\
**Admin Users**: Have the added capability to delete records.\
**Public Users**: Can view data.

All functionalities are exposed through API endpoints, allowing for easy usage.

## Prerequisites
**Python**: This application requires Python 3. Ensure it's installed by running python3 --version.\
**PostgreSQL**: This app uses PostgreSQL as its primary database. If you don't have it installed, you can use Homebrew (for macOS users) to install it. Check its installation with psql --version.\
**Virtual Environment**: It's recommended to use a virtual env to keep the application's dependencies isolated.

### Setup Instructions
1. Clone the repo
```
git clone https://github.com/Battsetseg20/qrcode_processor.git qrcode_processor
```
2. Navigate to Project Directory
```
cd qrcode_processor
```
3. Set up the virtual environnement
```
python3 -m venv venv
source venv/bin/activate
```
4. Install Required Packages
```
pip install -r requirements.txt
```

5. Install and Start PostgreSQL (For macOS users):
```
brew install postgresql
brew services start postgresql@14
```

6. Create the databases
```
createdb qrcode_processor_db
createdb qrcode_processor_db_test
```

7. Database seed
```
python seed_db.py
```
Seed will populate the database and generate the **test qrcode files** that are needed to test the endpoint. Please do not skip this step.

### Running the app
In your project directory 
```
cp .env.sample .env
```
Once the .env file created you can start the app by running
```
uvicorn main:app --reload
```

## API Documentation:

### Public Endpoints:

1. **Root Endpoint**:
    - **Method**: `GET`
    - **URL**: `/`
    - **Sample Response**:
      ```json
      {"message": "Hello, world!"}
      ```

2. **Generate Token**:
    - **Method**: `POST`
    - **URL**: `/token`
    - **Request Data**: Username and Password (through form data)
    - **Sample Response**:
      ```json
      {
        "access_token": "<YOUR_ACCESS_TOKEN>",
        "token_type": "bearer"
      }
      ```

3. **List Users**:
    - **Method**: `GET`
    - **URL**: `/users/`
    - **Parameters**: 
      - `skip`: Number of records to skip (default = 0)
      - `limit`: Number of records to fetch (default = 10)
    - **Sample Response**:
      ```json
      [
        {
          "id": "<UUID>",
          "name": "<USERNAME>"
        }
      ]
      ```

4. **List Departments**:
    - **Method**: `GET`
    - **URL**: `/departments/`
    - **Parameters**: `skip` and `limit`
    - **Sample Response**:
      ```json
      [
        {
          "id": "<UUID>",
          "name": "<DEPARTMENT_NAME>"
        }
      ]
      ```

5. **List Department Roles**:
    - **Method**: `GET`
    - **URL**: `/department_roles/`
    - **Parameters**: `skip` and `limit`
    - **Sample Response**:
      ```json
        [
        {
          "id": "<UUID>",
          "role": "<ROLE_NAME>",
          "department_id": "<DEPARTMENT_ID>",
          "user_id": "<USER_ID>"
        }
      ]
      ```

6. **Read User by ID**:
    - **Method**: `GET`
    - **URL**: `/user/{user_id}`
    - **Sample Response**:
      ```json
      {
        "id": "<UUID>",
        "name": "<USERNAME>"
      }
      ```

7. **Read Department by ID**:
    - **Method**: `GET`
    - **URL**: `/department/{department_id}`
    - **Sample Response**:
      ```json
      {
        "id": "<UUID>",
        "name": "<DEPARTMENT_NAME>"
      }
      ```

### Authenticated Endpoints:

1. **Upload QR Code**:
    - **Method**: `POST`
    - **URL**: `/upload_qr/`
    - **Headers**: Authorization (Bearer token)
    - **Request Data**: A file with the QR code
    - **Sample Response**:
      ```json
      {
        "detail": "QR code processed",
        "data": "<QR_CODE_DATA>"
      }
      ```

2. **Delete Department**:
    - **Method**: `DELETE`
    - **URL**: `/department/{department_id}`
    - **Headers**: Authorization (Bearer token)
    - **Sample Response**:
      ```json
      {
        "message": "Department deleted successfully"
      }
      ```

---

## API usage:

To interact with the API, you can use tools like curl, Python's requests library, or simply use Swagger UI provided by FastAPI by default. Remember, for the `upload_qr` and `delete_department` endpoints, you'll need to use the token for authentication.

### Example using curl:


#### Step 1: Get Users

Let's start by fetching the list of users.

```bash
curl -X GET 'http://127.0.0.1:8000/users/?skip=0&limit=10'
```

Once you execute this, you should get a list of users. Let's say one of the usernames you get is `john_doe`.

#### Step 2: Generate Token

Given that all passwords are set to `123456789`, we'll use this password along with the username `john_doe` to obtain a token.

```bash
curl -X POST "http://localhost:8000/token" -d "username=john_doe&password=123456789"
```

This should return an access token. Copy this token for future requests.
Example:
```
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTYXJhaCIsImV4cCI6MTY5ODgwMDUyNX0.DD6xF6zxtqeeEl10uFsyX0MKxUbxZDe1oeehSASwWy0","token_type":"bearer"}
```

#### Step 3: Upload QR Code

Now that you have the access token, you can use it to upload a QR code. Make sure to replace `<YOUR_ACCESS_TOKEN>` with the token you received in the previous step and `<PATH_TO_YOUR_FILE>` with the path to your qrcode file. Let's use the `update_dept_qr.png` that was generated during the seed step.

It contains the  following data to update the `user`:
```
    {
        "id": user.id,
        "name": "existing_user",
        "department": new_department,
        "department_role": user_role,
    }
```

```bash
curl -X POST "http://localhost:8000/upload_qr/" -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" -F "file=@./update_dept_qr.png"

```
Executing this will **upload** the QR code file and the endpoint should **process** it and return relevant data or any response message set by the backend:

```
{"detail":"QR code processed","data":{"user_id":"19f890aa-01a2-4a9f-804d-54b2ee258d85","username":"existing_user","department_name":"Hr","role":"admin"}}


```

Without the authentication token this endpoint will return:
```
{"detail":"Could not validate credentials"}
```
### Example using Swagger:

Let's use the Swagger UI for testing the endpoint `delete_department` 

1. **Open Swagger UI**: Navigate to your Swagger UI, usually it's hosted at `http://localhost:8000/docs` if you're running the application locally.

2. **Endpoint `GET department_roles`**: This endpoint is open to public. You can retrieve the `user_id` who has `admin` role at a certain department `department_id`.
   
   ![image description](misc/get_department_roles.png)

4. **Endpoint `GET /user/{user_id}`**: This endpoint is also open to public. You can retrieve the `name` of the `user` we have retrieved at the step `2`
   ![image description](misc/alyssa_by_id.png)

4. **Authorization**: 
   - Add the user `name` and common password `123456789` to log in

    ![image description](misc/alyssa_logged_in.png)
   
6. **Endpoint `DELETE department`**: As the description of the endpoint indicates, the authenticated user must be the admin of the department to be able to delete it.\
Use the `department_id` from the `step 2` to test the endpoint

    ![image description](misc/admin_deleted_department.png)

When the user is not admin(i.e member), forbidden message is sent in the response

![image description](misc/member_try_delete_department.png)


### Tests

This project utilizes `pytest` for testing. Tests are designed to interact with a local PostgreSQL database named `qrcode_processor_db_test`. Focus has been on integration tests to ensure the overall functionality of the application.

#### Requirements:

- Make sure you have `pytest` installed. If not, install it using:
  ```bash
  pip install pytest
  ```

- Ensure you have a local PostgreSQL server running and create a test database named `qrcode_processor_db_test`.

#### How to Run Tests:

1. Navigate to the project root directory.
2. Set up the necessary environment variable:
   ```bash
   export DATABASE_URL="postgresql://localhost/qrcode_processor_db_test"
   ```
3. Run the tests using the `pytest` command. To run all tests, simply use:
   ```bash
   pytest
   ```
   If you want to run specific tests, for example, tests related to user routes, you can specify the file:
   ```bash
   pytest tests/test_user_routes.py
   ```

#### Test Fixtures:

The provided fixtures in the tests help to set up and tear down sample data for testing purposes:

- `db_session`: Provides a database session for the test module.
- `sample_users`: Sets up multiple sample users.
- `sample_departments`: Sets up sample departments.
- `sample_department_roles`: Assigns sample roles to users for specific departments.
- `sample_user`, `sample_department`, `sample_department_role`: Set up individual sample data for their respective entities.


### Assumptions:
No Explicit Many-To-Many Table for Users and Departments:

Instead of a direct many-to-many relationship between `Users` and `Departments`, a separate `DepartmentRole` table acts as the associative table, which not only maps the relationship but also adds metadata in terms of roles. This provides more context to the relationship between a user and a department.

No `HTTPS` request as the purpose off the app is for demonstration on local machine.







 



