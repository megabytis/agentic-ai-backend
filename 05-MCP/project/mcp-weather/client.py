"""
MCP Client - Connects to weather server
"""

import json
import subprocess
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self, server_script):
        # Start the server as a subprocess
        self.server_process = subprocess.Popen(
            [sys.executable, server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.req_id = 0
        self.tools = []
    
    def _send_request(self, method, params=None):
        """Send JSON-RPC request to server"""
        self.req_id += 1
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self.req_id
        }
        if params:
            request["params"] = params
        
        # Send
        self.server_process.stdin.write(json.dumps(request) + "\n")
        self.server_process.stdin.flush()
        
        # Receive
        response_line = self.server_process.stdout.readline()
        return json.loads(response_line)
    
    def list_tools(self):
        """Get all tools from server"""
        response = self._send_request("list_tools")
        if "result" in response:
            self.tools = response["result"]["tools"]
            return self.tools
        return []
    
    def call_tool(self, tool_name, arguments):
        """Execute a tool on the server"""
        response = self._send_request("call_tool", {
            "name": tool_name,
            "arguments": arguments
        })
        if "result" in response:
            return response["result"]["content"]
        return f"Error: {response.get('error', 'Unknown error')}"
    
    def close(self):
        """Clean up"""
        self.server_process.terminate()


def main():
    print("Starting MCP Weather Bot...")
    
    # Initialize MCP client
    client = MCPClient("weather_server.py")
    
    # Get tools from server
    tools = client.list_tools()
    print(f"✅ Connected to server. Found {len(tools)} tool(s):")
    for tool in tools:
        print(f"   - {tool['function']['name']}")
    
    # Initialize LLM client
    llm = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    model = "stepfun/step-3.5-flash:free"
    
    messages = [
        {
            "role": "system",
            "content": "You are a weather assistant. Use the get_weather tool when asked about weather."
        }
    ]
    
    print("\n🌤️ Weather Bot Ready! Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        
        messages.append({"role": "user", "content": user_input})
        
        # Get LLM response
        response = llm.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        messages.append(message)
        
        # Handle tool calls
        if message.tool_calls:
            print("\n🔧 Executing tool...")
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"   Tool: {tool_name}")
                print(f"   Args: {args}")
                
                # Call tool via MCP client
                result = client.call_tool(tool_name, args)
                print(f"   Result: {result}")
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final response
            final = llm.chat.completions.create(
                model=model,
                messages=messages
            )
            final_message = final.choices[0].message
            messages.append(final_message)
            print(f"\nBot: {final_message.content}")
        else:
            print(f"\nBot: {message.content}")
    
    client.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()