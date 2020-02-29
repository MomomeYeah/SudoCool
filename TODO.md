# General

* Get secret key from os.environ

# UI

* go from puzzle entry to "solve" mode, where answer is loaded already, and we can e.g. "check so far"
* Show steps taken to solve puzzle
* Show intermediate steps and how they were calculated
* Click particular tiles to see their answer, rather than seeing them all at once?
* URL entry field should be URL type, i.e. .com button for mobile
* Manual entry boxes should be number type
* AJAX URL fetch

# Backend

* solveBoard function works, but should return something after loop terminates.  What's the right return value?
* We're doing way too much work - if we guess right that means we've solved the board, we should just return
* Store separate board for each update or just list of increments?
* Create puzzle with id/uuid for future reference
