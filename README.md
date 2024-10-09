# Health Data App

**HealthData** ist eine Webanwendung, die Gesundheitsdaten aus der **WHO GHO API** visulisiert.

## Voraussetzungen

Bevor Sie die Anwendung lokal starten, stellen Sie sicher, dass Sie die folgenden Software-Tools installiert hast:

- **Node.js** (Version 14.x oder höher) und **npm**
- **Python 3.10** oder höher
- **MySQL** (Version 8.0 oder höher)
- **Git**

## Installation

### 1. Repository klonen

Klonen des Repositories von GitHub:

```bash
git clone https://github.com/olliStr/health-data-react.git
cd health-data-react
```

### 2. MySQL-Datenbank einrichten

Starten Sie MySQL-Workbench und wählen Sie eine Connection (hier: localhost). Erstellen Sie einen neuen MySQL-Benutzer und eine Datenbank:

```bash
CREATE DATABASE health_data;
CREATE USER 'health_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON health_data.* TO 'health_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Erstellen Sie in dem Ordner **backend** eine .env Datei und fügen Sie folgenden Eintrag hinzu:

```bash
DATABASE_URL="mysql+pymysql://health_user:password@localhost/health_data"
```

### 3. Backend installieren und starten

Erstellen Sie eine virtuelle Umgebung und aktivieren Sie diese:

```bash
cd backend
python3 -m venv venv
venv\Scripts\activate
```

Installieren Sie alle Abhängigkeiten:

```bash
pip install -r requirements.txt
```

Starten Sie das Fackend:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Frontend installieren und starten

Installieren Sie die abhängigkeiten

```bash
cd frontend
npm install
```

Starten Sie das Frontend:

```bash
npm run dev
```

### Anwendung aufrufen

Öffnen Sie ihren Browser und gehen Sie auf **http://localhost:3000**