from config import load_config, save_config
from notifier import remind
from timer import wait, wait_for_return
from planner import create_plan
from session import Session

session = Session()

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
    print("/quit.  - Exit DevTime")
    print()

def start_session():
    if session.active:
        print("A session is already active.")
        return
    print()
    print("New DevTime Session")
    print("=" * 30)


    total_minutes = int(input("How much time in minutes do you have?: "))

    print()
    print("Choose a Strategy: ")
    print("1.Balanced.  - 52 Minutes Work / 17 Minutes Break")
    print("2.Classic.   - 25 Minutes Work / 5 Minutes Break")
    print("3.Deep.      - 90 Minutes Work / 20 Minutes Break")
    print("4.Custom.    - Specify your own work and break times")
    choice = input("Choice: ")
    custom_work = None
    custom_break = None

    if choice == "1":
        strategy = "Balanced"
    elif choice == "2":
        strategy = "Classic"
    elif choice == "3":
        strategy = "Deep"
    elif choice == "4":
        strategy = "custom"
        custom_work = int(input("Work Period in minutes: "))
        custom_break = int(input("Break Period in minutes: "))
    else:
        print("Invalid choice. Use Number only.")
        return

    plan = create_plan(total_minutes, strategy, custom_work, custom_break)
    session.start(total_minutes, 0, strategy, plan)

    print()
    show_plan()

    input("Press Enter to Start . . .")
    run_session()


def run_session():
    for activity, minutes in session.plan:
        if not session.active:
            return
        if activity == "work":
            session.current_work = minutes
            print()
            print(f"Work for {minutes} minutes.")
            wait(minutes)

            session.completed_work += minutes
        elif activity == "break":
            remind(session,current_work)
            print(f"Break: {minutes} minutes.")
            wait_for_return()
    print()
    print("Session Complete!")
    session.end()

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

def show_time():
    if not session.active:
        print("No active session.")
        return

    print()
    print("Session Time")
    print("=" * 30)
    print(f"Planned: {session.total_minutes} minutes")
    print(f"Completed: {session.completed_work} minutes")
    print("=" * 30)

def show_stats():
    if not session.active:
        print("No Active Session.")
        return

    print()
    print("Session Stats")
    print("=" * 30)
    print(f"Strategy: {session,strategy}")
    print(f"Planned: {session.total_minutes} minutes")
    print(f"Completed: {session.completed_work} minutes")
    print("=" * 30)

def end_session():
    if not session.active:
        print("No active session.")
        return
    session.end()

    print()
    print("Session Ended.")

def extend_session():
    if not session.active:
        print("No Active Session.")
        return
    extra_minutes = int(input("How many minutes do you want to add?: "))
    session.plan.append(("work", extra_minutes))
    session.total_minutes += extra_minutes
    print(f"Added {extra_minutes} minutes.")

def configure():
    config = load_config()
    print()
    print("DevTime Configuration")
    print("=" * 30)
    print(f"Default strategy: {config['default_strategy']}")
    print(f"Break interval: {config['break_interval']} minutes")
    print()
    strategy = input( "Default strategy " "(balanced/classic/deep): ")
    if strategy:
        config["default_strategy"] = strategy

    breaks = input("Default breaks: ")
    if breaks:
        config["default_breaks"] = int(breaks)
    save_config(config)

    print("configuration saved.")
def main():
    print()
    print("Welcome to DevTime")
    print("Type /help for commands.")
    print()

    while True:
        command = input("devtime> ").strip().lower()
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
        elif command == "/config":
            configure()
        elif command == "/help":
            show_help()
        elif command == "/quit":
            print("You have left the world of DevTime. Goodbye.")
            break
        elif command == "":
            continue
        else:
            print("Unknown command. Type /help")


if __name__ == "__main__":
    main()