from config import load_config, save_config, save_session, load_history
from notifier import remind
from timer import wait, wait_for_return
from planner import create_plan
from session import Session
import threading
import git_stats


session = Session()
stop_event = threading.Event()
session_thread = None

def show_help():
    print()
    print("DevTime Commands")
    print("=" * 30)
    print("/start  - Start New session")
    print("/end    - End Current Session")
    print("/extend - Extend Current Session")
    print("/plan   - View Current Plan")
    print("/time   - View Session Time")
    print("/stats  - View Session Statistics")
    print("/config - Change Settings")
    print("/help   - Show Commands")
    print("/quit   - Exit DevTime")
    print()
def choose_strategy():
    print()
    print("Choose a Strategy: ")
    print("1.Balanced.  - 52 Minutes Work / 17 Minutes Break")
    print("2.Classic.   - 25 Minutes Work / 5 Minutes Break")
    print("3.Deep.      - 90 Minutes Work / 20 Minutes Break")
    print("4.Custom.    - Specify your own work and break times")
    choice = input("Choice: ")
    if choice == "1":
        return "Balanced", None, None
    elif choice == "2":
        return "Classic", None, None
    elif choice == "3":
        return "Deep", None, None
    elif choice == "4":
        custom_work = int(input("Work Period in minutes: "))
        custom_break = int(input("Break Period in minutes: "))
        return "custom", custom_work, custom_break
    else:
        print("Invalid choice. Use Number only.")
        return None, None, None
def start_session():
    global session_thread
    if session.active:
        print("A session is already active.")
        return
    print()
    print("New DevTime Session")
    print("=" * 30)

    config = load_config()
    default_time = config["default_session"]
    print(f"Default session: {default_time} minutes")

    value = input(f"How much time in minutes do you have? [{default_time}]: ")
    if value:
        total_minutes = int(value)
    else:
        total_minutes = default_time

    strategy, custom_work, custom_break = choose_strategy()
    if strategy is None:
        return
    plan = create_plan(total_minutes, strategy, custom_work, custom_break)
    session.start(total_minutes, 0, strategy, plan)
    print()
    show_plan()
    input("\nPress Enter to Start . . .")
    stop_event.clear()
    session_thread = threading.Thread(target = run_session, daemon = True)

    session_thread.start()
    print()
    print("Session started.")
    print("Type /time to see the timer.")




def run_session():
    for index, (activity, minutes) in enumerate(session.plan):
        if not session.active:
            return
        session.current_index = index
        session.start_phase(activity, minutes)

        if activity == "work":
            session.current_work = minutes
            print()
            print(f"Work for {minutes} minutes.")
            completed = wait(minutes, stop_event)
            if not completed:
                return
            session.completed_work += minutes
        else:
            session.breaks_taken += 1
            remind(session.current_minutes)
            print(f"Break: {minutes} minutes.")
            print("Come back when you're ready.")
            print("Type /time to check your session")
            completed = wait_for_break_return()

            if not completed:
                return
    if session.active:
            print()
            print("Session Complete!")
            finish_session()

def wait_for_break_return():
    while session.active:
            command = input("devtime [break]> ").strip().lower()
            if command == "":
                return True
            if command == "/time":
                show_time()
            elif command == "/end":
                end_session()
                return False
            elif command == "/plan":
                show_plan()
            elif command == "/stats":
                show_stats()
            else:
                print("type Enter to continue or /time, /plan, /stats, /end.")
    return False

def finish_session():
    save_current_session()
    session.end()
    stop_event.set()
    print("Session saved.")
def save_current_session():
    data = {
        "total_minutes": session.total_minutes,
        "completed_work": session.completed_work,
        "strategy": session.strategy,
        "breaks_taken": session.breaks_taken,
        "elapsed_seconds": session.elapsed_seconds()
    }
    save_session(data)

def end_session():
    if not session.active:
        print("No Active Session")
        return
    stop_event.set()
    session.end()
    save_current_session()
    print()
    print("Session ended.")
    print("Session saved.")


