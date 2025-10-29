# 🌍 Global Google Service Availability Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Professional monitoring tool for tracking Google services and AI/ML endpoints availability** - Essential for hosting operators, startups, and infrastructure teams.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Ban Protection](#ban-protection)
- [Automation](#automation)
- [Output & Logging](#output--logging)
- [Monitored Services](#monitored-services)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This tool provides **real-time monitoring** of Google services and AI/ML endpoints, designed specifically for:

- **Hosting Providers**: Monitor service availability for your infrastructure
- **Startups**: Track dependencies on Google services
- **DevOps Teams**: Integrate into monitoring pipelines
- **Site Reliability Engineers**: Proactive outage detection

### Why This Tool?

✅ **Auto-updating databases** - Service endpoints updated automatically  
✅ **Ban protection** - Built-in rate limiting and user-agent rotation  
✅ **Comprehensive coverage** - Monitors 12+ critical Google services  
✅ **Easy automation** - Schedule checks with cron or systemd  
✅ **JSON output** - Machine-readable results for integration  
✅ **Colored console output** - Clear visual status indicators  

## ✨ Features

### Core Functionality
- 🔄 **Periodic availability checks** with configurable intervals
- 🎯 **Multi-endpoint monitoring** for each service
- ⏱️ **Response time tracking** in milliseconds
- 📊 **Availability reports** with uptime percentages
- 💾 **JSON result storage** for historical analysis
- 📝 **Detailed logging** to file and console

### Protection Mechanisms
- 🛡️ **User-agent rotation** - 5+ different browser signatures
- ⏰ **Request throttling** - Configurable delays between checks
- 🔁 **Automatic retries** - Up to 3 attempts with exponential backoff
- 🕒 **Timeout handling** - Prevent hanging requests

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/Mortyo666/global-google-service-availability.git
cd global-google-service-availability
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install with virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ⚡ Quick Start

### Run a Single Check

```bash
python check_availability.py --once
```

### Run Continuous Monitoring

```bash
python check_availability.py
```

This will check all services every 15 minutes (configurable in `config.json`).

## ⚙️ Configuration

Edit `config.json` to customize monitoring behavior:

```json
{
  "check_interval_minutes": 15,      // How often to check (minutes)
  "timeout_seconds": 10,             // Request timeout
  "retry_attempts": 3,               // Number of retry attempts
  "request_delay_seconds": 2,        // Delay between service checks
  "user_agents": [...]               // User-agent strings for rotation
}
```

### Adding Custom Services

Add new services to the `services` section in `config.json`:

```json
"Your Service": {
  "description": "Service description",
  "endpoints": [
    "https://your-service.com",
    "https://your-service.com/api"
  ]
}
```

## 📖 Usage

### Command Line Options

```bash
# Single check (run once and exit)
python check_availability.py --once

# Continuous monitoring (scheduled checks)
python check_availability.py
```

### Example Output

```
Google Services Availability Monitor
=============================================
2024-10-30 01:00:00 - INFO - Starting availability check...
2024-10-30 01:00:00 - INFO - Checking Google Search...
✓ Google Search - https://www.google.com - 145.23ms
✓ Google Search - https://www.google.com/search?q=test - 167.89ms
✓ Gmail - https://mail.google.com - 234.56ms
...

=== Availability Report ===
Total Services Checked: 14
UP: 14 (100.0%)
DOWN: 0
Check Time: 2024-10-30 01:00:15
========================================
```

## 🛡️ Ban Protection

This tool implements multiple strategies to avoid being blocked:

### 1. User-Agent Rotation
- Rotates through 5 different browser user-agents
- Mimics real browser traffic patterns

### 2. Request Throttling
- Configurable delay between requests (default: 2 seconds)
- Prevents rapid-fire requests that trigger rate limits

### 3. Retry Logic
- Exponential backoff on failures
- Maximum 3 retry attempts per endpoint

### 4. Timeout Management
- 10-second timeout prevents hanging connections
- Graceful failure handling

### Best Practices

⚠️ **Don't set `check_interval_minutes` below 5 minutes**  
⚠️ **Keep `request_delay_seconds` at least 1 second**  
⚠️ **Don't run multiple instances simultaneously**  

## 🤖 Automation

### Using Cron (Linux/Mac)

Add to crontab (`crontab -e`):

```bash
# Run every 15 minutes
*/15 * * * * cd /path/to/global-google-service-availability && python check_availability.py --once
```

### Using systemd (Linux)

Create `/etc/systemd/system/google-monitor.service`:

```ini
[Unit]
Description=Google Services Availability Monitor
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/global-google-service-availability
ExecStart=/usr/bin/python3 check_availability.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable google-monitor
sudo systemctl start google-monitor
```

### Using Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 15 minutes
4. Action: Start a program
   - Program: `python`
   - Arguments: `check_availability.py --once`
   - Start in: `C:\path\to\global-google-service-availability`

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "check_availability.py"]
```

Build and run:

```bash
docker build -t google-monitor .
docker run -d --name google-monitor google-monitor
```

## 📊 Output & Logging

### Console Output
- ✓ Green checkmarks for successful checks
- ✗ Red X marks for failures
- Response times in milliseconds
- Summary report after each cycle

### Log Files

**availability_log.txt** - Detailed execution log
```
2024-10-30 01:00:00 - INFO - Starting availability check...
2024-10-30 01:00:15 - INFO - Check completed.
```

**latest_results.json** - Most recent check results
```json
{
  "last_check": "2024-10-30T01:00:15",
  "results": [
    {
      "service": "Google Search",
      "url": "https://www.google.com",
      "status": "UP",
      "status_code": 200,
      "response_time_ms": 145.23,
      "timestamp": "2024-10-30T01:00:05"
    }
  ]
}
```

## 🌐 Monitored Services

Currently monitoring **12 critical Google services**:

| Service | Endpoints | Category |
|---------|-----------|----------|
| **Google Search** | google.com | Core |
| **Gmail** | mail.google.com | Communication |
| **Google Drive** | drive.google.com | Storage |
| **Google Maps** | maps.google.com | Navigation |
| **YouTube** | youtube.com | Media |
| **Google Cloud Platform** | cloud.google.com | Infrastructure |
| **Google AI Studio** | aistudio.google.com | AI/ML |
| **Vertex AI** | cloud.google.com/vertex-ai | AI/ML |
| **Google Colab** | colab.research.google.com | AI/ML |
| **Google Translate** | translate.google.com | AI/ML |
| **Firebase** | firebase.google.com | Development |
| **Google Analytics** | analytics.google.com | Analytics |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Adding New Services

To add monitoring for additional services:
1. Edit `config.json`
2. Add service to the `services` section
3. Test with `python check_availability.py --once`
4. Submit PR with your additions

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Mortyo666

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📞 Support

If you encounter any issues or have questions:
- Open an [Issue](https://github.com/Mortyo666/global-google-service-availability/issues)
- Check existing issues for solutions

## 🎯 Roadmap

- [ ] Web dashboard for visualization
- [ ] Email/Slack notifications on outages
- [ ] Historical data storage (SQLite)
- [ ] Prometheus metrics export
- [ ] Docker Compose setup
- [ ] API endpoint for programmatic access

---

**Made with ❤️ for hosting operators and startups worldwide**

⭐ If this tool helps you, please star the repository!
