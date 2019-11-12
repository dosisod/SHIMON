# Theme Example

This is an example css sheet which can be used to create themes.

Themes only affect pages that require to be logged, such as the index and the msg screen.

Themes do not get applied to all other pages, such as the login screen and error pages.

Variables can be suffixed with: `-fg` (foreground/text), `-bg` (background), `bd` (border), or `sd` (shadow).

```css
:root {
	--x-receiving-fg: black;    /* clickable "x" text color on receiving msgs */
	--receiving-bg: white;      /* background color for receiving msgs */
	--receiving-fg: black;      /* text color for receiving msgs */
	--receiving-bd: black;      /* border color for receiving msgs */
	--x-sending-fg: white;      /* clickable "x" text color for sending msgs */
	--sending-bg: black;        /* background for sending msgs */
	--sending-fg: white;        /* text color for sending msgs */
	--sending-bd: white;        /* border color for sending msg box */
	--typer-bd: black;          /* border color for typing in msg box */
	--typer-sd: white;          /* shadow border (trim) color around typing box */
	--container-bg: white;      /* the main background color for all the pages */
	--input-bd: #333;           /* generic border color for input boxes and textareas */
	--input-bg: white;          /* generic background color for input boxes and textareas */
	--input-fg: black;          /* generic text color for input boxes and textareas */
	--click-bg: white;          /* background color for clickable buttons */
	--click-fg: black;          /* text color for clickable buttons */
	--title-fg: black;          /* text color for titles such as usernames */
	--msg-fg: black;            /* text for msgs inside of a card (below usernames) */
	--rightitem-fg: black;      /* text color of the right sidebar items */
	--warn-fg: red;             /* error msg text color */
	--info-fg: grey;            /* text color for info (verson in account page) */
	--setting-fg: black;        /* text color for settings */
	--dropdown-bg: white;       /* background color for dropdown */
	--dropdown-bd: black;       /* border color for dropdown */
	--dropdown-fg: black;       /* text color for dropdowns */
	--dropdown-src: url("dropdown-black.png");
		/* src for arrow image for dropdowns */
	--reload-fg: black;         /* text color for reload */
	--error-bg: white;          /* background color for warning msgs */
}
```
