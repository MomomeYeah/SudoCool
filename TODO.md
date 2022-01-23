# General

* Get secret key from os.environ
* fix python3 manage.py makemigrations
* fix python3 manage.py migrate

# UI

* go from puzzle entry to "solve" mode, where answer is loaded already, and we can e.g. "check so far"
* Show steps taken to solve puzzle
* Show intermediate steps and how they were calculated
* Click particular tiles to see their answer, rather than seeing them all at once?
* URL entry field should be URL type, i.e. .com button for mobile
* Manual entry boxes should be number type
* AJAX URL fetch
* store original data used to create board, so solution can show boxes that were solved vs. provided

# Backend

* solveBoard function works, but should return something after loop terminates.  What's the right return value?
* Store separate board for each update or just list of increments?
* Create puzzle with id/uuid for future reference
