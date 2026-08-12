import datetime


class Session:
    def __init__(self):
        self.active = False
        self.total_minutes = 0
        self.strategy = ""

        self.current_index = 0
        self.current_phase = ""
        self.current_minutes = 0

        self.completed_work = 0
        self.breaks_taken = 0

        self.start_time = None
        self.phase_start = None

        self.git_start_commit = None
        self.git_start_changes = (0,0)


    def start(self, total_minutes, breaks, strategy, plan):
        self.active = True
        self.total_minutes = total_minutes
        self.strategy =strategy
        self.plan = plan

        self.current_index = 0
        self.current_phase = ""
        self.current_minutes = 0

        self.completed_work = 0
        self.breaks_taken = 0

        self.start_time = datetime.datetime.now()
        self.phase_start = datetime.datetime.now()

    def start_phase(self, activity, minutes):
        self.current_phase = activity
        self.current_minutes = minutes
        self.phase_start = datetime.datetime.now()

    def end(self):
        self.active = False

    def elapsed_seconds(self):
        if self.start_time is None:
            return 0

        elapsed = datetime.datetime.now() - self.start_time
        return int(elapsed.total_seconds())

    def phase_elapsed_seconds(self):
        if self.phase_start is None:
            return 0
        elapsed = datetime.datetime.now() - self.phase_start
        return int(elapsed.total_seconds())

    def phase_remaining_seconds(self):
        total_seconds = self.current_minutes * 60
        remaining = total_seconds - self.phase_elapsed_seconds()
        return max(remaining,0)