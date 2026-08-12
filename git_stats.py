import subprocess

def run_git(command):
    try:
        result = subprocess.run(["git"] + command, capture_output = True, text = True, check = True)

        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
def is_git_repo():
    result = run_git(["rev-parse", "--is-inside-work-tree"])
    return result == "true"

def current_branch():
    return run_git(["branch", "--show-current"])

def current_commit():
    return run_git(["rev-parse", "HEAD"])

def commit_count():
    result = run_git(["rev-list", "--count", "HEAD"])
    if result is None:
        return 0
    return int(result)

def changed_lines():
    result = run_git(["diff", "--numstat"])

    if not result:
        return 0, 0

    added = 0
    removed = 0

    for line in result.splitlines():
        parts = line.split()

        if len(parts) < 2:
            continue
        try:
            added += int(parts[0])
            removed += int(parts[1])
        except ValueError:
            pass
    return added, removed

def changed_files():
    result = run_git(["status", "--short"])

    if not result:
        return 0
    return len(result.splitlines())
