import subprocess
import time

result = subprocess.run(["ps", "aux"], capture_output = True, text = True)
output = result.stdout
for process in output.splitlines():
    if "claude" in process.lower():
        print("Claude code running")
        print(process)
else:
    print("Claude Code not running")