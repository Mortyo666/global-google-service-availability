#!/usr/bin/env python3
"""
Google Services Availability Checker
Monitors Google services and AI/ML endpoints for hosting operators and startups
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, List
import schedule
from retrying import retry
from colorama import init, Fore, Style

init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('availability_log.txt'),
        logging.StreamHandler()
    ]
)

class GoogleServiceMonitor:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.services = self.config['services']
        self.check_interval = self.config.get('check_interval_minutes', 15)
        self.timeout = self.config.get('timeout_seconds', 10)
        self.retry_attempts = self.config.get('retry_attempts', 3)
        
        # Ban protection settings
        self.request_delay = self.config.get('request_delay_seconds', 2)
        self.user_agents = self.config['user_agents']
        self.current_ua_index = 0
    
    def get_headers(self) -> Dict:
        """Rotate user agents to avoid detection"""
        self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        return {
            'User-Agent': self.user_agents[self.current_ua_index],
            'Accept': 'text/html,application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        }
    
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def check_endpoint(self, service_name: str, url: str) -> Dict:
        """Check if a single endpoint is available"""
        try:
            start_time = time.time()
            response = requests.get(
                url,
                headers=self.get_headers(),
                timeout=self.timeout,
                allow_redirects=True
            )
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            status = 'UP' if response.status_code in [200, 301, 302] else 'DOWN'
            
            return {
                'service': service_name,
                'url': url,
                'status': status,
                'status_code': response.status_code,
                'response_time_ms': round(response_time, 2),
                'timestamp': datetime.now().isoformat()
            }
        except requests.exceptions.Timeout:
            return {
                'service': service_name,
                'url': url,
                'status': 'TIMEOUT',
                'status_code': None,
                'response_time_ms': None,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logging.error(f"Error checking {service_name}: {str(e)}")
            return {
                'service': service_name,
                'url': url,
                'status': 'ERROR',
                'status_code': None,
                'response_time_ms': None,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_all_services(self) -> List[Dict]:
        """Check all configured services"""
        results = []
        
        for service_name, service_data in self.services.items():
            logging.info(f"Checking {service_name}...")
            
            for endpoint in service_data['endpoints']:
                result = self.check_endpoint(service_name, endpoint)
                results.append(result)
                
                # Display result with colors
                if result['status'] == 'UP':
                    print(f"{Fore.GREEN}✓ {service_name} - {endpoint} - {result['response_time_ms']}ms")
                else:
                    print(f"{Fore.RED}✗ {service_name} - {endpoint} - {result['status']}")
                
                # Anti-ban delay
                time.sleep(self.request_delay)
        
        return results
    
    def save_results(self, results: List[Dict], filename='latest_results.json'):
        """Save check results to file"""
        with open(filename, 'w') as f:
            json.dump({
                'last_check': datetime.now().isoformat(),
                'results': results
            }, f, indent=2)
    
    def generate_report(self, results: List[Dict]):
        """Generate availability report"""
        total = len(results)
        up = sum(1 for r in results if r['status'] == 'UP')
        down = total - up
        uptime_percentage = (up / total * 100) if total > 0 else 0
        
        print(f"\n{Style.BRIGHT}=== Availability Report ===")
        print(f"Total Services Checked: {total}")
        print(f"{Fore.GREEN}UP: {up} ({uptime_percentage:.1f}%)")
        print(f"{Fore.RED}DOWN: {down}")
        print(f"Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 40)
    
    def run_once(self):
        """Run a single check cycle"""
        logging.info("Starting availability check...")
        results = self.check_all_services()
        self.save_results(results)
        self.generate_report(results)
        logging.info("Check completed.")
    
    def run_scheduled(self):
        """Run checks on schedule"""
        logging.info(f"Starting scheduled monitoring (every {self.check_interval} minutes)")
        
        # Run immediately
        self.run_once()
        
        # Schedule periodic checks
        schedule.every(self.check_interval).minutes.do(self.run_once)
        
        while True:
            schedule.run_pending()
            time.sleep(30)

if __name__ == "__main__":
    import sys
    
    print(f"{Style.BRIGHT}Google Services Availability Monitor")
    print("===" * 15)
    
    monitor = GoogleServiceMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        monitor.run_once()
    else:
        monitor.run_scheduled()
