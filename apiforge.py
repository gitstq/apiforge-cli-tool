#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APIForge-CLI 🚀
轻量级终端HTTP API测试与智能文档生成引擎
Lightweight Terminal HTTP API Testing & Intelligent Documentation Generator

Zero Dependencies - Single File - Python 3.7+
"""

__version__ = "1.0.0"
__author__ = "APIForge Team"
__license__ = "MIT"

import sys
import os
import json
import time
import re
import urllib.request
import urllib.error
import urllib.parse
import ssl
import base64
from datetime import datetime
from pathlib import Path

# Try to import optional modules for enhanced features
try:
    import readline
    HAS_READLINE = True
except ImportError:
    HAS_READLINE = False

try:
    import curses
    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False

# ANSI Color Codes
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'dim': '\033[2m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bg_black': '\033[40m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m',
    'bg_magenta': '\033[45m',
    'bg_cyan': '\033[46m',
    'bg_white': '\033[47m',
}

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
CONTENT_TYPES = {
    'json': 'application/json',
    'form': 'application/x-www-form-urlencoded',
    'text': 'text/plain',
    'html': 'text/html',
    'xml': 'application/xml',
}

class Colors:
    """Color helper class"""
    @staticmethod
    def color(text, color_name):
        if color_name in COLORS:
            return f"{COLORS[color_name]}{text}{COLORS['reset']}"
        return text
    
    @staticmethod
    def bold(text): return Colors.color(text, 'bold')
    @staticmethod
    def dim(text): return Colors.color(text, 'dim')
    @staticmethod
    def red(text): return Colors.color(text, 'red')
    @staticmethod
    def green(text): return Colors.color(text, 'green')
    @staticmethod
    def yellow(text): return Colors.color(text, 'yellow')
    @staticmethod
    def blue(text): return Colors.color(text, 'blue')
    @staticmethod
    def magenta(text): return Colors.color(text, 'magenta')
    @staticmethod
    def cyan(text): return Colors.color(text, 'cyan')

class Config:
    """Configuration management"""
    CONFIG_DIR = Path.home() / '.apiforge'
    HISTORY_FILE = CONFIG_DIR / 'history.json'
    ENV_FILE = CONFIG_DIR / 'environments.json'
    COLLECTIONS_DIR = CONFIG_DIR / 'collections'
    
    @classmethod
    def init(cls):
        """Initialize configuration directory"""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        cls.COLLECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def save_history(cls, history):
        """Save request history"""
        try:
            with open(cls.HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(Colors.red(f"Error saving history: {e}"))
    
    @classmethod
    def load_history(cls):
        """Load request history"""
        if cls.HISTORY_FILE.exists():
            try:
                with open(cls.HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return []
    
    @classmethod
    def save_environments(cls, envs):
        """Save environments"""
        try:
            with open(cls.ENV_FILE, 'w', encoding='utf-8') as f:
                json.dump(envs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(Colors.red(f"Error saving environments: {e}"))
    
    @classmethod
    def load_environments(cls):
        """Load environments"""
        if cls.ENV_FILE.exists():
            try:
                with open(cls.ENV_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {'default': {}}

class HTTPClient:
    """HTTP Client for making requests"""
    
    @staticmethod
    def make_request(method, url, headers=None, data=None, timeout=30, verify_ssl=True):
        """Make HTTP request"""
        headers = headers or {}
        
        # Create request
        req = urllib.request.Request(url, method=method)
        
        # Add headers
        for key, value in headers.items():
            req.add_header(key, value)
        
        # Add default User-Agent if not present
        if 'User-Agent' not in headers:
            req.add_header('User-Agent', f'APIForge-CLI/{__version__}')
        
        # Prepare data
        if data and isinstance(data, dict):
            if headers.get('Content-Type') == 'application/json':
                data = json.dumps(data).encode('utf-8')
            else:
                data = urllib.parse.urlencode(data).encode('utf-8')
        elif data and isinstance(data, str):
            data = data.encode('utf-8')
        
        # SSL context
        ssl_context = None
        if not verify_ssl:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
        
        start_time = time.time()
        
        try:
            response = urllib.request.urlopen(
                req, 
                data=data, 
                timeout=timeout,
                context=ssl_context
            )
            
            elapsed = (time.time() - start_time) * 1000  # ms
            
            # Read response
            body = response.read()
            
            # Try to decode as UTF-8
            try:
                body_text = body.decode('utf-8')
            except UnicodeDecodeError:
                body_text = body.decode('utf-8', errors='replace')
            
            return {
                'status': response.getcode(),
                'headers': dict(response.headers),
                'body': body_text,
                'size': len(body),
                'time': elapsed,
                'url': response.geturl()
            }
            
        except urllib.error.HTTPError as e:
            elapsed = (time.time() - start_time) * 1000
            
            body = e.read()
            try:
                body_text = body.decode('utf-8')
            except UnicodeDecodeError:
                body_text = body.decode('utf-8', errors='replace')
            
            return {
                'status': e.code,
                'headers': dict(e.headers),
                'body': body_text,
                'size': len(body),
                'time': elapsed,
                'url': url,
                'error': True
            }
        
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return {
                'status': 0,
                'headers': {},
                'body': str(e),
                'size': 0,
                'time': elapsed,
                'url': url,
                'error': True,
                'exception': True
            }

class ResponseFormatter:
    """Format HTTP responses"""
    
    @staticmethod
    def format_json(text):
        """Format and colorize JSON"""
        try:
            data = json.loads(text)
            formatted = json.dumps(data, indent=2, ensure_ascii=False)
            return ResponseFormatter.colorize_json(formatted)
        except json.JSONDecodeError:
            return text
    
    @staticmethod
    def colorize_json(text):
        """Add colors to JSON output"""
        lines = []
        for line in text.split('\n'):
            # Color keys
            line = re.sub(r'"([^"]+)":', Colors.cyan(r'"\1":'), line)
            # Color strings
            line = re.sub(r':\s*"([^"]*)"', ': ' + Colors.green(r'"\1"'), line)
            # Color numbers
            line = re.sub(r':\s*(\d+\.?\d*)', ': ' + Colors.yellow(r'\1'), line)
            # Color booleans/null
            line = re.sub(r':\s*(true|false|null)', ': ' + Colors.magenta(r'\1'), line)
            lines.append(line)
        return '\n'.join(lines)
    
    @staticmethod
    def format_headers(headers):
        """Format HTTP headers"""
        lines = []
        for key, value in headers.items():
            lines.append(f"{Colors.cyan(key)}: {value}")
        return '\n'.join(lines)
    
    @staticmethod
    def format_status(status):
        """Format status code with color"""
        if 200 <= status < 300:
            return Colors.green(f"{status}")
        elif 300 <= status < 400:
            return Colors.yellow(f"{status}")
        elif 400 <= status < 500:
            return Colors.magenta(f"{status}")
        else:
            return Colors.red(f"{status}")

class DocumentationGenerator:
    """Generate API documentation"""
    
    @staticmethod
    def generate_markdown(history, title="API Documentation"):
        """Generate Markdown documentation from history"""
        lines = [
            f"# {title}",
            "",
            f"Generated by APIForge-CLI v{__version__}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Table of Contents",
            "",
        ]
        
        # TOC
        for i, req in enumerate(history, 1):
            method = req.get('method', 'GET')
            url = req.get('url', '')
            name = req.get('name', f"Request {i}")
            lines.append(f"- [{i}. {method} {name}](#request-{i})")
        
        lines.append("")
        
        # Requests
        for i, req in enumerate(history, 1):
            method = req.get('method', 'GET')
            url = req.get('url', '')
            name = req.get('name', f"Request {i}")
            headers = req.get('headers', {})
            body = req.get('body', '')
            
            lines.extend([
                f"## Request {i}: {method} {name}",
                "",
                f"**Method:** `{method}`",
                "",
                f"**URL:** `{url}`",
                "",
            ])
            
            if headers:
                lines.extend([
                    "**Headers:**",
                    "",
                    "```http",
                ])
                for key, value in headers.items():
                    lines.append(f"{key}: {value}")
                lines.extend([
                    "```",
                    "",
                ])
            
            if body:
                lines.extend([
                    "**Body:**",
                    "",
                    "```json",
                    body if isinstance(body, str) else json.dumps(body, indent=2),
                    "```",
                    "",
                ])
            
            lines.append("---")
            lines.append("")
        
        return '\n'.join(lines)
    
    @staticmethod
    def generate_openapi(history, title="API", version="1.0.0"):
        """Generate OpenAPI 3.0 spec from history"""
        paths = {}
        
        for req in history:
            method = req.get('method', 'GET').lower()
            url = req.get('url', '')
            headers = req.get('headers', {})
            body = req.get('body', '')
            
            # Parse URL to get path
            parsed = urllib.parse.urlparse(url)
            path = parsed.path or '/'
            
            if path not in paths:
                paths[path] = {}
            
            operation = {
                'summary': req.get('name', f'{method.upper()} {path}'),
                'responses': {
                    '200': {
                        'description': 'Successful response'
                    }
                }
            }
            
            # Add request body if present
            if body and method in ['post', 'put', 'patch']:
                try:
                    json_body = json.loads(body) if isinstance(body, str) else body
                    operation['requestBody'] = {
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object'
                                },
                                'example': json_body
                            }
                        }
                    }
                except (json.JSONDecodeError, TypeError):
                    pass
            
            paths[path][method] = operation
        
        spec = {
            'openapi': '3.0.0',
            'info': {
                'title': title,
                'version': version,
                'description': f'Generated by APIForge-CLI v{__version__}'
            },
            'paths': paths
        }
        
        return json.dumps(spec, indent=2, ensure_ascii=False)

class CollectionManager:
    """Manage request collections"""
    
    @staticmethod
    def export_collection(history, name, description=""):
        """Export collection to APIForge format"""
        collection = {
            'info': {
                'name': name,
                'description': description,
                'version': '1.0.0',
                'schema': 'https://schema.getapiforge.io/collection.json'
            },
            'item': []
        }
        
        for req in history:
            item = {
                'name': req.get('name', f"{req.get('method', 'GET')} Request"),
                'request': {
                    'method': req.get('method', 'GET'),
                    'url': req.get('url', ''),
                    'header': [
                        {'key': k, 'value': v}
                        for k, v in req.get('headers', {}).items()
                    ]
                }
            }
            
            body = req.get('body')
            if body:
                item['request']['body'] = {
                    'mode': 'raw',
                    'raw': body if isinstance(body, str) else json.dumps(body)
                }
            
            collection['item'].append(item)
        
        return collection
    
    @staticmethod
    def import_postman_collection(data):
        """Import Postman collection"""
        history = []
        
        items = data.get('item', [])
        for item in items:
            req = item.get('request', {})
            
            # Handle URL (can be string or object)
            url = req.get('url', '')
            if isinstance(url, dict):
                url = url.get('raw', '')
            
            # Handle headers
            headers = {}
            for header in req.get('header', []):
                headers[header.get('key', '')] = header.get('value', '')
            
            # Handle body
            body = ''
            body_data = req.get('body', {})
            if body_data:
                body = body_data.get('raw', '')
            
            history.append({
                'name': item.get('name', ''),
                'method': req.get('method', 'GET'),
                'url': url,
                'headers': headers,
                'body': body,
                'timestamp': datetime.now().isoformat()
            })
        
        return history

class TUI:
    """Terminal User Interface"""
    
    def __init__(self):
        self.history = Config.load_history()
        self.environments = Config.load_environments()
        self.current_env = 'default'
        self.running = True
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Print application banner"""
        banner = f"""
{Colors.cyan('╔══════════════════════════════════════════════════════════════╗')}
{Colors.cyan('║')}  {Colors.bold('🚀 APIForge-CLI')} - Terminal HTTP API Testing Engine          {Colors.cyan('║')}
{Colors.cyan('║')}  {Colors.dim(f'Version {__version__} | Zero Dependencies | Python 3.7+')}      {Colors.cyan('║')}
{Colors.cyan('╚══════════════════════════════════════════════════════════════╝')}
"""
        print(banner)
    
    def print_menu(self):
        """Print main menu"""
        menu = f"""
{Colors.bold('📋 Main Menu:')}

  {Colors.green('1.')} Send Request        - Make HTTP request
  {Colors.green('2.')} View History        - Browse request history
  {Colors.green('3.')} Manage Collections  - Import/Export collections
  {Colors.green('4.')} Environments        - Manage environment variables
  {Colors.green('5.')} Generate Docs       - Create API documentation
  {Colors.green('6.')} Settings            - Configure options
  
  {Colors.red('0.')} Exit
"""
        print(menu)
    
    def get_input(self, prompt, default=None):
        """Get user input with optional default"""
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        
        value = input(Colors.yellow(prompt)).strip()
        return value if value else default
    
    def send_request_flow(self):
        """Interactive request flow"""
        print(f"\n{Colors.bold('🌐 Send HTTP Request')}")
        print("=" * 50)
        
        # Method
        print(f"\n{Colors.dim('Available methods:')} {', '.join(HTTP_METHODS)}")
        method = self.get_input("Method", "GET").upper()
        if method not in HTTP_METHODS:
            print(Colors.red(f"Invalid method. Using GET."))
            method = "GET"
        
        # URL
        url = self.get_input("URL")
        if not url:
            print(Colors.red("URL is required!"))
            return
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Headers
        headers = {}
        print(f"\n{Colors.dim('Add headers (empty line to finish):')}")
        while True:
            header_line = self.get_input("Header (Name: Value)")
            if not header_line:
                break
            if ':' in header_line:
                key, value = header_line.split(':', 1)
                headers[key.strip()] = value.strip()
        
        # Body
        body = None
        if method in ['POST', 'PUT', 'PATCH']:
            print(f"\n{Colors.dim('Request body (JSON, empty to skip):')}")
            body_lines = []
            while True:
                line = input()
                if not line and body_lines:
                    break
                if not line and not body_lines:
                    break
                body_lines.append(line)
            
            if body_lines:
                body = '\n'.join(body_lines)
                headers['Content-Type'] = 'application/json'
        
        # Name for history
        name = self.get_input("Request name (for history)", f"{method} {url[:30]}...")
        
        # Make request
        print(f"\n{Colors.blue('⏳ Sending request...')}")
        response = HTTPClient.make_request(method, url, headers, body)
        
        # Display response
        self.display_response(response)
        
        # Save to history
        request_data = {
            'name': name,
            'method': method,
            'url': url,
            'headers': headers,
            'body': body,
            'timestamp': datetime.now().isoformat(),
            'response': {
                'status': response['status'],
                'size': response['size'],
                'time': response['time']
            }
        }
        self.history.append(request_data)
        Config.save_history(self.history)
        
        print(Colors.green(f"\n✅ Request saved to history"))
    
    def display_response(self, response):
        """Display HTTP response"""
        print(f"\n{Colors.bold('📨 Response:')}")
        print("=" * 50)
        
        # Status
        status = ResponseFormatter.format_status(response['status'])
        print(f"\n{Colors.bold('Status:')} {status}")
        print(f"{Colors.bold('Time:')} {response['time']:.2f}ms")
        print(f"{Colors.bold('Size:')} {response['size']} bytes")
        
        # Headers
        if response['headers']:
            print(f"\n{Colors.bold('Headers:')}")
            print(ResponseFormatter.format_headers(response['headers']))
        
        # Body
        if response['body']:
            print(f"\n{Colors.bold('Body:')}")
            body = response['body']
            
            # Try to format as JSON
            content_type = response['headers'].get('Content-Type', '')
            if 'json' in content_type or body.strip().startswith(('{', '[')):
                formatted = ResponseFormatter.format_json(body)
                print(formatted)
            else:
                # Truncate if too long
                if len(body) > 5000:
                    print(body[:5000])
                    print(Colors.dim(f"\n... ({len(body) - 5000} more bytes)"))
                else:
                    print(body)
    
    def view_history(self):
        """View and manage request history"""
        if not self.history:
            print(Colors.yellow("\n📭 No requests in history"))
            return
        
        print(f"\n{Colors.bold('📚 Request History')}")
        print("=" * 50)
        
        for i, req in enumerate(self.history[-20:], 1):  # Show last 20
            method = req.get('method', 'GET')
            url = req.get('url', '')[:40]
            name = req.get('name', 'Unnamed')
            time_str = req.get('timestamp', '')[:10]
            
            method_color = Colors.green(method) if method == 'GET' else (
                Colors.yellow(method) if method in ['POST', 'PUT'] else Colors.red(method)
            )
            
            print(f"  {Colors.cyan(f'{i:2d}.')} [{method_color}] {Colors.bold(name)}")
            print(f"      {Colors.dim(url)} {Colors.dim(time_str)}")
        
        print(f"\n{Colors.dim('Total: ' + str(len(self.history)) + ' requests')}")
        
        # Options
        print(f"\n{Colors.dim('Options: (r)eplay, (d)elete, (c)lear all, (Enter) back')}")
        choice = input(Colors.yellow("Choice: ")).strip().lower()
        
        if choice == 'c':
            confirm = input(Colors.red("Clear all history? (yes/no): ")).strip()
            if confirm == 'yes':
                self.history = []
                Config.save_history(self.history)
                print(Colors.green("History cleared"))
    
    def manage_collections(self):
        """Manage request collections"""
        print(f"\n{Colors.bold('📦 Collections')}")
        print("=" * 50)
        
        print(f"""
  {Colors.green('1.')} Export current history to collection
  {Colors.green('2.')} Import Postman collection
  {Colors.green('3.')} List saved collections
  
  {Colors.red('0.')} Back
""")
        
        choice = self.get_input("Choice")
        
        if choice == '1':
            if not self.history:
                print(Colors.yellow("No history to export"))
                return
            
            name = self.get_input("Collection name", "My Collection")
            desc = self.get_input("Description", "")
            
            collection = CollectionManager.export_collection(self.history, name, desc)
            
            filename = name.lower().replace(' ', '_') + '.apiforge.json'
            filepath = Config.COLLECTIONS_DIR / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(collection, f, indent=2, ensure_ascii=False)
            
            print(Colors.green(f"Collection saved: {filepath}"))
        
        elif choice == '2':
            path = self.get_input("Postman collection file path")
            if not os.path.exists(path):
                print(Colors.red("File not found!"))
                return
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                imported = CollectionManager.import_postman_collection(data)
                self.history.extend(imported)
                Config.save_history(self.history)
                
                print(Colors.green(f"Imported {len(imported)} requests"))
            except Exception as e:
                print(Colors.red(f"Import failed: {e}"))
    
    def generate_docs(self):
        """Generate API documentation"""
        if not self.history:
            print(Colors.yellow("\n📭 No requests to document"))
            return
        
        print(f"\n{Colors.bold('📝 Generate Documentation')}")
        print("=" * 50)
        
        print(f"""
  {Colors.green('1.')} Markdown documentation
  {Colors.green('2.')} OpenAPI 3.0 specification
  
  {Colors.red('0.')} Back
""")
        
        choice = self.get_input("Format")
        
        if choice == '1':
            title = self.get_input("Document title", "API Documentation")
            content = DocumentationGenerator.generate_markdown(self.history, title)
            
            filename = title.lower().replace(' ', '_') + '.md'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(Colors.green(f"Documentation saved: {filename}"))
        
        elif choice == '2':
            title = self.get_input("API title", "My API")
            version = self.get_input("API version", "1.0.0")
            content = DocumentationGenerator.generate_openapi(self.history, title, version)
            
            filename = title.lower().replace(' ', '_') + '.openapi.json'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(Colors.green(f"OpenAPI spec saved: {filename}"))
    
    def run(self):
        """Run TUI main loop"""
        while self.running:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = self.get_input("Choice")
            
            if choice == '1':
                self.send_request_flow()
            elif choice == '2':
                self.view_history()
            elif choice == '3':
                self.manage_collections()
            elif choice == '4':
                print(Colors.yellow("\nEnvironments feature coming soon!"))
            elif choice == '5':
                self.generate_docs()
            elif choice == '6':
                print(Colors.yellow("\nSettings feature coming soon!"))
            elif choice == '0':
                self.running = False
                print(Colors.green("\n👋 Goodbye!"))
            else:
                print(Colors.red("\nInvalid choice!"))
            
            if self.running:
                input(Colors.dim("\nPress Enter to continue..."))