def show_plan():
    if not session.active:
        print("No active session.")
        return

    print()
    print("Your DevTime Plan")
    print("=" * 30)

    for activity, minutes in session.plan:
        if activity == "work":
            print(f"Work -> {minutes} minutes")
        else:
            print(f"Break -> {minutes} minutes")
    print("=" * 30)

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def show_time():
    if not session.active:
        print("No active session.")
        return
    remaining = session.phase_remaining_seconds()
    print()
    print("DevTime")
    print("=" * 30)
    print(f"Phase:   {session.current_phase.upper()}")
    print(f"Time left: {format_time(remaining)}")
    print(f"Session:   {format_time(session.elapsed_seconds())}")
    print(f"Completed: {session.completed_work} minutes")
    print("=" * 30)

def show_stats():
    if not session.active:
        print("No Active Session.")
        return

    print()
    print("Session Stats")
    print("=" * 30)
    print(f"Strategy: {session.strategy}")
    print(f"Planned: {session.total_minutes} minutes")
    print(f"Completed: {session.completed_work} minutes")
    print(f"Breaks taken: {session.breaks_taken}")
    if git_stats.is_git_repo():
        print()
        print("Git")
        print("=" * 30)
        branch = git_stats.current_branch()
        commits = git_stats.commit_count()
        added, removed = git_stats.changed_lines()
        files = git_stats.changed_files()
        print(f"Branch:        {branch}")
        print(f"Commits:       {commits}")
        print(f"Changed Files: {files}")
        print(f"Lines added:   +{added}")
        print(f"Lines removed: -{removed}")
    else:
        print()
        print("Not inside a Git repository")
    print("=" * 30)

def show_history():
    history = load_history()
    if not history:
        print("No previous sessions.")
        return
    print()
    print("DevTime History")
    print("=" * 30)

    for number, item in enumerate(reversed(history), 1):
        print(f"{number}. "
              f"{item['strategy']} | "
              f"{item['completed_work']} min work | "
              f"{item['breaks_taken']} breaks")

    print("=" * 30)

def extend_session():
    if not session.active:
        print("No active session.")
        return

    extra_minutes = int(input("How many minutes do you want to add? "))

    if extra_minutes <= 0:
        print("Tiem should be greater than zero.")
        return
    remaining_minutes = session.total_minutes - session.completed_work
    
    session.plan.extend(create_plan(extra_minutes, session.strategy))
    session.total_minutes += extra_minutes


    print(f"Added {extra_minutes} minutes of work to the session")

def configure():
    config = load_config()
    print()
    print("DevTime Configuration")
    print("=" * 30)
    print(f"Default session: {config['default_session']} minutes")
    print(f"Default Strategy: {config['default_strategy']}")
    print()

    session_length = input("New default session length (Enter to Keep): ")
    strategy = input("New default strategy (Balanced/Classic/Deep): ")
    if session_length:
        config["default_session"] = int(session_length)
    if strategy:
        config["default_strategy"] = strategy
    save_config(config)
    print("Configuration saved.")


def main():
    print()
    print("Welcome to DevTime")
    print("The developer focused screen break tracker")
    print("Type /help for commands.")
    print()

    while True:
        try:
            command = input("devtime> ").strip().lower()
        except KeyboardInterrupt:
            print()
            print("Use /quit to exit.")
            continue
        except EOFError:
            print()
            print("You have left the world of DevTime. Goodbye.")
            break

        if command == "/start":
            start_session()
        elif command == "/end":
            end_session()
        elif command == "/extend":
            extend_session()
        elif command == "/plan":
            show_plan()
        elif command == "/time":
            show_time()
        elif command == "/stats":
            show_stats()
        elif command == "/history":
            show_history()

        elif command == "/config":
            configure()
        elif command == "/help":
            show_help()
        elif command == "/quit":
            if session.active:
                print("End Session before quitting")
            else:
                print("You have left the world of DevTime. Goodbye.")
                break
        elif command == "":
            continue
        else:
            print("Unknown command. Type /help")


if __name__ == "__main__":
    main()