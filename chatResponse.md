We should build it from the inside out, not start with the dashboard.
For SOC-X V1, our first goal should be very small:
Generate/collect one real security log → send it to our backend → store it in MySQL → retrieve it successfully.
Once that works, we'll build detection on top of it.

Development order
PHASE 1
Project Setup
    ↓
PHASE 2
MySQL Database
    ↓
PHASE 3
Log Collector
    ↓
PHASE 4
Log Normalization
    ↓
PHASE 5
Detection Engine
    ↓
PHASE 6
Alert Management
    ↓
PHASE 7
SOC Dashboard
    ↓
PHASE 8
Real-time Alerts
    ↓
PHASE 9
Incident Management
    ↓
PHASE 10
MITRE ATT&CK
    ↓
PHASE 11
Threat Intelligence
    ↓
PHASE 12
Automated Response
So, first we build the foundation
Step 1 — Create the project

We'll create:

SOC-X/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   └── services/
│   │
│   └── requirements.txt
│
├── collector/
│   └── linux_collector.py
│
├── frontend/
│
├── detection/
│
├── tests/
│
└── README.md

Don't worry if this looks complicated. We'll create it one piece at a time.

Step 2 — Set up MySQL

Create our database:

soc_x

Initially, we only need one table:

logs

Something like:

logs
────────────────────────────
id
timestamp
source
event_type
source_ip
username
message
severity
created_at

We don't need 10 tables on day one.

Step 3 — Create the FastAPI server

Our first API should be extremely simple:

POST /api/logs

The collector sends:

{
    "event_type": "failed_login",
    "source": "ubuntu",
    "source_ip": "192.168.80.25",
    "username": "admin",
    "message": "Failed password for admin"
}

FastAPI receives it:

Collector
    ↓
POST /api/logs
    ↓
FastAPI
    ↓
MySQL
Step 4 — Build the first log collector

For our first real security data source, I'd use Ubuntu/Linux authentication logs.

For example, when someone attempts an SSH login:

Failed password for admin from 192.168.80.25

Our Python collector will read the log and convert it into structured data:

Raw log
   ↓
Parser
   ↓
Structured event
   ↓
FastAPI
   ↓
MySQL

This is where you'll start learning an important SOC concept:

raw security logs → normalized security events

Step 5 — Verify the entire pipeline

Before building detection, we need to prove this works:

Kali
 │
 │ controlled SSH attempts
 ↓
Ubuntu
 │
 │ authentication log
 ↓
Linux Collector
 │
 ↓
FastAPI
 │
 ↓
MySQL

Then query MySQL:

SELECT * FROM logs;

and see:

ID    EVENT          SOURCE IP        USER
1     failed_login   192.168.80.25    admin
2     failed_login   192.168.80.25    admin
3     failed_login   192.168.80.25    admin

At this point, we have the foundation of our SOC.

Then comes the interesting part

Once the above works, we build:

5 Failed Login Attempts
          ↓
Detection Rule
          ↓
Brute Force Detected
          ↓
Alert Generated
          ↓
Severity = HIGH
          ↓
SOC Dashboard

Then eventually:

Alert
 ↓
Investigation
 ↓
MITRE ATT&CK
 ↓
Threat Intelligence
 ↓
Incident
 ↓
Response
Our immediate target

Let's not start coding everything at once.

First milestone:

SOC-X → FastAPI + MySQL + /api/logs + logs table

After that, we'll connect the Linux collector.

If you're ready, I can give you Step 1 with the exact installation commands, project folder structure, Python virtual environment, MySQL database creation, and the first FastAPI code, and we'll build it together step-by-step.

i have created the folder ad all files as shown in the step 1 now step 2 tell me step by step

Perfect. Since your SOC-X folder structure is already created, let's now do Phase 2: MySQL Database Setup.

For this phase, our goal is only:

Create the MySQL database → create the logs table → connect Python/FastAPI to MySQL → verify the connection.

Don't create the collector or detection engine yet.

Step 2 — MySQL Setup
2.1 Check that MySQL is running

If you're using MySQL Workbench:

Open MySQL Workbench.
Open your local MySQL connection.
Make sure you can access the SQL editor.

You can test:

SELECT VERSION();

