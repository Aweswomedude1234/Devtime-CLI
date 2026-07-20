import subprocess
import time
import json

result = subprocess.run(["ps", "aux"], capture_output = True, text = True)
output = result.stdout
claudeOn = False
for process in output.splitlines():
    if "claude" in process.lower():
        print(process)
        claudeOn = True

claude = subprocess.Popen(["claude", "--output-format", "stream-json", "--input-format", "stream-json"], stdout=subprocess.PIPE, text = True)
if claudeOn:
    print("Claude Code Running")
    for line in claude.stdout:
        event = json.loads(line)
        print(event)
    
else: 
    print("Claude Code not running")

