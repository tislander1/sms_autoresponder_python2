# sms_autoresponder_python2
A usable SMS auto-responder for Python2

This Python 2 program checks a gmail account every few minutes. When an SMS from a phone matching a particular message is received, it executes a function and sends a confirmation message. As many functions (matching different messages) as the user desires can be added. You must have IMAP enabled in the gmail account used by the program. Since the password is in plain text, I use a special dedicated Gmail account for this program.  It works like this:

- Gmail recieves text from phone
- Python script checks gmail
- If a new email contains a certain phrase (ex. "please turn on the light") a function (ex. turn_on_light) is run.  Raspberry Pi or other home automation integration helps here, but is not required.
- A confirmation will be sent to the phone (ex. "OK, turned on the light")
- Be sure to add the email to the SENDER and RECIPIENT variables, and the phone number to the PHONE variable.
