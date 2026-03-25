"""
Simple Weather MCP Server
Communicates via JSON messages over STDIO
"""

import json
import sys
import requests

class WeatherServer:
    def __init__(self):
        # Define tools this server provides
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "City name"}
                        },
                        "required": ["city"]
                    }
                }
            }
        ]
    
    def get_weather(self, city: str):
        """Get weather from free API"""
        try:
            # wttr.in returns simple text weather
            url = f"https://wttr.in/{city}?format=%C+%t"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                weather = response.text.strip()
                return f"Weather in {city}: {weather}"
            else:
                return f"Could not get weather for {city}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def handle_request(self, request):
        """Process incoming requests"""
        method = request.get("method")
        req_id = request.get("id")
        
        if method == "list_tools":
            return {
                "jsonrpc": "2.0",
                "result": {"tools": self.tools},
                "id": req_id
            }
        
        elif method == "call_tool":
            params = request.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})
            
            if tool_name == "get_weather":
                result = self.get_weather(args.get("city"))
            else:
                result = f"Unknown tool: {tool_name}"
            
            return {
                "jsonrpc": "2.0",
                "result": {"content": result},
                "id": req_id
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": "Method not found"},
                "id": req_id
            }
    
    def run(self):
        """Main loop - read from stdin, write to stdout"""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line.strip())
                response = self.handle_request(request)
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32603, "message": str(e)},
                    "id": None
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

if __name__ == "__main__":
    server = WeatherServer()
    server.run()