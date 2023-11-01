import uuid

from faker import Faker

import models
from database import SessionLocal, engine
from security import hash_password
from services import qrcode_process_service

fake = Faker()

models.Base.metadata.create_all(bind=engine)

"""
Seed the database with sample data. It will create 50 users, 5 departments, and assign a random department to each user.
It will assign one admin per department.
It will also create example QR codes files for different scenarios.
"""


def seed_database():
    db = SessionLocal()

    try:
        # Seed departments
        department_names = ["Hr", "Engineering", "Marketing", "Finance", "Sales"]
        for name in department_names:
            department = models.Department(name=name)
            db.add(department)
        db.commit()

        # Seed users and their roles
        common_password = "123456789"  # Set a common password for all users
        hashed_common_password = hash_password(common_password)

        for _ in range(50):
            user = models.User(
                name=fake.first_name(), hashed_password=hashed_common_password
            )
            db.add(user)
            db.commit()

            # Assign a random department and set one admin per department
            department = fake.random_element(elements=department_names)
            department_obj = (
                db.query(models.Department).filter_by(name=department).first()
            )

            # Check if department already has an admin, else set the user as admin
            role = (
                "admin"
                if not db.query(models.DepartmentRole)
                .filter_by(department_id=department_obj.id, role="admin")
                .first()
                else "member"
            )

            department_role = models.DepartmentRole(
                user_id=user.id, department_id=department_obj.id, role=role
            )
            db.add(department_role)
            db.commit()

            print(f"Added user {user.name} with role {role} in department {department}")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()

    finally:
        db.close()
        print(f"Seed DONE. Closing connection.")
        print(f"Count of users: {db.query(models.User).count()}")
        print(f"Count of departments: {db.query(models.Department).count()}")
        print(f"Count of department roles: {db.query(models.DepartmentRole).count()}")
        print(
            f"Each department name and its admin count: {db.query(models.Department.name, models.DepartmentRole.role, models.DepartmentRole.user_id).join(models.DepartmentRole).filter(models.DepartmentRole.role == 'admin').all()}"
        )

    print(f"Fetch three different users from the database:")
    session = SessionLocal()
    existing_users = session.query(models.User).limit(3).all()

    if existing_users and len(existing_users) >= 3:
        user_1 = existing_users[0]
        user_2 = existing_users[1]
        user_3 = existing_users[2]

        # For user_1, different department
        if user_1.department_roles:
            other_departments = [
                dept
                for dept in department_names
                if dept != user_1.department_roles[0].department.name
            ]
            user_1_new_department = fake.random_element(elements=other_departments)
        else:
            user_1_new_department = fake.random_element(elements=department_names)

        # For user_2, different department and role
        if user_2.department_roles:
            other_departments_for_user_2 = [
                dept
                for dept in department_names
                if dept != user_2.department_roles[0].department.name
            ]
            user_2_new_department = fake.random_element(
                elements=other_departments_for_user_2
            )
            user_2_new_role = (
                "admin" if user_2.department_roles[0].role != "admin" else "member"
            )
        else:
            user_2_new_department = fake.random_element(elements=department_names)
            user_2_new_role = "admin"

        example_users = [
            {
                "id": str(user_1.id),
                "name": "existing_user",
                "department": user_1_new_department,
                "department_role": user_1.department_roles[0].role,
                "scenario": "update_dept",
            },
            {
                "id": str(user_2.id),
                "name": "existing_user",
                "department": user_2_new_department,
                "department_role": user_2_new_role,
                "scenario": "update_dept_role",
            },
            {
                "id": str(user_3.id),
                "name": "existing_user",
                "department": user_3.department_roles[0].department.name,
                "department_role": user_3.department_roles[0].role,
                "scenario": "up_to_date",
            },
            {
                "id": "unknown_data",
                "name": "unknown_data",
                "department": "unknown_data",
                "department_role": "unknown_data",
                "scenario": "unprocessable",
            },
        ]

        qrcode_process_service.generate_example_qr_codes(example_users)
        print(
            "QR code generation DONE. Check the test_qrcodes directory for the generated QR codes."
        )
        print("Closing connection.")
    else:
        print(
            "Less than three users found in the database. Skipping QR code generation."
        )

    session.close()


if __name__ == "__main__":
    seed_database()
