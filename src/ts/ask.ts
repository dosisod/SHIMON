function askForPassword(ask: string): string | void {
	const pwd=prompt(ask)

	if (!pwd) {
		throw new Error("Cannot use blank password");
	}
	else {
		return pwd
	}
}

function askForConfirmation(ask: string): string | void {
	if (!confirm(ask)) {
		throw new Error("Confirm failed")
	}
}
