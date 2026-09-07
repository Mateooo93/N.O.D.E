
# made this at 3am, it proably has bugs
import time


# global vars. i know there bad but idc

folder_im_in = "/"
things_ive_read = []
puzzles_done = []
times_typed_null = 0
final_prediction_shown = False
avoided_it_already = False
times_played = 0



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

the_folders = {
    "/": ["archive", "predictions", "personnel", "system", "restricted"],
    "/archive": ["README.txt", "incident_01.txt"],
    "/predictions": [],
    "/personnel": ["voss.txt", "player.dat"],
    "/system": ["status.log"],
    "/restricted": ["subjects.log"],
}

story_order = [
    "README.txt",
    "incident_01.txt",
    "voss.txt",
    "player.dat",
    "subjects.log",
    "origin.log",
    "2025.log",
]



def make_full_path(thing):
    if thing == "":
        return folder_im_in
    if thing.startswith("/"):
        return thing
    if folder_im_in == "/":
        return "/" + thing
    return folder_im_in + "/" + thing


def join_path_and_name(path, name):
    if path == "/":
        return "/" + name
    return path + "/" + name


def find_the_file(full_path):
    if full_path in the_story_files:
        return the_story_files[full_path]
    if full_path in secret_files:
        return secret_files[full_path]
    return None


def is_hidden(full_path):
    if full_path in the_story_files:
        return False
    if full_path in secret_files:
        return True
    return "idk"


def already_read(name):
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
    for one_file in story_order:
        if not already_read(one_file):
            print()
            print("the machine says you will open:", one_file)
            print()
            return


# roates letters for the cypher, voss used it or somthing
def rot13(words):
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



def look_around():
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
    if path == "/personnel/voss_final.txt":
        pass


def unlock_message(name):
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


# dont tuch this, it breaks the cd thing
def go_up():
    global folder_im_in
    if folder_im_in == "/":
        return
    chopped = folder_im_in
    cut_here = 0
    for i in range(len(chopped)):
        if chopped[i] == "/":
            cut_here = i
    folder_im_in = chopped[:cut_here]
    if folder_im_in == "":
        folder_im_in = "/"


def give_hint():
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
    global final_prediction_shown
    if already_read("origin.log") and "voss_message" in puzzles_done:
        if not final_prediction_shown:
            show_final_prediction()


# secret comand that wins the game shhh
def type_null():
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



def startup_screen():
    global times_played
    times_played = times_played + 1
    print("N.O.D.E. v4.7.12")
    print("----------------")
    print("Initializing terminal...")
    print("[ OK ] Kernel")
    print("[ OK ] Storage")
    print("[ OK ] Authentication")
    print("[ OK ] Network")
    print("[WARN] NODE STATUS: UNKNOWN")
    print("Last system activity: 14,892 days ago.")
    print()


started = False


# the game loop or whatever. gl
def boot():
    startup_screen()


def handle(command):
    global started

    command = command.strip()

    if command == "":
        return None

    parts = command.split(" ")
    first_word = parts[0].lower()
    rest = " ".join(parts[1:])

    if not started:
        started = True
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
            return "done"
    elif first_word == "null":
        if type_null() == "done":
            return "done"
    else:
        print()
        print("UNKNOWN COMMAND: " + command)
        print()

    return None


def main():
    boot()
    while True:
        try:
            command = input("node:" + folder_im_in + "> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if handle(command) == "done":
            break


if __name__ == "__main__":
    try:
        import js  # only exists in the browser, so we skip the local loop
    except ImportError:
        main()
