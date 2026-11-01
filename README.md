# PC Specs

Client–server tool for **hardware inventory and remote diagnostics** of Windows workstations on an internal network. Built in Python (2022–2023) while working in an IT area that kept track of its PCs by hand.

## The problem

The IT team kept the inventory of every workstation (user, department, IP, OS, CPU, RAM, disk, UPS) manually, PC by PC. The data was always out of date, and checking a remote machine meant walking to it.

## What it does

**Server** (`servidor/`) — runs on every workstation:
- On first run, a small Tkinter form asks for the assigned user and department, loaded live from the existing inventory database.
- Collects the hardware specs automatically (`platform`, `psutil`, `py-cpuinfo`, `wmic`) and normalizes them to the catalog values the database expects (e.g. a 465 GB disk is stored as the "500 GB" catalog entry).
- Saves the data in a local CSV-style file and **upserts** it into MySQL through the Peewee ORM (insert if the IP is new, update otherwise).
- Starts automatically at logon via a Windows scheduled task and listens on a TCP socket for the technician's client.

**Client** (`cliente/`) — console app for the technician:
- **Network scan**: pings a range of a `/24` network with one thread per IP and lists which PCs are on, off or unreachable.
- **Remote specs**: requests the hardware data of any PC on the network.
- **Live bandwidth**: streams the remote PC's network usage every second (and the local one).
- **Remote console**: runs diagnostic commands on the remote PC and returns the output.

```
 Technician PC                         Workstation (x N)
┌─────────────────┐   TCP :55555     ┌──────────────────────────┐
│ cliente         │ ───────────────▶ │ servidor                 │
│  · IP scan      │  "Lista"         │  · collects specs        │
│  · specs        │  "bandwidth"     │  · socket listener       │──▶ MySQL (inventory)
│  · bandwidth    │  "cmd"           │  · Tkinter first-run form│
│  · remote cmd   │ ◀─────────────── │                          │
└─────────────────┘                  └──────────────────────────┘
```

## Tech

Python 3 · Tkinter · sockets (TCP) · threading · Peewee ORM · MySQL / PyMySQL · psutil · py-cpuinfo · PyInstaller · Windows Task Scheduler

## Run it

```bash
pip install -r requirements.txt
```

The server reads the database connection from environment variables:

| Variable | Default |
|---|---|
| `PCSPECS_DB_HOST` | `127.0.0.1` |
| `PCSPECS_DB_PORT` | `3306` |
| `PCSPECS_DB_NAME` | `pc_specs` |
| `PCSPECS_DB_USER` | `pc_specs_user` |
| `PCSPECS_DB_PASSWORD` | *(empty)* |

The database must already contain the inventory tables the tool reads from (`personal`, `dependencia`, `computadora`, `procesador`, `memoria`); the `Lista_Pc_Specs` table is created automatically.

```bash
# Server (on each workstation)
cd servidor && python PC_Specs.py

# Client (technician)
cd cliente && python Consola_PC_Specs.py
```

### Building the executables

```bash
cd servidor && pyinstaller --windowed --onefile --icon=./logo.ico PC_Specs.py
cd cliente  && pyinstaller --onefile --icon=./logo.ico Consola_PC_Specs.py
```

### Deploying on a workstation

1. Copy the `servidor` folder to `C:\Servidor`.
2. Run `C:\Servidor\dist\PC_Specs.exe`, fill in the form and accept.
3. Open **Task Scheduler** as administrator and import `servidor/tarea_programada.xml` (it starts the server at logon; Windows will ask for the account to run it with).
4. Allow ping responses so the client's network scan can see the PC:
   ```
   netsh advfirewall firewall add rule name="Habilitar respuesta ICMP IPv4" protocol=icmpv4:8,any dir=in action=allow
   ```

## Security note

This was designed for an **isolated internal network**, early in my career. The remote console executes commands **without authentication or encryption**, so it must never be exposed outside a trusted network. If I built it today I would add:

- Authentication (shared secret or certificates) and TLS on the socket.
- An allow-list of diagnostic commands instead of arbitrary execution.
- Configuration via environment variables from day one (now done) and parameterized batch updates instead of one query per field.

## What I learned

My first real client–server system: designing a minimal text protocol over raw sockets, handling concurrent scans with threads, mapping messy real-world data onto an existing database schema, and packaging a Python app so non-technical users could deploy it.
