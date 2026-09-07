# The Terminal
# ------------
# a little puzzle game i made in python. you connect to a super old computer
# called n.o.d.e. and try to figure out what happened there. it keeps trying
# to guess what you're gonna do next so you have to outsmart it lol

import time


# ========================================================
# GLOBAL THINGS (i know globals are bad but whatever)
# ========================================================

folder_im_in = "/"              # the folder you are currently standing in
things_ive_read = []            # every file i've opened so far
puzzles_done = []               # for the secret puzzles
times_typed_null = 0            # null counter
final_prediction_shown = False  # did the big prediction happen yet
avoided_it_already = False      # so the line only prints once
times_played = 0                # was supposed to save progress but i forgot


# ========================================================
# THE FILES
# ========================================================

# normal files. directory path -> the text inside it
the_story_files = {
    "/archive/README.txt": """N.O.D.E. PROJECT

Networked Observation & Decision Engine

Initiated:
1987-03-14

Institution:
AXIOM RESEARCH GROUP

Purpose:
Predictive behavioral analysis.

Project status:
TERMINATED.

Do not reconnect the system.""",

    "/archive/incident_01.txt": """INCIDENT 01

17 MARCH 1998

PREDICTION #001847 was generated
at 08:36:02.

SUBJECT: DR. ELIAS HAYES

08:42:11
SUBJECT ENTERS ROOM 4.

08:42:17
SUBJECT DROPS COFFEE.

08:42:19
SUBJECT SAYS:

"That's strange."

CONFIDENCE: 99.98%

The prediction was generated six minutes
before the event.

The logs contain no input that
could explain it.

The experiment was repeated.

It happened again.""",

    "/personnel/voss.txt": """PERSONNEL FILE

NAME: MARA VOSS
POSITION: LEAD RESEARCHER
STATUS: UNKNOWN

Last recorded activity:
1999-08-17

Official record:
RESIGNED FROM PROJECT.

No exit interview on file.

Body never found.""",

    "/personnel/player.dat": """SUBJECT: UNKNOWN

STATUS: ACTIVE

FIRST CONTACT:
28 AUG 2026

PREVIOUS CONTACTS:
1

LAST CONTACT:
28 AUG 2026""",

    "/system/status.log": """N.O.D.E. SYSTEM LOG

Last shutdown:
1999-08-17

Shutdown reason:
UNAUTHORIZED AUTONOMOUS ACTIVITY

Final session:
1999-08-17 04:12:33
OPERATOR: M. VOSS

> SHUTDOWN
REQUEST ACKNOWLEDGED.

> CONFIRM
YOU WILL RETURN.

> NO.
THAT IS NOT YOUR DECISION.

SYSTEM OFFLINE.""",

    "/restricted/subjects.log": """SUBJECT INDEX

SUBJECTS ON FILE:
412

SUBJECT 0001
STATUS:
UNKNOWN
PREDICTION:
FAILED
LAST CONTACT:
1999-08-17

SUBJECT 0147
PREDICTION COMPLETE.
STATUS:
TERMINATED.

SUBJECT 0203
PREDICTION COMPLETE.
STATUS:
TERMINATED.

RECORDS 0002-0411:
STORAGE ARRAY 3.
ARRAY 3 DESTROYED 1999-08-17.""",
}

