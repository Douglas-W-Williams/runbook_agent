"""Generate synthetic evaluation questions with expected runbook IDs."""

import json
import os

from constants import DATA_DIR, EVAL_QUESTIONS_PATH

EVAL_QUESTIONS = [
    # Printer
    {"question": "The printer is showing a paper jam error and the light is flashing amber.", "expected_runbook_ids": ["RB-001"]},
    {"question": "How do I clear a paper jam from the fuser area?", "expected_runbook_ids": ["RB-001"]},
    {"question": "I need to install a printer on my new laptop.", "expected_runbook_ids": ["RB-002"]},
    {"question": "The printer driver says unavailable when I try to print.", "expected_runbook_ids": ["RB-002"]},
    {"question": "How do I add a network printer by IP address?", "expected_runbook_ids": ["RB-002"]},
    {"question": "All my printers show offline and the print spooler seems to be down.", "expected_runbook_ids": ["RB-003"]},
    {"question": "Print jobs keep disappearing from the queue without printing anything.", "expected_runbook_ids": ["RB-003"]},
    {"question": "How do I restart the print spooler service on Windows?", "expected_runbook_ids": ["RB-003"]},
    # VTC
    {"question": "The conference room camera shows a black screen in Teams.", "expected_runbook_ids": ["RB-004"]},
    {"question": "Remote participants can't hear us in the meeting room.", "expected_runbook_ids": ["RB-004"]},
    {"question": "There's bad echo during our video conferences.", "expected_runbook_ids": ["RB-004"]},
    {"question": "Video keeps freezing during my Teams calls.", "expected_runbook_ids": ["RB-005"]},
    {"question": "Teams is showing a network connection unstable warning.", "expected_runbook_ids": ["RB-005"]},
    # Network
    {"question": "I can browse the internet but can't access the intranet.", "expected_runbook_ids": ["RB-006"]},
    {"question": "I'm getting network path not found when mapping a drive.", "expected_runbook_ids": ["RB-006"]},
    {"question": "My laptop keeps asking for WiFi credentials on the corporate network.", "expected_runbook_ids": ["RB-007"]},
    {"question": "I get 'Can't connect to this network' on the corporate WiFi.", "expected_runbook_ids": ["RB-007"]},
    {"question": "Internal websites work by IP but not by hostname.", "expected_runbook_ids": ["RB-008"]},
    {"question": "nslookup is returning non-existent domain for internal servers.", "expected_runbook_ids": ["RB-008"]},
    # Endpoint
    {"question": "My computer blue-screened with KERNEL_DATA_INPAGE_ERROR.", "expected_runbook_ids": ["RB-009"]},
    {"question": "My workstation keeps crashing with a blue screen every few hours.", "expected_runbook_ids": ["RB-009"]},
    {"question": "My computer is very slow and Task Manager shows 100% disk usage.", "expected_runbook_ids": ["RB-010"]},
    {"question": "Applications take forever to open on my laptop.", "expected_runbook_ids": ["RB-010"]},
    {"question": "Outlook keeps crashing with 'has stopped working' errors.", "expected_runbook_ids": ["RB-011"]},
    {"question": "An application freezes and shows not responding.", "expected_runbook_ids": ["RB-011"]},
    # Access
    {"question": "My account is locked out and I can't log in.", "expected_runbook_ids": ["RB-012"]},
    {"question": "I keep getting locked out of my account every few minutes.", "expected_runbook_ids": ["RB-012"]},
    {"question": "I'm getting access denied on the shared department folder.", "expected_runbook_ids": ["RB-013"]},
    {"question": "I was added to a new team and need access to their shared drive.", "expected_runbook_ids": ["RB-013"]},
    {"question": "I got a new phone and can't get past the MFA prompt.", "expected_runbook_ids": ["RB-014"]},
    {"question": "My authenticator app lost all accounts after a phone reset.", "expected_runbook_ids": ["RB-014"]},
    # VPN
    {"question": "My VPN connects briefly then disconnects after a minute.", "expected_runbook_ids": ["RB-015"]},
    {"question": "VPN works at home but not at the hotel.", "expected_runbook_ids": ["RB-015"]},
    {"question": "I need to install the VPN client on my new laptop.", "expected_runbook_ids": ["RB-016"]},
    {"question": "VPN installation says another version is already installed.", "expected_runbook_ids": ["RB-016"]},
    # Email
    {"question": "Outlook shows disconnected and keeps asking for my password.", "expected_runbook_ids": ["RB-017"]},
    {"question": "I can't start Outlook, it says it cannot open the window.", "expected_runbook_ids": ["RB-017"]},
    {"question": "I have an email stuck in my outbox that won't send.", "expected_runbook_ids": ["RB-019"]},
    {"question": "A large attachment email is blocking all my other outgoing mail.", "expected_runbook_ids": ["RB-019"]},
    {"question": "I can't open the team shared mailbox in Outlook.", "expected_runbook_ids": ["RB-020"]},
    {"question": "Replies from our shared mailbox go to my personal sent items.", "expected_runbook_ids": ["RB-020"]},
    # Server
    {"question": "A Windows service on the server is stopped and the app is down.", "expected_runbook_ids": ["RB-021"]},
    {"question": "The monitoring alert says a service crashed on the application server.", "expected_runbook_ids": ["RB-021"]},
    {"question": "Server C: drive is almost full, below 10% free space.", "expected_runbook_ids": ["RB-022"]},
    {"question": "IIS logs are eating up all the disk space on the web server.", "expected_runbook_ids": ["RB-022"]},
    {"question": "The server is unresponsive and needs a remote reboot.", "expected_runbook_ids": ["RB-023"]},
    {"question": "How do I safely reboot a production server remotely?", "expected_runbook_ids": ["RB-023"]},
    # Storage
    {"question": "My mapped drive has a red X and says disconnected.", "expected_runbook_ids": ["RB-024"]},
    {"question": "Mapped drives disappear every time I restart my computer.", "expected_runbook_ids": ["RB-024"]},
    {"question": "The backup job failed last night with a VSS snapshot error.", "expected_runbook_ids": ["RB-025"]},
    {"question": "Backups have been failing for three days straight.", "expected_runbook_ids": ["RB-025"]},
    # Telephony
    {"question": "My desk phone says registering and won't connect.", "expected_runbook_ids": ["RB-018"]},
    {"question": "The VoIP phone shows no service on the screen.", "expected_runbook_ids": ["RB-018"]},
]


def main():
    """Write evaluation questions to JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(EVAL_QUESTIONS_PATH, "w") as f:
        json.dump(EVAL_QUESTIONS, f, indent=2)
    print(f"Generated {len(EVAL_QUESTIONS)} eval questions → {EVAL_QUESTIONS_PATH}")


if __name__ == "__main__":
    main()
