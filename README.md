STUDENT SUPPORT HUB
A desktop app to find student support services and submit support requests.

CONTENTS
  1. Quick start
  2. Developer guide
  3. User manual

=====================================================================
1. QUICK START
=====================================================================
    pip install -r requirements.txt
    python src/main.py
    pyqt6

=====================================================================
2. DEVELOPER GUIDE (Users can ignore this)
=====================================================================

FILES
  src/main.py          Starts the app
  src/gui.py           Screens and buttons (MainWindow class)
  src/logic.py         Rules: search, validation, creating requests
  src/data_handler.py  Reads/writes data/data.json
  tests/               Automated tests

HOW IT WORKS
  The app has three layers. Each one only talks to the next:

      gui.py  ->  logic.py  ->  data_handler.py  ->  data.json

  - main.py creates the QApplication and MainWindow, then app.exec()
    waits for clicks.
  - MainWindow has a menu on the left and a QStackedWidget on the
    right. Each screen is a page in the stack:
        0 Home | 1 Support Services | 2 New Request | 3 My Requests
    A nav button just calls stack.setCurrentIndex(n).
  - Buttons use signals/slots, e.g.
        btn_search.clicked.connect(self.perform_search)
  - Every logic function reloads data.json, so the data is always
    up to date.

  data.json looks like this:
      {"topics": [{"category": "...", "description": "..."}],
       "announcements": ["..."],
       "requests": [{"RequestID": 1, "Category": "...",
                     "Description": "...", "Status": "Submitted"}]}



KNOWN LIMITATIONS
  - IDs could duplicate if requests were ever deleted.
  - No logins: "My Requests" shows all requests.
  - Status can't be updated (no staff screen).
  - A corrupt data.json is not handled.

=====================================================================
3. USER MANUAL
=====================================================================

GETTING STARTED
  1. Install Python 3.9+ from python.org.
  2. Open a terminal (Windows: type "cmd" in the Start menu;
     Mac: open "Terminal").
  3. Go to the folder:      cd student_support_hub
  4. Install (first time):  pip install -r requirements.txt
  5. Start the app:         python src/main.py

  Use "python3" and "pip3" on Mac/Linux if needed.

  The window has a menu on the left (Home, Support Services,
  New Request, My Requests) and the current page on the right.

  Screenshot: screenshots/01_home.png

BASIC USAGE

  Browse services
    1. Click "Support Services".
    2. Read the list. Click "Home" to go back.
    Screenshot: screenshots/02_support_services.png

  Search
    1. On Home, type a word (e.g. "counselling").
    2. Click "Search". Matching services appear in a pop-up.
    3. Click OK.
    Screenshot: screenshots/04_search_results.png

  Submit a request
    1. Click "New Request".
    2. Pick a category.
    3. Describe your problem in the box.
    4. Click "Submit Request". A message confirms it was created.
    Screenshots: screenshots/03_new_request.png
                 screenshots/05_request_created.png
    If the description is empty you will see an error. Type a
    description and try again.
    Screenshot: screenshots/07_empty_error.png

  Check your requests
    1. Click "My Requests".
    2. You will see each request's ID, category, status and details.
    Screenshot: screenshots/06_my_requests.png

TROUBLESHOOTING
  "python not recognized"  -> Reinstall Python and tick "Add to PATH".
  "No module named PyQt6"  -> Run: pip install -r requirements.txt
  Empty lists              -> data/data.json is missing; restore it.