If you get something like:

8.0.xx

MySQL is working.

2.2 Create the SOC-X database

Run:

CREATE DATABASE soc_x;

Then:

USE soc_x;

Verify:

SELECT DATABASE();

You should get:

soc_x
2.3 Create the first table

For now, we only need the logs table.

Run:

CREATE TABLE logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NULL,
    source VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    source_ip VARCHAR(45),
    destination_ip VARCHAR(45),
    username VARCHAR(100),
    message TEXT,
    severity ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') DEFAULT 'LOW',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Why these columns?
Column	Purpose
id	Unique log ID
timestamp	Time when the security event occurred
source	Linux, Windows, firewall, etc.
event_type	failed_login, successful_login, etc.
source_ip	IP generating the event
destination_ip	Target IP
username	Account involved
message	Original log message
severity	Initial severity
created_at	Time SOC-X stored the log
2.4 Verify the table

Run:

SHOW TABLES;

You should see:

logs

Then:

DESCRIBE logs;

You should see the columns we created.

2.5 Insert a test security event

Before connecting Python, let's make sure the table works.

Run:

INSERT INTO logs (
    timestamp,
    source,
    event_type,
    source_ip,
    username,
    message,
    severity
)
VALUES (
    NOW(),
    'ubuntu',
    'failed_login',
    '192.168.80.25',
    'admin',
    'Failed password for admin',
    'MEDIUM'
);

Now:

SELECT * FROM logs;

You should see your test event.

Something like:

id | timestamp           | source | event_type    | source_ip      | username
1  | 2026-09-18 11:xx:xx | ubuntu | failed_login  | 192.168.80.25  | admin

If this works, your database is ready.

2.6 Now connect Python to MySQL

Go to:

SOC-X/
└── backend/

Open your terminal inside the backend folder.

Create a virtual environment:

Windows
python -m venv venv

Activate it:

venv\Scripts\activate

You should see something like:

(venv) C:\...\SOC-X\backend>
2.7 Install required Python packages

Run:

pip install fastapi uvicorn sqlalchemy pymysql python-dotenv

These are our initial dependencies.

What each does
Package	Purpose
FastAPI	Backend API
Uvicorn	Runs FastAPI
SQLAlchemy	Database ORM
PyMySQL	MySQL driver
python-dotenv	Stores database credentials safely

Then save them:

pip freeze > requirements.txt

Your existing:

backend/
└── requirements.txt

will now contain the dependencies.

2.8 Create database.py

You already created:

backend/
└── app/
    └── database.py

Open database.py and put:

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "soc_x")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
2.9 Create .env

Inside:

SOC-X/backend/

create:

.env

So you have:

backend/
│
├── app/
│   └── database.py
│
├── requirements.txt
└── .env

Put your MySQL credentials in .env:

DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_HOST=localhost
DB_PORT=3306
DB_NAME=soc_x

Replace:

YOUR_MYSQL_PASSWORD

with the password you use to connect to MySQL.

Important

Do not put the password directly inside database.py.

And later we'll add .env to .gitignore so your password isn't uploaded to GitHub.

2.10 Create the Log model

Now open:

backend/app/models/

Create:

log.py

