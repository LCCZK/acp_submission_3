import psycopg2
from postgres_cfg import PostgresCfg as cfg

conn = psycopg2.connect(**cfg.CONNECTION)
cur = conn.cursor()
cur.execute(f"DROP TABLE IF EXISTS {cfg.TABLE_NAME}")
cur.execute(f"""CREATE TABLE {cfg.TABLE_NAME} (employer_id INTEGER PRIMARY KEY,
                                            name VARCHAR(100) NOT NULL,
                                            department VARCHAR(50) NOT NULL,
                                            role VARCHAR(100) NOT NULL,
                                            email VARCHAR(150) NOT NULL)""")

employees = [
    (1001, "Alice Chen",    "Engineering",  "Senior Developer",    "alice.chen@company.com"),
    (1002, "Bob Martinez",  "Engineering",  "DevOps Engineer",     "bob.martinez@company.com"),
    (1003, "Carol Smith",   "Marketing",    "Marketing Manager",   "carol.smith@company.com"),
    (1004, "Dave Wilson",   "Engineering",  "Junior Developer",    "dave.wilson@company.com"),
    (1005, "Eva Johnson",   "HR",           "HR Director",         "eva.johnson@company.com"),
    (1006, "Frank Lee",     "Marketing",    "Content Specialist",  "frank.lee@company.com"),
    (1007, "Grace Kim",     "Finance",      "Financial Analyst",   "grace.kim@company.com"),
    (1008, "Henry Brown",   "Engineering",  "Tech Lead",           "henry.brown@company.com"),
    (1009, "Iris Patel",    "HR",           "Recruiter",           "iris.patel@company.com"),
    (1010, "Jack Taylor",   "Finance",      "Finance Manager",     "jack.taylor@company.com"),]

cur.executemany(
    f"INSERT INTO {cfg.TABLE_NAME} (employer_id, name, department, role, email) VALUES (%s, %s, %s, %s, %s)",
    employees
)
conn.commit()

cur.execute(f"SELECT * FROM {cfg.TABLE_NAME}")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()