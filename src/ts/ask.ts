function askForPassword(ask: string): string | void {
	const pwd=prompt(ask)

	if (!pwd) {
		throw new Error("User cancelled or used blank password.");
	}
	else {
		return pwd
	}
}

function askForConfirmation(ask: string): void {
	if (!confirm(ask)) {
		throw new Error("User cancelled or declined confirmation.")
	}
}
