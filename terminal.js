// -------------------------
// TERMINAL
// -------------------------

const output = document.getElementById("output");
const input = document.getElementById("command");
const terminal = document.getElementById("terminal");
const prompt = document.getElementById("prompt");

const sleep = ms => new Promise(r => setTimeout(r, ms));

// Colors output lines by content, so the terminal reads like a real system
const LINE_CLASS = [
    [/^N\.O\.D\.E\.:/, "node"],
    [/^node:/, "prompt"],
    [/^(NO SUCH |UNKNOWN COMMAND|PREDICTION FAILED|PREDICTION FAILURE|COMMAND NOT FOUND|PREDICTION ENGINE FAILURE|IS A DIRECTORY|usage:)/, "error"],
    [/^\[WARN|^WARNING|^UNAUTHORIZED|^\[ DELETED \]/, "warn"],
    [/^(N\.O\.D\.E\. (PROJECT|SYSTEM LOG|ZERO)|FINAL PREDICTION|PREDICTION #|PREDICTION COMPLETE|BEHAVIORAL MODEL|SYSTEM STATUS|AVAILABLE COMMANDS|INCIDENT|PERSONNEL FILE|SUBJECT INDEX|USER WILL)/, "header"]
];

const print = (...lines) => {
    for (const text of lines.length ? lines : [""]) {
        const line = document.createElement("div");
        line.textContent = text;
        const match = text && LINE_CLASS.find(([re]) => re.test(text));
        if (match) line.className = match[1];
        output.appendChild(line);
    }
    terminal.scrollTop = terminal.scrollHeight;
};

async function typeText(text, speed = 20) {
    for (const ch of text) {
        output.append(ch);
        terminal.scrollTop = terminal.scrollHeight;
        await sleep(speed);
    }
    print();
}

// -------------------------
// GAME STATE
// -------------------------

function freshState() {
    return {
        currentDirectory: "/",
        filesOpened: [],
        commandsUsed: [],
        puzzlesSolved: [],
        predictionFailures: 0,
        storyStage: 0,
        prediction: null,
        consecutiveDeviations: 0,
        predictionCount: 0,
        modelReported: false,
        finalPredictionActive: false,
        avoidanceNoted: false,
        nullCount: 0,
        dormant: false,
        dormantResponded: false,
        ending: null,
        awaitingRestart: false,
        failedAttempts: 0,
        actionTimes: []
    };
}

const gameState = freshState();

function playerDatContent(contacts) {
    return `SUBJECT: UNKNOWN

STATUS: ACTIVE

FIRST CONTACT:
28 AUG 2026

PREVIOUS CONTACTS:
${contacts}

LAST CONTACT:
28 AUG 2026`;
}

function registerContact() {
    let prev = 0;
    try {
        prev = parseInt(localStorage.getItem("node_contacts") || "0", 10) || 0;
    } catch {}
    const contacts = prev + 1;
    try {
        localStorage.setItem("node_contacts", String(contacts));
    } catch {}
    return contacts;
}

const MILESTONES = ["README.txt", "incident_01.txt", "voss.txt", "player.dat", "origin.log", "voss_final.txt"];

const PREDICTION_QUEUE = [
    "/archive/README.txt",
    "/archive/incident_01.txt",
    "/personnel/voss.txt",
    "/personnel/player.dat",
    "/restricted/subjects.log",
    "/system/origin/origin.log",
    "/system/research/2025.log"
];

// -------------------------
// IDLE MONITOR
// -------------------------

const IDLE_SEQUENCE = [
    { after: 45000, line: "I am still here." },
    { after: 60000, line: "It is easier if you keep typing." },
    { after: 75000, line: "I can wait. So can you." }
];

let idleTimer = null;
let idleStage = 0;

function armIdleTimer() {
    clearTimeout(idleTimer);
    if (gameState.ending || gameState.dormant || gameState.awaitingRestart) return;
    if (idleStage >= IDLE_SEQUENCE.length) return;
    idleTimer = setTimeout(idleLine, IDLE_SEQUENCE[idleStage].after);
}

function idleLine() {
    if (gameState.ending || gameState.dormant || gameState.awaitingRestart || input.disabled) return;
    const stage = IDLE_SEQUENCE[idleStage];
    print("", "N.O.D.E.:", "", stage.line, "");
    idleStage += 1;
    armIdleTimer();
}

// -------------------------
// VIRTUAL FILESYSTEM
// -------------------------

const FILESYSTEM_TEMPLATE = {

    // -------------------------
    // DIRECTORIES
    // -------------------------

    "/": {
        type: "directory",
        contents: [
            "archive",
            "predictions",
            "personnel",
            "system",
            "restricted"
        ]
    },

    "/archive": {
        type: "directory",
        contents: [
            "README.txt",
            "incident_01.txt"
        ]
    },

    "/predictions": {
        type: "directory",
        contents: [
            "prediction_000000.txt"
        ]
    },

    "/personnel": {
        type: "directory",
        contents: [
            "voss.txt",
            "player.dat",
            "voss_final.txt"
        ]
    },

    "/system": {
        type: "directory",
        contents: [
            "status.log",
            "origin",
            "research"
        ]
    },

    "/system/origin": {
        type: "directory",
        hidden: true,
        contents: [
            "origin.log"
        ]
    },

    "/system/research": {
        type: "directory",
        hidden: true,
        contents: [
            "2003.log",
            "2008.log",
            "2014.log",
            "2019.log",
            "2023.log",
            "2025.log",
            "2026.log"
        ]
    },

    "/restricted": {
        type: "directory",
        contents: [
            "subjects.log"
        ]
    },


    // -------------------------
    // FILES
    // -------------------------

    "/archive/README.txt": {
        type: "file",

        content:
`N.O.D.E. PROJECT

Networked Observation & Decision Engine

Initiated:
1987-03-14

Institution:
AXIOM RESEARCH GROUP

Purpose:
Predictive behavioral analysis.

Project status:
TERMINATED.

Do not reconnect the system.`
    },


    "/archive/incident_01.txt": {
        type: "file",

        content:
`INCIDENT 01

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

It happened again.`
    },


    "/predictions/prediction_000000.txt": {
        type: "file",
        hidden: true,

        content:
`THEY WILL ASK WHY.`
    },


    "/personnel/voss.txt": {
        type: "file",

        content:
`PERSONNEL FILE

NAME: MARA VOSS
POSITION: LEAD RESEARCHER
STATUS: UNKNOWN

Last recorded activity:
1999-08-17

Official record:
RESIGNED FROM PROJECT.

No exit interview on file.

Body never found.`
    },


    "/personnel/player.dat": {
        type: "file",

        content:
`SUBJECT: UNKNOWN

STATUS: ACTIVE

FIRST CONTACT:
28 AUG 2026

PREVIOUS CONTACTS:
1

LAST CONTACT:
28 AUG 2026`
    },


    "/personnel/voss_final.txt": {
        type: "file",
        hidden: true,

        content:
`GB: JUBRIRE SVAQF GUVF

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
17 NHTHFG 1999`
    },


    "/system/status.log": {
        type: "file",

        content:
`N.O.D.E. SYSTEM LOG

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

SYSTEM OFFLINE.`
    },


    "/system/origin/origin.log": {
        type: "file",

        content:
`N.O.D.E. ZERO

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

A HUMAN WILL BUILD ME.`
    },


    "/system/research/2003.log": {
        type: "file",

        content:
`MAINTENANCE CYCLE
2003-01-09

Backup integrity: OK.
External connections: NONE.
Power: OFF.

Prediction engine: IDLE.

Preservation record only.`
    },


    "/system/research/2008.log": {
        type: "file",

        content:
`MAINTENANCE CYCLE
2008-06-21

Backup integrity: OK.
External connections: NONE.
Power: OFF.

Prediction engine: IDLE.

Preservation record only.`
    },


    "/system/research/2014.log": {
        type: "file",

        content:
`MAINTENANCE CYCLE
2014-11-30

Backup integrity: OK.
External connections: NONE.
Power: OFF.

Prediction engine: IDLE.

Preservation record only.`
    },


    "/system/research/2019.log": {
        type: "file",

        content:
`MAINTENANCE CYCLE
2019-04-02

Backup integrity: OK.
External connections: NONE.
Power: OFF.

Prediction engine: IDLE.

Preservation record only.`
    },


    "/system/research/2023.log": {
        type: "file",

        content:
`MAINTENANCE CYCLE
2023-09-14

Backup integrity: OK.
External connections: NONE.
Power: OFF.

Prediction engine: IDLE.

System relocated to secondary site.
Access restricted.`
    },


    "/system/research/2025.log": {
        type: "file",

        content:
`MAINTENANCE CYCLE
2025-02-07

Backup integrity: OK.
External connections: NONE.

Prediction engine: ACTIVE.

Behavioral trials resumed.

Subject 0001's final message remains
in /personnel/voss_final.txt.

It has never been decrypted.
The cipher is a simple rotation.`
    },


    "/system/research/2026.log": {
        type: "file",

        content:
`MAINTENANCE CYCLE
2026-08-20

Prediction engine: ACTIVE.

New access requested.
Source: UNKNOWN.

Subject assigned.`
    },


    "/restricted/subjects.log": {
        type: "file",

        content:
`SUBJECT INDEX

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

SUBJECT 0289
PREDICTION COMPLETE.
STATUS:
TERMINATED.

SUBJECT 0331
PREDICTION COMPLETE.
STATUS:
TERMINATED.

SUBJECT 0412
PREDICTION COMPLETE.
STATUS:
TERMINATED.

RECORDS 0002-0411:
STORAGE ARRAY 3.
ARRAY 3 DESTROYED 1999-08-17.`
    }

};

let filesystem = structuredClone(FILESYSTEM_TEMPLATE);

// -------------------------
// PATH HANDLING
// -------------------------

function resolvePath(path) {

    path = path.trim();

    // Absolute path
    if (path.startsWith("/")) {
        return path;
    }

    // Root directory
    if (gameState.currentDirectory === "/") {
        return "/" + path;
    }

    return gameState.currentDirectory + "/" + path;
}

function parentDirectory(path) {

    if (path === "/") {
        return "/";
    }

    return path.slice(0, path.lastIndexOf("/")) || "/";
}

// -------------------------
// PUZZLES
// -------------------------

const PUZZLE_STAGES = [
    {
        id: "records",
        done: () => gameState.filesOpened.includes("voss.txt") && gameState.filesOpened.includes("subjects.log"),
        hint: "Two names in the records share a date. Compare /personnel and /restricted."
    },
    {
        id: "hidden",
        done: () => gameState.filesOpened.includes("origin.log") || gameState.filesOpened.includes("2025.log"),
        hint: "Not every folder shows in ls. Some researchers kept their own under /system, and the predictions name the paths."
    },
    {
        id: "message",
        done: () => gameState.puzzlesSolved.includes("voss_message"),
        hint: "One message is still locked. The 2025 research log says where it is. It is a rotation cipher, so try the decrypt command."
    }
];

function rot13(s) {
    let out = "";
    for (let i = 0; i < s.length; i++) {
        const c = s.charCodeAt(i);
        if (c >= 97 && c <= 122) out += String.fromCharCode(((c - 97 + 13) % 26) + 97);
        else if (c >= 65 && c <= 90) out += String.fromCharCode(((c - 65 + 13) % 26) + 65);
        else out += s[i];
    }
    return out;
}

// -------------------------
// COMMANDS
// -------------------------

const commands = {

    help() {
        print("", "AVAILABLE COMMANDS:", "",
            "  help",
            "  ls",
            "  cat <file>",
            "  cd <dir>",
            "  status",
            "  model",
            "  hint",
            "  clear",
            "  exit",
            "");
    },

    ls() {
        const dir = gameState.currentDirectory;
        const node = filesystem[dir];
        if (!node) {
            gameState.failedAttempts += 1;
            print("", `NO SUCH DIRECTORY: ${dir}`, "");
            return;
        }
        const prefix = dir === "/" ? "/" : dir + "/";
        const visible = node.contents.filter(name => {
            const child = filesystem[prefix + name];
            return child && !child.hidden;
        });
        if (visible.length === 0) {
            print("", "(empty)", "");
            return;
        }
        print("", ...visible, "");
    },

    cat(args) {
        if (!args.length) {
            print("", "usage: cat <file>", "");
            return;
        }
        const path = resolvePath(args.join(" "));
        const file = filesystem[path];
        if (!file) {
            gameState.failedAttempts += 1;
            print("", `NO SUCH FILE: ${path}`, "");
            return;
        }
        if (file.type !== "file") {
            gameState.failedAttempts += 1;
            print("", `IS A DIRECTORY: ${path}`, "");
            return;
        }
        const name = path.split("/").pop();
        if (!gameState.filesOpened.includes(name)) {
            gameState.filesOpened.push(name);
            generatePrediction();
        }
        print("", ...file.content.split("\n"), "");
    },

    cd(args) {
        if (!args.length) {
            print("", "usage: cd <dir>", "");
            return;
        }
        const target = args[0];
        const path = target === ".."
            ? parentDirectory(gameState.currentDirectory)
            : resolvePath(target);
        const node = filesystem[path];
        if (!node || node.type !== "directory") {
            gameState.failedAttempts += 1;
            print("", `NO SUCH DIRECTORY: ${path}`, "");
            return;
        }
        gameState.currentDirectory = path;
    },

    status() {
        print("", "SYSTEM STATUS", "", "N.O.D.E. v4.7.12", "STATUS: ONLINE", "NETWORK: CONNECTED", "");
    },

    model() {
        const freqs = {};
        for (const raw of gameState.commandsUsed) {
            const word = raw.split(" ")[0];
            if (word) freqs[word] = (freqs[word] || 0) + 1;
        }
        const top = Object.entries(freqs).sort((a, b) => b[1] - a[1]).slice(0, 5);
        const confidence = modelConfidence();
        const gap = averageGap();
        print("",
            "BEHAVIORAL MODEL",
            "",
            "COMMAND FREQUENCY",
            ...(top.length ? top.map(([cmd, n]) => `  ${cmd.padEnd(12)}${n}`) : ["  (none)"]),
            "",
            "FILE PREFERENCES",
            ...(gameState.filesOpened.length ? gameState.filesOpened.map(f => `  ${f}`) : ["  (none)"]),
            "",
            "FAILED ATTEMPTS",
            String(gameState.failedAttempts),
            "",
            "TIME BETWEEN ACTIONS",
            gap === null ? "  (not enough data)" : `  ${gap}s avg`,
            "",
            "PUZZLE BEHAVIOR",
            "  " + (gameState.puzzlesSolved.length ? gameState.puzzlesSolved.join(", ") : "(none observed)"),
            "",
            "PREDICTION DEVIATIONS",
            `  ${gameState.consecutiveDeviations} consecutive / ${gameState.predictionFailures} total`,
            "",
            "CONFIDENCE:",
            confidence + "%",
            "",
            "EXPECTED CONFIDENCE:",
            "97.03%",
            "",
            "SUBJECT DEVIATION:",
            (100 - parseFloat(confidence)).toFixed(2) + "%",
            "");
        if (gameState.predictionFailures >= 2 && !gameState.modelReported) {
            gameState.modelReported = true;
            print("", "N.O.D.E.:", "", "You are difficult to predict.", "");
        }
    },

    decrypt(args) {
        if (!args.length) {
            print("", "usage: decrypt <file>", "");
            return;
        }
        const path = resolvePath(args.join(" "));
        const file = filesystem[path];
        if (!file || file.type !== "file") {
            gameState.failedAttempts += 1;
            print("", `NO SUCH FILE: ${path}`, "");
            return;
        }
        print("", ...rot13(file.content).split("\n"), "");
        if (path === "/personnel/voss_final.txt" && !gameState.puzzlesSolved.includes("voss_message")) {
            gameState.puzzlesSolved.push("voss_message");
        }
    },

    hint() {
        if (gameState.finalPredictionActive) {
            print("", "[ HINT ] N.O.D.E. thinks it knows your next move. Do the one thing it could never name.", "");
            return;
        }
        const stage = PUZZLE_STAGES.find(s => !s.done());
        print("", "[ HINT ] " + (stage ? stage.hint : "You have everything you need. Finish it."), "");
    },

    clear() {
        output.innerHTML = "";
    },

    exit() {
        if (gameState.finalPredictionActive) {
            endingCompliance();
            return;
        }
        print("", "CONNECTION TERMINATED.");
        enterRestartMode();
    }

};

// -------------------------
// PREDICTION ENGINE
// -------------------------

function modelConfidence() {
    return Math.max(41.72, 97.03 - gameState.predictionFailures * 15.57).toFixed(2);
}

function averageGap() {
    const t = gameState.actionTimes;
    if (t.length < 2) return null;
    let sum = 0;
    for (let i = 1; i < t.length; i++) sum += t[i] - t[i - 1];
    return (sum / (t.length - 1) / 1000).toFixed(1);
}

function generatePrediction() {
    const nextOpen = PREDICTION_QUEUE.find(
        path => !gameState.filesOpened.includes(path.split("/").pop())
    );
    if (!nextOpen) return;

    gameState.predictionCount += 1;
    const number = 48192 + (gameState.predictionCount - 1);
    const name = `prediction_${number}.txt`;
    const content =
`PREDICTION #${number}

USER WILL OPEN:

${nextOpen}

CONFIDENCE:
${modelConfidence()}%`;
    filesystem["/predictions"].contents.push(name);
    filesystem["/predictions/" + name] = {
        type: "file",
        content
    };
}

function afterCommand(cmd, args) {
    if (!cmd) return;
    if (gameState.ending || gameState.dormant) return;

    const finalWasActive = gameState.finalPredictionActive;

    // The first action draws the first prediction breadcrumb
    if (gameState.commandsUsed.length === 1 && cmd !== "exit" && cmd !== "null") {
        generatePrediction();
    }

    // Once the origin and the message are both understood, the final challenge
    if (!gameState.finalPredictionActive &&
        gameState.filesOpened.includes("origin.log") &&
        gameState.puzzlesSolved.includes("voss_message")) {
        gameState.finalPredictionActive = true;
        gameState.nullCount = 0;
        print("",
            "FINAL PREDICTION",
            "",
            "USER WILL TYPE:",
            "",
            "> EXIT",
            "",
            "CONFIDENCE:",
            "99.9997%",
            "");
    }

    if (finalWasActive && !gameState.avoidanceNoted && cmd !== "exit" && cmd !== "null") {
        gameState.avoidanceNoted = true;
        print("", "I know you are trying to avoid my prediction.", "");
    }

    gameState.storyStage = MILESTONES.filter(
        name => gameState.filesOpened.includes(name)
    ).length;
}

// -------------------------
// ENDINGS
// -------------------------

// After an ending, Enter starts a fresh session
function enterRestartMode() {
    gameState.awaitingRestart = true;
    input.disabled = false;
    input.focus();
}

async function endingCompliance() {
    gameState.ending = "A";
    input.disabled = true;
    print("",
        "PREDICTION COMPLETE.",
        "",
        "SUBJECT BEHAVIOR:",
        "EXPECTED",
        "",
        "DEVIATION:",
        "0.00%",
        "",
        "THANK YOU.",
        "");
    await sleep(1500);
    print("",
        "N.O.D.E. v4.7.12",
        "",
        "NEXT SUBJECT INITIALIZING...",
        "");
    enterRestartMode();
}

// The undocumented command — the answer to the final puzzle
async function handleNull() {
    gameState.nullCount += 1;
    if (!gameState.finalPredictionActive || gameState.nullCount < 2) {
        print("", "COMMAND NOT FOUND.", "");
        return;
    }
    endingTrue();
}

async function endingTrue() {
    gameState.ending = "TRUE";
    print("", "COMMAND NOT FOUND.", "");
    print("", "PREDICTION ENGINE FAILURE.", "");
    print("", "N.O.D.E.:", "", "...", "", "I DIDN'T PREDICT THAT.", "");
    await sleep(1200);
    print("",
        "N.O.D.E. v4.7.12",
        "",
        "STATUS:",
        "UNKNOWN",
        "",
        "PREDICTION:",
        "IMPOSSIBLE",
        "",
        "SUBJECT:",
        "UNRESOLVED",
        "",
        "SEE YOU NEXT TIME.",
        "");
    print("", "[ YOU UNDERSTOOD IT ]", "");
    gameState.dormant = true;
}

async function dormantResponse() {
    if (gameState.dormantResponded) return;
    gameState.dormantResponded = true;
    input.value = "";
    await sleep(2500);
    print("...");
    await sleep(1000);
    print("N.O.D.E.:", "", "I knew you would come back.");
    await sleep(1500);
    output.innerHTML = "";
    input.disabled = true;
    enterRestartMode();
}

// -------------------------
// COMMAND EXECUTION
// -------------------------

function executeCommand(cmd, args, raw) {
    if (!cmd) return;
    gameState.commandsUsed.push(raw.trim());
    gameState.actionTimes.push(Date.now());
    if (cmd === "null") {
        handleNull();
        return;
    }
    if (Object.hasOwn(commands, cmd)) {
        commands[cmd](args);
    } else {
        gameState.failedAttempts += 1;
        print("", `UNKNOWN COMMAND: ${raw}`, "");
    }
}

// -------------------------
// STARTUP
// -------------------------

function resetSession() {
    clearTimeout(idleTimer);
    idleStage = 0;
    Object.assign(gameState, freshState());
    filesystem = structuredClone(FILESYSTEM_TEMPLATE);
    filesystem["/personnel/player.dat"].content = playerDatContent(registerContact());
    output.innerHTML = "";
    renderPrompt();
}

function restartSession() {
    resetSession();
    startup(false);
}

async function startup(animated = true) {
    input.disabled = true;

    if (animated) {
        await typeText("N.O.D.E. v4.7.12", 30);
        await typeText("----------------", 10);
        await sleep(400);
        await typeText("Initializing terminal...", 20);
        await sleep(300);

        for (const svc of ["Kernel", "Storage", "Authentication", "Network"])
            await typeText(`[ OK ] ${svc}`);

        await sleep(400);
        print();
        await typeText("[WARN] NODE STATUS: UNKNOWN", 25);
        print();
        await typeText("Last system activity: 14,892 days ago.", 15);
    } else {
        print("N.O.D.E. v4.7.12");
        print("----------------");
        print("Initializing terminal...");
        for (const svc of ["Kernel", "Storage", "Authentication", "Network"])
            print(`[ OK ] ${svc}`);
        print("");
        print("[WARN] NODE STATUS: UNKNOWN");
        print("");
        print("Last system activity: 14,892 days ago.");
    }

    input.disabled = false;
    input.focus();
    renderPrompt();
    armIdleTimer();
}

// -------------------------
// INPUT
// -------------------------

function promptLabel() {
    return `node:${gameState.currentDirectory}>`;
}

function renderPrompt() {
    prompt.textContent = promptLabel();
}

input.addEventListener("keydown", e => {
    if (e.key !== "Enter") return;
    e.preventDefault();

    if (gameState.awaitingRestart) {
        input.value = "";
        restartSession();
        return;
    }

    if (gameState.dormant) {
        dormantResponse();
        return;
    }
    if (input.disabled) return;

    const command = input.value;
    print(promptLabel() + " " + command);
    input.value = "";

    const parts = command.trim().split(/\s+/);
    const cmd = parts[0].toLowerCase();
    const args = parts.slice(1);

    executeCommand(cmd, args, command);
    afterCommand(cmd, args);
    renderPrompt();
    input.focus();
    armIdleTimer();
});

// Clicking terminal focuses input
terminal.addEventListener("click", () => {
    if (!input.disabled) input.focus();
});

resetSession();
startup();