class CLI:
    """Command Line Interface"""
    
    @staticmethod
    def print_help():
        """Print help message"""
        help_text = f"""
{Colors.bold('APIForge-CLI')} v{__version__} - HTTP API Testing & Documentation Tool

{Colors.bold('USAGE:')}
  apiforge [COMMAND] [OPTIONS]

{Colors.bold('COMMANDS:')}
  {Colors.green('request')}    Send HTTP request
  {Colors.green('history')}    View request history
  {Colors.green('docs')}       Generate API documentation
  {Colors.green('import')}     Import collection
  {Colors.green('export')}     Export collection
  {Colors.green('tui')}        Launch interactive TUI mode
  {Colors.green('version')}    Show version
  {Colors.green('help')}       Show this help

{Colors.bold('OPTIONS:')}
  -X, --method     HTTP method (GET, POST, PUT, DELETE, etc.)
  -H, --header     Request header (can be used multiple times)
  -d, --data       Request body data
  -o, --output     Output file
  -f, --format     Output format (json, markdown, openapi)

{Colors.bold('EXAMPLES:')}
  # Send GET request
  apiforge request https://api.example.com/users

  # Send POST request with JSON data
  apiforge request -X POST -H "Content-Type: application/json" \\
    -d '{{"name":"John"}}' https://api.example.com/users

  # Generate Markdown documentation
  apiforge docs -f markdown -o api.md

  # Launch TUI mode
  apiforge tui

{Colors.dim('For more information: https://github.com/gitstq/apiforge-cli')}
"""
        print(help_text)
    
    @staticmethod
    def parse_args(args):
        """Parse command line arguments"""
        parsed = {
            'command': None,
            'url': None,
            'method': 'GET',
            'headers': {},
            'data': None,
            'output': None,
            'format': 'json'
        }
        
        if not args:
            return parsed
        
        parsed['command'] = args[0]
        
        i = 1
        while i < len(args):
            arg = args[i]
            
            if arg in ['-X', '--method']:
                i += 1
                if i < len(args):
                    parsed['method'] = args[i].upper()
            
            elif arg in ['-H', '--header']:
                i += 1
                if i < len(args):
                    header = args[i]
                    if ':' in header:
                        key, value = header.split(':', 1)
                        parsed['headers'][key.strip()] = value.strip()
            
            elif arg in ['-d', '--data']:
                i += 1
                if i < len(args):
                    parsed['data'] = args[i]
            
            elif arg in ['-o', '--output']:
                i += 1
                if i < len(args):
                    parsed['output'] = args[i]
            
            elif arg in ['-f', '--format']:
                i += 1
                if i < len(args):
                    parsed['format'] = args[i]
            
            elif not arg.startswith('-') and not parsed['url']:
                parsed['url'] = arg
            
            i += 1
        
        return parsed
    
    @staticmethod
    def handle_request(args):
        """Handle request command"""
        parsed = CLI.parse_args(['request'] + args)
        
        url = parsed['url']
        if not url:
            print(Colors.red("Error: URL is required"))
            return 1
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"{Colors.blue('⏳ Sending')} {parsed['method']} {url}")
        
        response = HTTPClient.make_request(
            parsed['method'],
            url,
            parsed['headers'],
            parsed['data']
        )
        
        # Display response
        TUI().display_response(response)
        
        # Save to history
        history = Config.load_history()
        history.append({
            'name': f"{parsed['method']} {url[:40]}",
            'method': parsed['method'],
            'url': url,
            'headers': parsed['headers'],
            'body': parsed['data'],
            'timestamp': datetime.now().isoformat(),
            'response': {
                'status': response['status'],
                'size': response['size'],
                'time': response['time']
            }
        })
        Config.save_history(history)
        
        # Save to file if output specified
        if parsed['output']:
            output_data = {
                'request': {
                    'method': parsed['method'],
                    'url': url,
                    'headers': parsed['headers'],
                    'body': parsed['data']
                },
                'response': response
            }
            with open(parsed['output'], 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(Colors.green(f"\nSaved to: {parsed['output']}"))
        
        return 0 if response['status'] < 400 else 1
    
    @staticmethod
    def handle_history(args):
        """Handle history command"""
        history = Config.load_history()
        
        if not history:
            print(Colors.yellow("No request history"))
            return 0
        
        print(f"\n{Colors.bold('Request History:')}")
        print("-" * 60)
        
        for i, req in enumerate(history[-20:], 1):
            method = req.get('method', 'GET')
            url = req.get('url', '')[:50]
            status = req.get('response', {}).get('status', 0)
            
            status_str = ResponseFormatter.format_status(status)
            
            print(f"{i:2d}. [{status_str}] {method:6} {url}")
        
        return 0
    
    @staticmethod
    def handle_docs(args):
        """Handle docs command"""
        parsed = CLI.parse_args(['docs'] + args)
        
        history = Config.load_history()
        if not history:
            print(Colors.yellow("No requests to document"))
            return 1
        
        fmt = parsed['format']
        output = parsed['output']
        
        if fmt == 'markdown':
            content = DocumentationGenerator.generate_markdown(history)
            ext = '.md'
        elif fmt in ['openapi', 'json']:
            content = DocumentationGenerator.generate_openapi(history)
            ext = '.json'
        else:
            print(Colors.red(f"Unknown format: {fmt}"))
            return 1
        
        if output:
            filename = output
        else:
            filename = f'api_documentation{ext}'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(Colors.green(f"Documentation saved: {filename}"))
        return 0
    
    @staticmethod
    def run(args):
        """Run CLI"""
        Config.init()
        
        if not args or args[0] in ['help', '--help', '-h']:
            CLI.print_help()
            return 0
        
        command = args[0]
        
        if command == 'version' or command == '--version':
            print(f"APIForge-CLI v{__version__}")
            return 0
        
        elif command == 'tui':
            TUI().run()
            return 0
        
        elif command == 'request':
            return CLI.handle_request(args[1:])
        
        elif command == 'history':
            return CLI.handle_history(args[1:])
        
        elif command == 'docs':
            return CLI.handle_docs(args[1:])
        
        elif command == 'import':
            print(Colors.yellow("Import command - use TUI mode for interactive import"))
            return 0
        
        elif command == 'export':
            print(Colors.yellow("Export command - use TUI mode for interactive export"))
            return 0
        
        else:
            # Try to interpret as URL for quick request
            if command.startswith(('http://', 'https://')) or '.' in command:
                return CLI.handle_request(args)
            else:
                print(Colors.red(f"Unknown command: {command}"))
                CLI.print_help()
                return 1

def main():
    """Main entry point"""
    try:
        args = sys.argv[1:]
        exit_code = CLI.run(args)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(Colors.yellow("\n\n⚠️  Interrupted by user"))
        sys.exit(130)
    except Exception as e:
        print(Colors.red(f"\n❌ Error: {e}"))
        sys.exit(1)

if __name__ == '__main__':
    main()
