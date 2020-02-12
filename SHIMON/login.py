from datetime import datetime

class LoginLimiter:
	def __init__(self):
		self.attempts: int=0
		self.max_attempts: int=3
		self.cooldown_start: float=0.0
		self.cooldown_duration: int=10

	def in_cooldown(self) -> bool:
		return self.elapsed_time()<self.cooldown_duration

	def elapsed_time(self) -> float:
		return round((
			self.get_time()-
			self.cooldown_start
		), 1)

	def time_to_wait(self) -> float:
		return round((
			self.cooldown_start-
			self.get_time()+
			self.cooldown_duration
		), 1)

	def get_time(self) -> float:
		return datetime.today().timestamp()

	def exceeded_max(self) -> bool:
		return self.attempts>=self.max_attempts

	def start_cooldown(self) -> None:
		self.cooldown_start=self.get_time()
		self.attempts=0

	def stop_cooldown(self) -> None:
		self.cooldown_start=0

	def reset(self) -> None:
		self.stop_cooldown()
		self.attempts=0
