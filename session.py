class Session:
    def __init__(self):
        self.active = False
        self.total_minutes = 0
        self.breaks = 0
        self.strategy = ""
        self.current_work = 0
        self.completed_work = 0

    def start(self, total_minutes, breaks, strategy, plan):
        self.active = True
        self.total_minutes = total_minutes
        self.breaks = breaks
        self.strategy =strategy
        self.plan = plan
        self.current_work = 0
        self.completed_work = 0
    def end(self):
        self.active = False