Put:

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    timestamp: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    source_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )

    destination_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )

    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    severity: Mapped[str] = mapped_column(
        Enum("LOW", "MEDIUM", "HIGH", "CRITICAL"),
        default="LOW"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

Also create:

backend/app/models/__init__.py

It can remain empty for now.

2.11 Test the Python → MySQL connection

Now let's create a very small test.

Open:

backend/app/main.py

Put:

from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

app = FastAPI(title="SOC-X")


@app.get("/")
def root():
    return {
        "message": "SOC-X backend is running"
    }


@app.get("/health/database")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "MySQL"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
2.12 Start FastAPI

From:

SOC-X/backend/

run:

uvicorn app.main:app --reload

You should see:

Uvicorn running on http://127.0.0.1:8000

Open your browser:

http://127.0.0.1:8000

You should get:

{
    "message": "SOC-X backend is running"
}
2.13 Test MySQL connection

Open:

http://127.0.0.1:8000/health/database

Expected:

{
    "status": "healthy",
    "database": "MySQL"
}

If you get that response:

Phase 2 is successfully completed.

Your folder should now look like this
SOC-X/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── log.py
│   │   │
│   │   ├── schemas/
│   │   ├── routes/
│   │   └── services/
│   │
│   ├── .env
│   ├── requirements.txt
│   └── venv/
│
├── collector/
│
├── detection/
│
├── frontend/
│
├── tests/
│
└── README.md
Don't move to the next phase until this works.

The exact checkpoint is:

MySQL
  ↓
soc_x database
  ↓
logs table
  ↓
FastAPI
  ↓
SQLAlchemy
  ↓
PyMySQL
  ↓
/health/database
  ↓
"healthy"

Once you get "status": "healthy", the next step will be Phase 3 — building the Linux Log Collector, where we'll make SOC-X receive an actual SSH authentication event from your Ubuntu machine instead of manually inserting fake logs.

lets start next phase

Great. Now we move to Phase 4 — Linux Log Collector.

The goal of this phase is to stop manually entering logs through Swagger. Our SOC should automatically receive security events from a Linux machine.

What we're building now
             Ubuntu Server
                  │
                  ↓
             auth.log
                  │
                  ↓
        linux_collector.py
                  │
             HTTP POST
                  │
                  ↓
            FastAPI SOC-X
                  │
                  ↓
               MySQL
                  │
                  ↓
              logs table

We'll first make it work with Ubuntu authentication logs, especially SSH events.

Step 4.1 — Where should the collector run?

Important distinction:

FastAPI server

Your current SOC-X backend can run on your Windows machine:

Windows
└── SOC-X Backend
    └── FastAPI
Collector

The collector should run on the Ubuntu machine whose logs we want to monitor:

Ubuntu
└── SOC-X Collector
    └── linux_collector.py

So eventually:

Ubuntu ────────────────→ Windows
Collector               FastAPI
                           ↓
                         MySQL

For our first test, we'll make sure the Ubuntu machine can reach the FastAPI machine.

Step 4.2 — Find the FastAPI machine's IP

On the Windows machine where FastAPI is running, open CMD:

ipconfig

Find your active network adapter and look for:

IPv4 Address

For example:

192.168.80.10

Don't use 127.0.0.1 in the Ubuntu collector.

Why?

127.0.0.1

means the current machine itself.

From Ubuntu, 127.0.0.1 means Ubuntu, not your Windows computer.

Step 4.3 — Test connectivity from Ubuntu

On Ubuntu:

ping YOUR_WINDOWS_IP

For example:

ping 192.168.80.10

If you receive:

64 bytes from 192.168.80.10...

the machines can communicate.

If ping doesn't work, don't worry yet; some firewalls block ICMP. We can test the API directly next.

Step 4.4 — Make FastAPI accessible on the network

Currently you're probably starting FastAPI with:

uvicorn app.main:app --reload

That normally binds it to:

127.0.0.1

which means only your Windows machine can access it.

Stop it:

CTRL + C

Then start:

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Now FastAPI listens on network interfaces too.

Your Windows browser can still use:

http://127.0.0.1:8000/docs

But Ubuntu should use:

http://YOUR_WINDOWS_IP:8000/docs

For example:

http://192.168.80.10:8000/docs
Step 4.5 — Test from Ubuntu

Open a browser on Ubuntu if you have one, or use:

curl http://YOUR_WINDOWS_IP:8000/

Example:

curl http://192.168.80.10:8000/

Expected:

{"message":"SOC-X backend is running"}

If you get this, our network connection is working.

Step 4.6 — Check Ubuntu's authentication log

On Ubuntu, run:

sudo tail -n 20 /var/log/auth.log

You should see authentication-related events.

For example:

Failed password for ...
Accepted password for ...
Invalid user ...

This is the raw data our SOC collector will consume.

Important

Don't modify or delete the log.

We're only reading it.

Step 4.7 — Install Python dependencies on Ubuntu

On Ubuntu:

python3 --version

Then create a collector environment:

mkdir -p ~/soc-x-collector
cd ~/soc-x-collector

Create virtual environment:

python3 -m venv venv

If Ubuntu says that venv isn't installed:

sudo apt install python3-venv

Then:

source venv/bin/activate

Install:

pip install requests
Step 4.8 — Create the collector

Inside:

~/soc-x-collector/

create:

linux_collector.py

Put this in it:

import os
import time
import requests


SOC_API_URL = os.getenv(
    "SOC_API_URL",
    "http://192.168.80.10:8000/api/logs/"
)

LOG_FILE = "/var/log/auth.log"


def send_log(log_data):
    try:
        response = requests.post(
            SOC_API_URL,
            json=log_data,
            timeout=5
        )

        if response.status_code == 200:
            print("[+] Log sent successfully")
        else:
            print(
                f"[-] API error: {response.status_code} "
                f"{response.text}"
            )

    except requests.RequestException as e:
        print(f"[-] Could not connect to SOC-X: {e}")


def process_line(line):
    line = line.strip()

    if not line:
        return

    log_data = {
        "source": "ubuntu",
        "event_type": "authentication_event",
        "message": line,
        "severity": "LOW"
    }

    send_log(log_data)


def monitor_log():
    print(f"[*] Monitoring {LOG_FILE}")
    print(f"[*] Sending logs to {SOC_API_URL}")

    with open(LOG_FILE, "r") as file:
        file.seek(0, os.SEEK_END)

        while True:
            line = file.readline()

            if line:
                process_line(line)
            else:
                time.sleep(1)


if __name__ == "__main__":
    monitor_log()
Change this line
"http://192.168.80.10:8000/api/logs/"

to the actual IPv4 address of your Windows machine.

Step 4.9 — Run the collector

Because /var/log/auth.log requires elevated privileges, run:

sudo ~/soc-x-collector/venv/bin/python ~/soc-x-collector/linux_collector.py

You should see:

[*] Monitoring /var/log/auth.log
[*] Sending logs to http://192.168.80.10:8000/api/logs/

At this point the collector is waiting for a new authentication event.

Step 4.10 — Generate a test event

On your Ubuntu machine, make a controlled SSH login attempt against your own Ubuntu lab machine.

For example, from your Kali lab machine:

ssh wronguser@UBUNTU_IP

Enter an incorrect password.

This should create an authentication event in Ubuntu's log.

The collector should print:

[+] Log sent successfully
Step 4.11 — Check MySQL

Go to MySQL Workbench and run:

USE soc_x;

SELECT
    id,
    timestamp,
    source,
    event_type,
    source_ip,
    username,
    message,
    severity
FROM logs
ORDER BY id DESC
LIMIT 10;

You should now see an event originating from the Ubuntu collector.

One limitation in our first version

Notice that our current collector sends:

{
    "source": "ubuntu",
    "event_type": "authentication_event",
    "message": "raw log line",
    "severity": "LOW"
}

It doesn't yet understand that:

Failed password for admin from 192.168.80.25

means:

event_type = failed_login
username = admin
source_ip = 192.168.80.25

That's intentional.

The next step after proving collection works will be:

RAW LOG
   ↓
PARSER
   ↓
Structured Event
   ↓
{
  event_type: "failed_login",
  username: "admin",
  source_ip: "...",
  ...
}
   ↓
FastAPI
   ↓
MySQL

That is log normalization/parsing, and it is an important SOC concept.

Your checkpoint for this phase

Don't move ahead until this works:

Kali/Ubuntu test event
        ↓
/var/log/auth.log
        ↓
linux_collector.py
        ↓
POST /api/logs/
        ↓
FastAPI
        ↓
MySQL
        ↓
SELECT * FROM logs

If you encounter an error at any step, send me the exact terminal output, and we'll fix that step before continuing.

Perfect. This confirms the APT lock is no longer held.

PID 3344 → no longer exists.
fuser → nothing is holding /var/lib/dpkg/lock-frontend.
The unattended-upgrade-shutdown process you see is not currently holding that lock.

So we can continue.

1. Install pip

Run:

sudo apt install python3-pip

If it asks:

Do you want to continue? [Y/n]

type:

Y
2. Make sure you're using the correct SOC-X venv

After installation:

deactivate

Your prompt should become:

ubuntu@ubuntu:~/soc-x-collector$

Then activate the correct environment:

source ~/soc-x-collector/venv/bin/activate

Check:

which python

It must show:

/home/ubuntu/soc-x-collector/venv/bin/python
3. Check pip inside this venv

Run:

python -m pip --version

If that works, install Requests:

python -m pip install requests

Then verify:

python -c "import requests; print(requests.__version__)"
4. Test the collector WITHOUT sudo first

Run:

python ~/soc-x-collector/linux_collector.py

If you get:

PermissionError: [Errno 13] Permission denied: '/var/log/auth.log'

that's actually good at this stage — it means the requests problem is solved and we're now hitting the expected permission restriction.

Then we'll run it with the correct privileges:

sudo ~/soc-x-collector/venv/bin/python ~/soc-x-collector/linux_collector.py
Your immediate target

Get this command working:

python -c "import requests; print(requests.__version__)"

Once that prints a version number, we're ready to test the actual collector.

done

Great. Now we can continue with Phase 4 — actually running the Linux log collector.

Step 1 — Make sure you're in the correct venv

Run:

which python

It should show:

/home/ubuntu/soc-x-collector/venv/bin/python
Step 2 — Check the collector's API address

Open:

nano ~/soc-x-collector/linux_collector.py

Find:

SOC_API_URL = os.getenv(
    "SOC_API_URL",
    "http://192.168.80.10:8000/api/logs/"
)

Replace 192.168.80.10 with the IPv4 address of the Windows computer running FastAPI.

For example, if Windows has:

IPv4 Address: 192.168.80.15

then:

SOC_API_URL = os.getenv(
    "SOC_API_URL",
    "http://192.168.80.15:8000/api/logs/"
)

Save in nano:

CTRL + O
ENTER
CTRL + X
Step 3 — Make sure FastAPI is accessible

On your Windows machine, start SOC-X:

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Keep this terminal running.

Then, from Ubuntu, test:

curl http://WINDOWS_IP:8000/

For example:

curl http://192.168.80.15:8000/

You should get:

{"message":"SOC-X backend is running"}

If you get that, the Ubuntu → Windows connection is working.

Step 4 — Start the collector

On Ubuntu:

sudo ~/soc-x-collector/venv/bin/python ~/soc-x-collector/linux_collector.py

You should see:

[*] Monitoring /var/log/auth.log
[*] Sending logs to http://192.168.80.15:8000/api/logs/

Leave this terminal running.

Step 5 — Generate a test authentication event

Open another Ubuntu terminal and run:

sudo -k
sudo -v

Enter an incorrect password once or twice.

Or, better, from your Kali lab machine, make a controlled SSH attempt against your Ubuntu machine using an intentionally incorrect credential.

The Ubuntu /var/log/auth.log should receive something like:

Failed password for ...

Your collector should then show:

[+] Log sent successfully
Step 6 — Check MySQL

In MySQL Workbench:

USE soc_x;

SELECT *
FROM logs
ORDER BY id DESC
LIMIT 10;

You should see the new Ubuntu authentication event.

Our milestone

Once this works, we've achieved:

Kali / Ubuntu test
        ↓
Ubuntu auth.log
        ↓
Linux Collector
        ↓
FastAPI
        ↓
MySQL
        ↓
SOC-X

Then we'll do the important upgrade: teach the collector to understand the raw log instead of storing everything as authentication_event.

For example:

Raw:
Failed password for admin from 192.168.80.25

             ↓

Structured:
event_type = failed_login
username   = admin
source_ip  = 192.168.80.25

That will be Phase 5: Log Parsing & Normalization, followed by our first real SOC detection rule: SSH Brute Force Detection.

Yes. Let's insert 5 controlled failed-login events into MySQL so we can test the detection engine.

1. Open MySQL

On your Windows machine:

mysql -u root -p

Then:

USE soc_x;
2. Insert 5 failed-login events

Use the same source IP for all five:

INSERT INTO logs
(timestamp, source, event_type, source_ip, username, message, severity)
VALUES
(NOW(), 'ubuntu', 'failed_login', '192.168.80.25', 'admin', 'Failed password for admin from 192.168.80.25', 'MEDIUM'),
(NOW(), 'ubuntu', 'failed_login', '192.168.80.25', 'admin', 'Failed password for admin from 192.168.80.25', 'MEDIUM'),
(NOW(), 'ubuntu', 'failed_login', '192.168.80.25', 'admin', 'Failed password for admin from 192.168.80.25', 'MEDIUM'),
(NOW(), 'ubuntu', 'failed_login', '192.168.80.25', 'admin', 'Failed password for admin from 192.168.80.25', 'MEDIUM'),
(NOW(), 'ubuntu', 'failed_login', '192.168.80.25', 'admin', 'Failed password for admin from 192.168.80.25', 'MEDIUM');
3. Verify the five events
SELECT
    id,
    timestamp,
    event_type,
    source_ip,
    username,
    severity
FROM logs
WHERE source_ip = '192.168.80.25'
ORDER BY id DESC
LIMIT 5;

You should see five failed_login records.

One important point

The detection code looks at:

failed_login
+
same source_ip
+
last 5 minutes

So using NOW() for all five makes this a good controlled test.

Once you confirm that the 5 rows are present, we'll run the detection engine and verify that this appears in alerts:

SSH_BRUTE_FORCE
192.168.80.25
HIGH
OPEN

Send me the output of the SELECT query after inserting them.

Yes — the screenshot confirms the 5 failed-login events were inserted successfully.

You have:

ID    Event          Source IP       Username   Severity
29    failed_login   192.168.80.25   admin      MEDIUM
28    failed_login   192.168.80.25   admin      MEDIUM
27    failed_login   192.168.80.25   admin      MEDIUM
26    failed_login   192.168.80.25   admin      MEDIUM
25    failed_login   192.168.80.25   admin      MEDIUM

All five have the same IP and timestamp, so they satisfy our test condition.

Next: Run the Detection Engine

Before we run it, we need to make sure SQLAlchemy knows about the new Alert model.

Open:

SOC-X/backend/app/main.py

At the top, add:

from app.models.alert import Alert

You don't actually need to use Alert directly in main.py; importing it ensures the model is loaded.

Now create a temporary test file:

SOC-X/backend/test_detection.py

Put:

from app.database import SessionLocal
from app.services.detection_engine import detect_ssh_brute_force


db = SessionLocal()

try:
    alert = detect_ssh_brute_force(
        db,
        "192.168.80.25"
    )

    if alert:
        print("ALERT CREATED")
        print("ID:", alert.id)
        print("Type:", alert.alert_type)
        print("IP:", alert.source_ip)
        print("Severity:", alert.severity)
        print("Status:", alert.status)
        print("Description:", alert.description)
    else:
        print("No alert detected")

finally:
    db.close()

Then, from:

SOC-X/backend/

run:

python test_detection.py
Expected result

You should get approximately:

ALERT CREATED
ID: 1
Type: SSH_BRUTE_FORCE
IP: 192.168.80.25
Severity: HIGH
Status: OPEN
Description: Detected 5 failed SSH login attempts from 192.168.80.25 within 5 minutes.

Then verify directly in MySQL:

USE soc_x;

SELECT * FROM alerts;

You should see the newly created SSH_BRUTE_FORCE alert.

Don't connect this to the live collector yet. First let's prove that the detection engine correctly turns those five logs into one alert.

(venv) PS D:\Clg_Projects\soc x\backend> SOC-X/backend/app/main.py
SOC-X/backend/app/main.py : The term 'SOC-X/backend/app/main.py' is not recognized 
as the name of a cmdlet, function, script file, or operable program. Check the 
spelling of the name, or if a path was included, verify that the path is correct and 
try again.
At line:1 char:1
+ SOC-X/backend/app/main.py
+ ~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (SOC-X/backend/app/main.py:String) [], 
    CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
(venv) PS D:\Clg_Projects\soc x\backend> 

That's not a code error. You tried to execute the Python file path as a PowerShell command.

You are already in:

D:\Clg_Projects\soc x\backend

So you don't need to type SOC-X/backend/app/main.py.

If you want to open main.py

Use VS Code:

code app\main.py

Or open it with Notepad:

notepad app\main.py

Then add this import near the top:

from app.models.alert import Alert
But for our current test

We don't need to run main.py.

We need to create:

D:\Clg_Projects\soc x\backend\test_detection.py

Since you're already in the backend directory, run:

notepad test_detection.py

Paste:

from app.database import SessionLocal
from app.services.detection_engine import detect_ssh_brute_force

db = SessionLocal()

try:
    alert = detect_ssh_brute_force(
        db,
        "192.168.80.25"
    )

    if alert:
        print("ALERT CREATED")
        print("ID:", alert.id)
        print("Type:", alert.alert_type)
        print("IP:", alert.source_ip)
        print("Severity:", alert.severity)
        print("Status:", alert.status)
        print("Description:", alert.description)
    else:
        print("No alert detected")

finally:
    db.close()

Save and close Notepad.

Then run:

python test_detection.py
One thing to check first

Your backend structure should now look like:

backend
│
├── app
│   ├── main.py
│   ├── database.py
│   ├── models
│   │   ├── log.py
│   │   └── alert.py
│   └── services
│       └── detection_engine.py
│
├── test_detection.py
└── ...

If python test_detection.py gives an error, send me the complete error, and we'll fix it before moving forward.

dome with this step also now what i have to do next

Good. You have now completed the first working detection rule in Phase 6.

Current SOC-X status
Phase	Status
Phase 1 — Project Setup	✅
Phase 2 — MySQL Database	✅
Phase 3 — Log Ingestion API	✅
Phase 4 — Linux Log Collection	✅
Phase 5 — Log Parsing & Normalization	✅
Phase 6.1 — Alerts Table	✅
Phase 6.2 — SSH Brute-Force Detection	✅

Now we should make the detection engine actually run automatically whenever a new log arrives.

Phase 6.3 — Connect Detection Engine to Log Ingestion

Currently:

Ubuntu
  ↓
Collector
  ↓
Parser
  ↓
FastAPI
  ↓
MySQL logs

The detection engine is separate:

MySQL logs
  ↓
Detection Engine
  ↓
Alert

We want:

Ubuntu
   ↓
Collector
   ↓
Parser
   ↓
FastAPI
   ↓
MySQL
   ↓
Detection Engine
   ↓
SSH_BRUTE_FORCE Alert
Step 1 — Modify logs.py

Open:

notepad app\routes\logs.py

At the top, add:

from app.services.detection_engine import detect_ssh_brute_force

Then modify your create_log() function.

Change this:

db.add(new_log)
db.commit()
db.refresh(new_log)

return new_log

to:

db.add(new_log)
db.commit()
db.refresh(new_log)

# Run detection after storing the log
if new_log.event_type == "failed_login" and new_log.source_ip:
    detect_ssh_brute_force(
        db,
        new_log.source_ip
    )

return new_log

So the complete endpoint becomes:

@router.post("/", response_model=LogResponse)
def create_log(log_data: LogCreate, db: Session = Depends(get_db)):

    new_log = Log(
        timestamp=log_data.timestamp or datetime.utcnow(),
        source=log_data.source,
        event_type=log_data.event_type,
        source_ip=log_data.source_ip,
        destination_ip=log_data.destination_ip,
        username=log_data.username,
        message=log_data.message,
        severity=log_data.severity
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    # Run detection after storing the log
    if new_log.event_type == "failed_login" and new_log.source_ip:
        detect_ssh_brute_force(
            db,
            new_log.source_ip
        )

    return new_log
Step 2 — Restart FastAPI

Stop your current server with:

CTRL + C

Then:

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Step 3 — Test the automatic detection

We already have an alert from our previous test, so first check:

SELECT * FROM alerts;

Then we should eventually test with fresh logs, rather than relying on the five manually inserted records.

The ideal test will be:

Kali
 ↓
5 failed SSH attempts
 ↓
Ubuntu auth.log
 ↓
Collector
 ↓
Parser
 ↓
FastAPI
 ↓
Detection Engine
 ↓
alerts table
One improvement before that

Our current detection rule checks all failed logins from the IP in the last 5 minutes. That's fine for the first version, but we should eventually add alert cooldown/deduplication, which we've already partially handled with:

Alert.status == "OPEN"

That prevents five incoming events from creating five identical open alerts.

For now, modify logs.py and restart FastAPI. After that, we'll do the real end-to-end brute-force test using Kali → Ubuntu → SOC-X.

Today 1:53 PM
done 

Excellent. Now let's do the real end-to-end test of Phase 6.

Step 6.4 — Test automatic brute-force detection

Keep your FastAPI terminal running.

Also keep your Ubuntu collector running.

Your setup should currently be:

Windows
└── FastAPI + MySQL
        ↑
        │
Ubuntu
└── Collector → /var/log/auth.log
        ↑
        │
Kali
└── Test SSH authentication
1. Generate failed SSH attempts from Kali

From Kali, target your own Ubuntu lab machine:

ssh wronguser@UBUNTU_IP

Enter an incorrect password.

Repeat the attempt until you have 5 failed attempts.

You can simply run the SSH command again after each failed attempt.

2. Watch the Ubuntu collector

You should see something like:

[*] Parsed event: {
    'event_type': 'failed_login',
    'username': 'wronguser',
    'source_ip': 'KALI_IP',
    'severity': 'MEDIUM',
    ...
}

[+] Log sent successfully
3. Check the alerts table

After the fifth failed login, go to MySQL:

USE soc_x;

SELECT
    id,
    alert_type,
    source_ip,
    username,
    severity,
    status,
    description,
    created_at
FROM alerts
ORDER BY id DESC;

You should see something similar to:

alert_type       SSH_BRUTE_FORCE
source_ip        <KALI_IP>
username         wronguser
severity         HIGH
status           OPEN
4. Also check the logs
SELECT
    id,
    event_type,
    source_ip,
    username,
    severity,
    timestamp
FROM logs
ORDER BY id DESC
LIMIT 10;

You should see the new failed_login events.

What this proves

If the alert appears automatically, you've achieved an important SOC-X milestone:

Raw Security Event
       ↓
Log Collection
       ↓
Log Parsing
       ↓
Centralized Storage
       ↓
Detection Rule
       ↓
Security Alert

That's the foundation of a SIEM/SOC monitoring system.

After this test

We'll move to Phase 6.5 — Alert API, where you'll be able to retrieve alerts through FastAPI:

GET /api/alerts/

That API will later feed your SOC dashboard.

Run the five controlled SSH failures and check alerts. If the alert appears, tell me "alert generated" and we'll build the Alert API.


fix the problem

3:40 PM
I’ll verify the exact Ubuntu source IP against the current five-minute count and open-alert deduplication before changing anything. The code already ignores interleaved generic events, so I want to distinguish a real missed detection from the expected “fewer than five” or “alert already open” cases.

I found the underlying bug: this IP already has an OPEN alert, and duplicate suppression checks only IP and status, so that old alert blocks every future alert for the same IP indefinitely. I’ll scope duplicate suppression to alerts created in the current five-minute detection window, so a later brute-force episode can produce a new alert while retries within one episode remain deduplicated. The pasted sample itself has three failed_login entries, so it still needs two more within five minutes to meet the threshold.

Edited
detection_engine.py
The change is in place. I’m validating the precise regression with a rolled-back database transaction: five fresh failures for that IP should create a new alert despite the older open one, and a repeat detection in the same window should reuse that new alert.

Checked detection_engine.py, no problems found

Fixed the stale-alert suppression in detection_engine.py: an old OPEN alert no longer blocks a new brute-force alert forever. Alerts are deduplicated only when an open alert for that IP was created within the current five-minute detection window.

I verified that five fresh failures create a new alert despite the old one, and repeated detection within that window reuses it. The test ran in a rolled-back transaction, so it left no test rows behind.

Your pasted Ubuntu output has only three failed_login events; the rule still needs five within five minutes. Restart the backend to load the change, then test with five failures in that window.

## SOC-X Frontend Dashboard

The SOC analyst dashboard displays:
- Summary cards for total logs, total alerts, open alerts, and high/critical alerts
- Recent security alerts with source IP, severity, and status
- Selectable alerts with detailed information, including alert ID, type, username, timestamp, and description
- Source IPs generating alerts and their counts
- Recent security events with event type, source IP, severity, and timestamp

The dashboard fetches its information from the SOC-X API, refreshes automatically every 10 seconds, and has a manual Refresh button. The displayed totals now come from stored records rather than randomly changing sample values; they change when the underlying logs or alerts change.

Frontend preview: http://127.0.0.1:8001/