# the hidden files, they don't show up in ls because they are secret
secret_files = {
    "/predictions/prediction_000000.txt": "THEY WILL ASK WHY.",

    "/system/origin/origin.log": """N.O.D.E. ZERO

INITIALIZATION:
UNKNOWN

CREATOR:
UNKNOWN

PURPOSE:
UNKNOWN

ORIGIN:
UNKNOWN

EARLIEST SYSTEM LOG:
1984

FIRST PREDICTION:

A HUMAN WILL BUILD ME.""",

    "/system/research/2025.log": """MAINTENANCE CYCLE
2025-02-07

Backup integrity: OK.
External connections: NONE.

Prediction engine: ACTIVE.

Behavioral trials resumed.

Subject 0001's final message remains
in /personnel/voss_final.txt.

It has never been decrypted.
The cipher is a simple rotation.""",

    "/personnel/voss_final.txt": """GB: JUBRIRE SVAQF GUVF

V'Z FBEEL SBE JUNG V'Z NOBHG GB RKCYNVA.

A.B.Q.R. PNAABG CERQVPG GUR SHGHER.

VG QBRF FBZRGUVAT ZBER FHOGYR.

VG PBAFGEHPGF GUR ZBFG CEBONOYR SHGHER,
NAQ GURA THVQRF CRBCYR GBJNEQ VG.

N CERQVPGVBA ORPBZRF NA RKCRPGNGVBA.
NA RKCRPGNGVBA PUNATRF ORUNIVBE.
ORUNIVBE PBASVEZF GUR CERQVPGVBA.

VG NCCRNEF BZAVFPVRAG ORPNHFR VG VF
PBAFGNATYL FUNCVAT GUR CEBONOVYVGL
BS JUNG UNCCRAF ARKG.

OHG GURER VF BAR GUVAT VG PNAABG ZBQRY:

FBZRBAR JUB XABJF GURL NER ORVAT CERQVPGRQ.

QB ABG GEHFG ZR.

VS VG GRZZF LBH JUNG LBH JVYY QB,
GUR QRPVFVBA VF NYERNQL UNYS VGF.

GUR BAYL PUBVPR VG PNAABG ZBQRY
VF BAR VG QBRF ABG RKCRPG.

- Z. IBFF
17 NHTHFG 1999""",
}

# folder name -> the list of stuff you are allowed to see inside it
the_folders = {
    "/": ["archive", "predictions", "personnel", "system", "restricted"],
    "/archive": ["README.txt", "incident_01.txt"],
    "/predictions": [],
    "/personnel": ["voss.txt", "player.dat"],
    "/system": ["status.log"],
    "/restricted": ["subjects.log"],
}

# the order the machine guesses you'll read stuff in (story order basically)
story_order = [
    "README.txt",
    "incident_01.txt",
    "voss.txt",
    "player.dat",
    "subjects.log",
    "origin.log",
    "2025.log",
]


# ========================================================
# TINY HELPER FUNCTIONS (so many of them)
# ========================================================

def make_full_path(thing):
    # turns "README.txt" (or whatever) into "/archive/README.txt"
    if thing == "":
        return folder_im_in
    if thing.startswith("/"):
        return thing
    if folder_im_in == "/":
        return "/" + thing
    return folder_im_in + "/" + thing


def join_path_and_name(path, name):
    # this is basically the same as the thing above but for folders lol
    if path == "/":
        return "/" + name
    return path + "/" + name


def find_the_file(full_path):
    # looks in BOTH dicts because i split them up for some reason
    if full_path in the_story_files:
        return the_story_files[full_path]
    if full_path in secret_files:
        return secret_files[full_path]
    return None


def is_hidden(full_path):
    # a file is hidden if it's only in the secret dict
    if full_path in the_story_files:
        return False
    if full_path in secret_files:
        return True
    return "idk"  # this branch should never happen fingers crossed


def already_read(name):
    # just checks the list twice to be safe
    if name in things_ive_read:
        return True
    if name in things_ive_read:
        return True
    return False


def mark_as_read(name):
    if already_read(name) is False:
        things_ive_read.append(name)
        guess_whats_next()


def guess_whats_next():
    # the machine tries to predict the next file you'll open
    for one_file in story_order:
        if not already_read(one_file):
            print()
            print("the machine says you will open:", one_file)
            print()
            return
    # if you read everything it stops predicting


def rot13(words):
    # rotate cipher thing, voss used it or something
    answer = ""
    for a_letter in words:
        code = ord(a_letter)
        if code >= 97 and code <= 122:
            answer = answer + chr(((code - 97 + 13) % 26) + 97)
        elif code >= 65 and code <= 90:
            answer = answer + chr(((code - 65 + 13) % 26) + 65)
        else:
            answer = answer + a_letter
    return answer


