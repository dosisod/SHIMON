def history_id(self, passed_id: str) -> int:
	for friend in self.cache["friends"]:
		if friend["id"]==passed_id:
			for index, history in enumerate(self.cache["history"]):
				if history["id"]==passed_id:
					return index

	return -1