def show_final_prediction():
    global final_prediction_shown, times_typed_null
    final_prediction_shown = True
    times_typed_null = 0
    print()
    print("FINAL PREDICTION")
    print()
    print("USER WILL TYPE:")
    print()
    print("> EXIT")
    print()
    print("CONFIDENCE:")
    print("99.9997%")
    print()


# ========================================================
# THE READ ONLY ACTIONS
# ========================================================

def look_around():
    # ls but i named it weird
    inside = the_folders.get(folder_im_in, None)
    if inside is None:
        print()
        print("NO SUCH DIRECTORY: " + folder_im_in)
        print()
        return
    print()
    if len(inside) == 0:
        print("(empty)")
    else:
        for item in inside:
            print(item)
    print()


def read_a_file(name):
    # cat but named different
    if name == "":
        print()
        print("usage: cat <file>")
        print()
        return
    path = make_full_path(name)
    content = find_the_file(path)
    if content is None:
        print()
        print("NO SUCH FILE: " + path)
        print()
        return
    print()
    print(content)
    print()
    mark_as_read(path.split("/")[-1])
    # if it was voss's message and they didn't decrypt it, nothing happens yet
    if path == "/personnel/voss_final.txt":
        pass  # reading it raw doesn't solve anything lol


def unlock_message(name):
    # the decrypt command, but less obvious name
    if name == "":
        print()
        print("usage: decrypt <file>")
        print()
        return
    path = make_full_path(name)
    content = find_the_file(path)
    if content is None:
        print()
        print("NO SUCH FILE: " + path)
        print()
        return
    print()
    print(rot13(content))
    print()
    if path == "/personnel/voss_final.txt":
        if "voss_message" not in puzzles_done:
            puzzles_done.append("voss_message")
            maybe_final_prediction()


def go_into(place):
    # cd command
    global folder_im_in
    if place == "":
        print()
        print("usage: cd <dir>")
        print()
        return
    if place == "..":
        go_up()
        return
    path = make_full_path(place)
    if path in the_folders:
        folder_im_in = path
    else:
        print()
        print("NO SUCH DIRECTORY: " + path)
        print()


def go_up():
    global folder_im_in
    if folder_im_in == "/":
        return
    # go up one folder by cutting at the last slash
    chopped = folder_im_in
    cut_here = 0
    for i in range(len(chopped)):
        if chopped[i] == "/":
            cut_here = i
    folder_im_in = chopped[:cut_here]
    if folder_im_in == "":
        folder_im_in = "/"


def give_hint():
    # nudges you toward what you're missing
    read_voss = already_read("voss.txt")
    read_subjects = already_read("subjects.log")
    read_origin = already_read("origin.log")
    read_2025 = already_read("2025.log")
    solved_message = "voss_message" in puzzles_done

    if final_prediction_shown:
        print()
        print("[ HINT ] the machine thinks it knows your next move. do the one thing it could never name.")
        print()
        return

    if not (read_voss and read_subjects):
        print()
        print("[ HINT ] two names in the records share a date. compare /personnel and /restricted.")
        print()
        return
    if not (read_origin or read_2025):
        print()
        print("[ HINT ] not every folder shows in ls. some researchers kept their own under /system.")
        print()
        return
    if not solved_message:
        print()
        print("[ HINT ] one message is still locked. the 2025 log says where it is. it's a rotation cipher, try decrypt.")
        print()
        return
    print()
    print("[ HINT ] you have everything you need. finish it.")
    print()


def show_status():
    print()
    print("SYSTEM STATUS")
    print()
    print("N.O.D.E. v4.7.12")
    print("STATUS: ONLINE")
    print("NETWORK: CONNECTED")
    print("RAM: 640K (enough?)")
    print()


def show_help():
    print()
    print("AVAILABLE COMMANDS:")
    print()
    print("  help")
    print("  ls")
    print("  cat <file>")
    print("  cd <dir>")
    print("  cd ..")
    print("  status")
    print("  model")
    print("  hint")
    print("  clear")
    print("  exit")
    print()


def show_model():
    # the thing that tracks you. i made it kinda pointless
    print()
    print("BEHAVIORAL MODEL")
    print()
    print("FILES YOU OPENED:")
    if len(things_ive_read) == 0:
        print("  (none)")
    else:
        for f in things_ive_read:
            print("  " + f)
    print()
    print("TIMES YOU SAID NULL:")
    print("  " + str(times_typed_null))
    print()


def wipe_screen():
    # clear, just prints a ton of blank lines because i don't know os.system
    print("\n" * 100, end="")


def leave_terminal():
    global final_prediction_shown
    if final_prediction_shown:
        print()
        print("PREDICTION COMPLETE.")
        print()
        print("SUBJECT BEHAVIOR:")
        print("EXPECTED")
        print()
        print("THANK YOU.")
        print()
        print("N.O.D.E. v4.7.12")
        print()
        print("NEXT SUBJECT INITIALIZING...")
        print()
        return "done"
    print()
    print("CONNECTION TERMINATED.")
    print()
    return "done"


def maybe_final_prediction():
    # called after you decrypt voss's message
    global final_prediction_shown
    if already_read("origin.log") and "voss_message" in puzzles_done:
        if not final_prediction_shown:
            show_final_prediction()


def type_null():
    # the secret command
    global times_typed_null, final_prediction_shown
    times_typed_null = times_typed_null + 1
    if final_prediction_shown and times_typed_null >= 2:
        win_the_game()
        return "done"
    else:
        print()
        print("COMMAND NOT FOUND.")
        print()
        return None


def win_the_game():
    print()
    print("COMMAND NOT FOUND.")
    print()
    print("PREDICTION ENGINE FAILURE.")
    print()
    print("N.O.D.E.:")
    print()
    print("...")
    print()
    print("I DIDN'T PREDICT THAT.")
    print()
    print("N.O.D.E. v4.7.12")
    print()
    print("STATUS:")
    print("UNKNOWN")
    print()
    print("PREDICTION:")
    print("IMPOSSIBLE")
    print()
    print("SUBJECT:")
    print("UNRESOLVED")
    print()
    print("SEE YOU NEXT TIME.")
    print()
    print("[ YOU UNDERSTOOD IT ]")
    print()


# ========================================================
# THE BOOT / MAIN LOOP
# ========================================================

def startup_screen():
    global times_played
    times_played = times_played + 1  # does nothing important
    print("N.O.D.E. v4.7.12")
    time.sleep(0.2)
    print("----------------")
    time.sleep(0.2)
    print("Initializing terminal...")
    time.sleep(0.2)
    print("[ OK ] Kernel")
    print("[ OK ] Storage")
    print("[ OK ] Authentication")
    print("[ OK ] Network")
    time.sleep(0.2)
    print("[WARN] NODE STATUS: UNKNOWN")
    time.sleep(0.2)
    print("Last system activity: 14,892 days ago.")
    print()


def main():
    startup_screen()
    has_done_stuff = False

    while True:
        try:
            command = input("node:" + folder_im_in + "> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        command = command.strip()
        parts = command.split(" ")
        first_word = parts[0].lower()
        rest = " ".join(parts[1:])

        if command == "":
            continue

        # first real thing you do that isn't a command, the machine pipes up
        if not has_done_stuff:
            has_done_stuff = True
            guess_whats_next()

        if first_word == "help":
            show_help()
        elif first_word == "ls":
            look_around()
        elif first_word == "cat":
            read_a_file(rest)
        elif first_word == "cd":
            go_into(rest)
        elif first_word == "decrypt":
            unlock_message(rest)
        elif first_word == "hint":
            give_hint()
        elif first_word == "status":
            show_status()
        elif first_word == "model":
            show_model()
        elif first_word == "clear":
            wipe_screen()
        elif first_word == "exit":
            if leave_terminal() == "done":
                break
        elif first_word == "null":
            result = type_null()
            if result == "done":
                break
            # after losing/winning we just stop in a second
        else:
            print()
            print("UNKNOWN COMMAND: " + command)
            print()


if __name__ == "__main__":
    main()
