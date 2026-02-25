"""Generate 25 synthetic IT runbook markdown files."""

import os
from constants import RUNBOOKS_DIR, RUNBOOK_CATEGORIES


RUNBOOKS = [
    # --- Printer (3) ---
    {
        "id": "RB-001",
        "title": "Printer Paper Jam Resolution",
        "category": "Printer",
        "symptoms": [
            "Printer displays 'Paper Jam' error on control panel",
            "Print jobs stuck in queue with status 'Error - Printing'",
            "Crumpled or partially fed paper visible in output tray",
            "Amber warning light flashing on printer front panel",
        ],
        "prerequisites": [
            "Physical access to the printer",
            "Printer model and asset tag number",
            "Latex gloves (optional, for toner-contact areas)",
        ],
        "steps": [
            "1. Power off the printer and unplug the power cable. Wait 30 seconds.",
            "2. Open the front access panel and remove the toner cartridge carefully.",
            "3. Inspect the paper path for jammed sheets. Pull paper gently in the direction of travel — never pull against feed direction.",
            "4. Open the rear access panel and check the fuser area. If paper is stuck in the fuser, pull slowly to avoid tearing.",
            "5. Check the paper tray: remove all paper, fan the stack, and reload. Confirm the paper guides are snug against the stack edges.",
            "6. Reinstall the toner cartridge and close all panels.",
            "7. Plug in and power on. Print a test page: control panel → Settings → Reports → Test Page.",
            "8. If the jam error persists, run the built-in cleaning cycle: Settings → Maintenance → Clean Paper Path.",
            "9. Clear any remaining stuck jobs: on the user's PC, open the print queue (Control Panel → Devices and Printers → right-click printer → See what's printing) and cancel all documents.",
            "10. Have the user re-send the print job.",
        ],
        "escalation": [
            "Jam recurs more than 3 times in 24 hours",
            "Paper is stuck in the fuser and cannot be removed without tools",
            "Printer displays 'Service Required' or error code 79.xx",
            "Escalate to on-site hardware technician — Priority 3",
        ],
        "related": ["RB-003"],
    },
    {
        "id": "RB-002",
        "title": "Printer Driver Installation and Configuration",
        "category": "Printer",
        "symptoms": [
            "User cannot find the printer in their device list",
            "Print jobs sent but nothing prints; no error shown",
            "'Driver is unavailable' message when selecting the printer",
            "New hire or workstation rebuild needs printer access",
        ],
        "prerequisites": [
            "User's workstation hostname and OS version",
            "Printer model, IP address, and print server queue name",
            "Admin credentials or SCCM/Intune push access",
        ],
        "steps": [
            "1. Verify the printer is online: ping the printer IP (e.g., `ping 10.20.30.40`). Confirm it responds.",
            "2. On the user's workstation, open Settings → Devices → Printers & Scanners → Add a printer.",
            "3. If the printer is on a print server, click 'The printer that I want isn't listed' → 'Select a shared printer by name' and enter `\\\\printserver01\\HP-4050-Floor3`.",
            "4. If connecting by IP, choose 'Add a printer using a TCP/IP address' and enter the printer IP.",
            "5. Windows should auto-detect the driver. If prompted, select the correct model from the list or click 'Have Disk' and browse to the driver INF file.",
            "6. For managed environments, push the driver via SCCM: Software Center → Available Applications → search for the printer package → Install.",
            "7. Set the printer as default if requested: Settings → Devices → Printers & Scanners → select printer → Manage → Set as default.",
            "8. Print a test page to confirm: right-click the printer → Printer properties → Print Test Page.",
            "9. Verify the test page output. If the page prints with garbled text, the driver version may be wrong — uninstall and retry with the manufacturer's latest driver from support.hp.com.",
        ],
        "escalation": [
            "Driver package not available in SCCM/Intune and manual install requires elevation",
            "Printer IP unreachable — may be a network or VLAN issue",
            "Escalate to Desktop Engineering for driver packaging or Networking for IP issues — Priority 4",
        ],
        "related": ["RB-001", "RB-003"],
    },
    {
        "id": "RB-003",
        "title": "Print Spooler Service Recovery",
        "category": "Printer",
        "symptoms": [
            "All printers on the workstation show 'Offline' simultaneously",
            "Print jobs disappear from the queue without printing",
            "Error: 'The print spooler service is not running'",
            "Opening Devices and Printers is extremely slow or hangs",
        ],
        "prerequisites": [
            "Admin credentials on the workstation",
            "Remote access (RDP or remote PowerShell) or user at the device",
        ],
        "steps": [
            "1. Open an elevated Command Prompt or PowerShell on the workstation.",
            "2. Check the spooler status: `sc query spooler`. Look for STATE — if it says STOPPED or STOP_PENDING, proceed.",
            "3. Stop the spooler cleanly: `net stop spooler`.",
            "4. Clear the print queue folder: `del /Q /F %systemroot%\\System32\\spool\\PRINTERS\\*`.",
            "5. Restart the spooler: `net start spooler`.",
            "6. Verify the service is running: `sc query spooler` — STATE should be RUNNING.",
            "7. If the spooler crashes again within minutes, check the Event Log: Event Viewer → Windows Logs → System → filter for Source = 'Print' or 'Spooler'. Look for faulting module names.",
            "8. A common cause is a corrupt driver. Identify recently installed printer drivers: `Get-PrinterDriver | Sort-Object -Property Date`. Remove the suspect driver: `Remove-PrinterDriver -Name 'BadDriver'`.",
            "9. Restart the spooler once more and monitor for 10 minutes.",
        ],
        "escalation": [
            "Spooler crashes repeatedly even after removing suspect drivers",
            "Spooler will not start — error 0x800706b9 (firewall/RPC issue)",
            "Multiple workstations affected (print server issue)",
            "Escalate to Desktop Engineering or Print Services — Priority 2",
        ],
        "related": ["RB-001", "RB-002"],
    },
    # --- VTC (2) ---
    {
        "id": "RB-004",
        "title": "Video Conference Camera and Audio Troubleshooting",
        "category": "VTC",
        "symptoms": [
            "Camera shows black screen or 'No camera detected' in Teams/Zoom",
            "Microphone not picking up audio — remote participants cannot hear",
            "Echo or feedback reported by remote participants",
            "USB conference device (Poly, Jabra) not recognized",
        ],
        "prerequisites": [
            "Conference room name or user's workstation details",
            "Device make/model (e.g., Poly Studio X30, Jabra Speak 750)",
            "Application in use (Teams, Zoom, WebEx)",
        ],
        "steps": [
            "1. Check physical connections: ensure the USB cable from the conference device is firmly seated in the PC/room system. Try a different USB port.",
            "2. Verify the device appears in Device Manager: Win + X → Device Manager → expand 'Cameras' and 'Audio inputs and outputs'. If the device shows a yellow triangle, right-click → Update driver.",
            "3. In the conferencing app, go to Settings → Devices (Teams) or Settings → Audio/Video (Zoom). Select the correct camera and microphone from the dropdown.",
            "4. For camera black screen: check if a privacy shutter is closed. Check if another app is using the camera: Task Manager → look for processes like 'CameraApp', 'Skype'. End them.",
            "5. For no audio pickup: check that the microphone is not muted on the physical device (LED indicator). Unmute in the app as well.",
            "6. For echo: ensure only one audio device is active (disable laptop speakers if using external). In Teams → Settings → Devices → enable 'Noise suppression' set to High.",
            "7. Power-cycle the conference device: unplug USB and power for 10 seconds, reconnect.",
            "8. If the device is a room system (Poly, Crestron), restart it via the touch panel: Settings → Restart. Boot typically takes 2-3 minutes.",
            "9. Test with a self-call or test meeting before closing the ticket.",
        ],
        "escalation": [
            "Device not recognized after driver reinstall and port swap",
            "Room system unresponsive to touch panel or remote management",
            "Issue affects all meetings in the room (possible firmware)",
            "Escalate to AV/Collaboration team — Priority 3",
        ],
        "related": ["RB-005"],
    },
    {
        "id": "RB-005",
        "title": "Video Conference Call Quality Degradation",
        "category": "VTC",
        "symptoms": [
            "Video freezing or pixelated for remote participants",
            "Audio cutting in and out, robotic voice effect",
            "High latency — noticeable delay between speaking and hearing",
            "'Network connection is unstable' warning in Teams/Zoom",
        ],
        "prerequisites": [
            "Room name or user location and network connection type (wired/wireless)",
            "Time of day and frequency of the issue",
            "Number of participants in the meeting",
        ],
        "steps": [
            "1. Determine if the user is on WiFi or wired. If WiFi, connect via ethernet if available — this resolves most quality issues.",
            "2. Run a quick bandwidth test: open a browser and go to speedtest.net. Document download/upload speeds. Video calling needs at least 3 Mbps up/down for HD.",
            "3. Check for bandwidth-heavy background activity: large file downloads, OneDrive sync, Windows Update. Pause them temporarily.",
            "4. In Teams, check call health: during a call, click '...' → 'Call health'. Note the round-trip time (should be <100ms), packet loss (should be <1%), and jitter (<30ms).",
            "5. If on WiFi, check signal strength: click the WiFi icon in the taskbar. If signal is weak, move closer to the access point or switch to a less congested band (5GHz preferred).",
            "6. Reduce video load: lower camera resolution in app settings (720p instead of 1080p). Disable 'Together mode' or 'Large gallery' views.",
            "7. If the issue persists and affects multiple users in the same area, document the location, AP name (visible in WiFi properties), and times of occurrence.",
            "8. Close and reopen the conferencing app. If severe, restart the workstation.",
        ],
        "escalation": [
            "Consistent poor quality on wired connection with adequate bandwidth",
            "Multiple users in the same building/floor affected",
            "Packet loss >5% or latency >200ms on wired connection",
            "Escalate to Network team with call quality metrics — Priority 3",
        ],
        "related": ["RB-004", "RB-008"],
    },
    # --- Network (3) ---
    {
        "id": "RB-006",
        "title": "Cannot Reach Network Resources",
        "category": "Network",
        "symptoms": [
            "User cannot access shared drives, intranet sites, or internal applications",
            "Browser shows 'This site can't be reached' for internal URLs",
            "'Network path not found' when mapping a drive",
            "Can browse the internet but not internal resources",
        ],
        "prerequisites": [
            "User's workstation IP, hostname, and location",
            "Specific resources that are unreachable (URLs, server names, share paths)",
            "Whether the issue affects one user or multiple",
        ],
        "steps": [
            "1. Verify basic connectivity: open Command Prompt and run `ipconfig /all`. Confirm the user has a valid IP (not 169.254.x.x), subnet mask, gateway, and DNS servers.",
            "2. Ping the default gateway: `ping 10.1.1.1`. If this fails, the issue is local — check cable, switch port, or WiFi connection.",
            "3. Ping an internal server by IP: `ping 10.50.100.25`. If this works but pinging by hostname fails, it's a DNS issue — see RB-008.",
            "4. Check if the user is on the correct VLAN: `ipconfig` should show an IP in the expected subnet for their location. If the IP is in a wrong range, the switchport may be misconfigured.",
            "5. Test name resolution: `nslookup intranet.company.com`. The response should return the correct internal IP. If it returns NXDOMAIN, flush DNS: `ipconfig /flushdns` and retry.",
            "6. Check if a VPN is connected when it shouldn't be (or vice versa). VPN split-tunneling can route internal traffic incorrectly.",
            "7. Test with traceroute: `tracert fileserver01.company.com`. Look for where the path stops — this identifies the failing hop.",
            "8. Verify Windows Firewall is not blocking: temporarily disable it for testing (Control Panel → Windows Defender Firewall → Turn off). Re-enable immediately after testing.",
            "9. If the resource is a web application, try accessing it from a different browser or in incognito mode to rule out cache/cookie issues.",
        ],
        "escalation": [
            "Gateway is unreachable and cable/port have been verified",
            "User is on wrong VLAN and port reconfiguration is needed",
            "Traceroute shows failure at a core router or firewall hop",
            "Escalate to Network Engineering — Priority 2",
        ],
        "related": ["RB-007", "RB-008", "RB-018"],
    },
    {
        "id": "RB-007",
        "title": "Wireless Network Authentication Failure",
        "category": "Network",
        "symptoms": [
            "Laptop prompts for WiFi credentials repeatedly",
            "WiFi connects briefly then disconnects",
            "Error: 'Can't connect to this network' on corporate SSID",
            "WiFi icon shows 'No Internet, Secured' after connecting",
        ],
        "prerequisites": [
            "User's AD account status (not locked out)",
            "Laptop model, OS version, and WiFi adapter model",
            "Corporate SSID name and authentication method (802.1X, WPA2-Enterprise)",
        ],
        "steps": [
            "1. Forget the network and reconnect: Settings → Network & Internet → WiFi → Manage known networks → select the corporate SSID → Forget. Then reconnect and enter credentials.",
            "2. Verify the user's AD account is not locked: check Active Directory Users and Computers or run `net user USERNAME /domain` from an admin workstation. Unlock if needed.",
            "3. Check the wireless adapter: Device Manager → Network adapters → find the WiFi adapter. If it shows a yellow triangle, right-click → Disable, wait 5 seconds, then Enable.",
            "4. Reset the WiFi adapter via command line: `netsh wlan disconnect` then `netsh wlan connect name=\"CorpWiFi\"`.",
            "5. Check the 802.1X certificate: if the network uses certificate-based auth, ensure the device has a valid machine certificate. Run `certlm.msc` → Personal → Certificates → look for a cert issued by the corporate CA with a valid expiration date.",
            "6. If the certificate is missing or expired, reconnect to wired ethernet and run `gpupdate /force` to request a new certificate via Group Policy auto-enrollment.",
            "7. Check if the wireless profile is configured correctly: `netsh wlan show profiles name=\"CorpWiFi\"` — verify the authentication method matches the expected config (PEAP, EAP-TLS).",
            "8. As a last resort, reset all network settings: Settings → Network & Internet → Advanced network settings → Network reset. This requires a reboot.",
        ],
        "escalation": [
            "Certificate auto-enrollment fails after gpupdate",
            "Issue affects multiple users at the same access point",
            "Wireless adapter driver issues persist after update",
            "Escalate to Network team (wireless) or Desktop Engineering (driver/cert) — Priority 3",
        ],
        "related": ["RB-006", "RB-008"],
    },
    {
        "id": "RB-008",
        "title": "DNS Resolution Failures",
        "category": "Network",
        "symptoms": [
            "Internal websites load by IP but not by hostname",
            "`nslookup` returns 'Non-existent domain' for known internal hosts",
            "Intermittent 'Server not found' errors in the browser",
            "Some internal sites work while others don't",
        ],
        "prerequisites": [
            "User's workstation IP and configured DNS servers (`ipconfig /all`)",
            "Specific hostnames that fail to resolve",
            "Whether the issue is limited to one workstation or widespread",
        ],
        "steps": [
            "1. Check configured DNS servers: `ipconfig /all`. DNS Servers should list internal DNS IPs (e.g., 10.1.1.10, 10.1.1.11). If DNS points to external servers (8.8.8.8), the machine is misconfigured.",
            "2. Flush the local DNS cache: `ipconfig /flushdns`. Then retry the lookup: `nslookup problemhost.company.com`.",
            "3. Test resolution against each DNS server individually: `nslookup problemhost.company.com 10.1.1.10` and `nslookup problemhost.company.com 10.1.1.11`. If one works and the other doesn't, the failing server may have a zone issue.",
            "4. Clear the DNS client resolver cache and re-register: `ipconfig /flushdns && ipconfig /registerdns`.",
            "5. Check the hosts file for overrides: `type C:\\Windows\\System32\\drivers\\etc\\hosts`. Remove any stale entries for the affected hostname.",
            "6. If DHCP-assigned DNS is wrong, release and renew: `ipconfig /release && ipconfig /renew`. Verify DNS servers are correct after renewal.",
            "7. Test external DNS resolution: `nslookup google.com`. If external works but internal doesn't, the internal DNS servers may be down or the workstation's DNS suffix search list is incomplete.",
            "8. Check the DNS suffix: `ipconfig /all` → Connection-specific DNS Suffix should be `company.com`. If missing, short names like `intranet` won't resolve. Add it via: Network adapter properties → IPv4 → Advanced → DNS tab.",
        ],
        "escalation": [
            "DNS servers are unreachable (ping fails to DNS IPs)",
            "One or more DNS servers returning stale or incorrect records",
            "Widespread DNS failures affecting multiple users/sites",
            "Escalate to Network/Infrastructure team — Priority 1 if widespread, Priority 3 if isolated",
        ],
        "related": ["RB-006", "RB-007"],
    },
    # --- Endpoint (3) ---
    {
        "id": "RB-009",
        "title": "Blue Screen of Death (BSOD) Diagnostics",
        "category": "Endpoint",
        "symptoms": [
            "Workstation crashes with a blue screen showing a stop code",
            "Common stop codes: KERNEL_DATA_INPAGE_ERROR, IRQL_NOT_LESS_OR_EQUAL, SYSTEM_SERVICE_EXCEPTION",
            "Machine reboots unexpectedly during normal use",
            "User reports repeated crashes at specific times or during specific tasks",
        ],
        "prerequisites": [
            "Workstation hostname and asset tag",
            "Stop code displayed on the blue screen (ask user to photograph it)",
            "Frequency and timing pattern of the crashes",
        ],
        "steps": [
            "1. Check the Event Log for crash details: Event Viewer → Windows Logs → System. Filter for Level = Critical, source = 'BugCheck'. Note the BugCheck code and parameters.",
            "2. Review reliability history: Control Panel → Security and Maintenance → Reliability Monitor. Look for red X critical events around the crash times.",
            "3. Check for recent changes: new software installed, driver updates, Windows updates. Correlate with crash timing.",
            "4. Check disk health: open Command Prompt as admin, run `wmic diskdrive get status,model`. If status is not 'OK', the drive may be failing.",
            "5. Run memory diagnostics: open Start → search 'Windows Memory Diagnostic' → Restart now and check. Results appear in Event Viewer → System → source 'MemoryDiagnosticsResults' after reboot.",
            "6. Check for driver issues: `verifier /querysettings` to see if Driver Verifier is enabled. If a third-party driver is the faulting module (visible in the dump file), update or remove it.",
            "7. Run System File Checker: `sfc /scannow`. If it finds and repairs corruption, reboot and monitor.",
            "8. If KERNEL_DATA_INPAGE_ERROR: this often indicates disk failure. Run `chkdsk C: /f /r` (requires reboot for system drive).",
            "9. Check for overheating: install HWMonitor or check BIOS for CPU temperature. Sustained temps above 90°C can cause crashes.",
        ],
        "escalation": [
            "Memory diagnostics report hardware errors",
            "Disk SMART status indicates imminent failure",
            "BSOD occurs in Safe Mode (rules out most software causes)",
            "Crash dump analysis indicates kernel/HAL corruption requiring re-image",
            "Escalate to Desktop Engineering — Priority 2",
        ],
        "related": ["RB-010", "RB-011"],
    },
    {
        "id": "RB-010",
        "title": "Slow Workstation Performance",
        "category": "Endpoint",
        "symptoms": [
            "Applications take over 30 seconds to launch",
            "System feels sluggish; mouse cursor lags",
            "Task Manager shows sustained high CPU, memory, or disk usage",
            "Fan running at full speed constantly",
        ],
        "prerequisites": [
            "Workstation hostname, model, and age",
            "RAM installed (check System → About)",
            "Whether the issue is recent or has been gradual",
        ],
        "steps": [
            "1. Open Task Manager (Ctrl+Shift+Esc) → Performance tab. Check CPU, Memory, Disk, and GPU usage. Identify which resource is at capacity.",
            "2. Switch to the Processes tab. Sort by the resource that is maxed out. Identify the top consumers.",
            "3. High CPU: if a single process is consuming >80%, note the process. Common offenders: antivirus scans, Windows Update, search indexing. If it's SearchIndexer.exe, let it finish or rebuild the index.",
            "4. High Memory: check if the machine has <8GB RAM with many apps open. Close unnecessary applications. If a browser has 50+ tabs, suggest reducing them.",
            "5. High Disk: check if the drive is HDD or SSD. HDDs are inherently slower. If Disk is at 100%, common causes: Windows Superfetch (SysMain service), antivirus scan, or a failing drive. Check drive health per RB-009 step 4.",
            "6. Clear temporary files: Settings → System → Storage → Temporary files → Remove files. Or run `cleanmgr /d C:` for a more thorough cleanup.",
            "7. Check startup programs: Task Manager → Startup tab. Disable unnecessary startup items (right-click → Disable).",
            "8. Ensure Windows updates are current: Settings → Update & Security → Check for updates. Some updates include performance fixes.",
            "9. If the machine has an HDD and is <4 years old, recommend an SSD upgrade to Desktop Engineering. This is the single biggest performance improvement for older machines.",
            "10. Reboot the machine if it hasn't been restarted in >7 days: `systeminfo | find \"Boot Time\"` to check.",
        ],
        "escalation": [
            "Machine has <8GB RAM and upgrade is needed",
            "Hard drive health check indicates imminent failure",
            "Performance issues persist after all software remediation",
            "Machine is >5 years old and qualifies for hardware refresh",
            "Escalate to Desktop Engineering — Priority 4",
        ],
        "related": ["RB-009", "RB-011"],
    },
    {
        "id": "RB-011",
        "title": "Application Crash and Recovery",
        "category": "Endpoint",
        "symptoms": [
            "Application closes unexpectedly with 'has stopped working' dialog",
            "Application freezes (not responding) and must be force-closed",
            "Error message with a specific exception code or crash dump reference",
            "Application fails to launch — shows a brief splash screen then disappears",
        ],
        "prerequisites": [
            "Application name and version",
            "Error message or exception code (screenshot preferred)",
            "Frequency: does it happen every time or intermittently?",
        ],
        "steps": [
            "1. Check the Event Log: Event Viewer → Windows Logs → Application. Filter for Level = Error, Source = 'Application Error'. Note the faulting module and exception code.",
            "2. If the app is frozen (not responding), try waiting 30 seconds. If still frozen, open Task Manager → right-click the process → End task.",
            "3. Clear the application cache/temp data. For common apps:\n   - Outlook: close Outlook, rename `%localappdata%\\Microsoft\\Outlook\\*.ost` (it will rebuild)\n   - Chrome: Settings → Privacy → Clear browsing data\n   - Teams: close Teams, delete contents of `%appdata%\\Microsoft\\Teams\\Cache`",
            "4. Repair the application: Settings → Apps → Apps & features → find the app → Advanced options → Repair. If repair fails, try Reset.",
            "5. Check for updates: open the application and check for available updates. For Microsoft 365 apps: File → Account → Update Options → Update Now.",
            "6. Run the application in compatibility mode if it's an older app: right-click the shortcut → Properties → Compatibility → check 'Run this program in compatibility mode' → select an older Windows version.",
            "7. Check if the crash correlates with a specific action (opening a file, connecting to a server). Try the action with a different file or server to isolate.",
            "8. Reinstall the application: uninstall via Settings → Apps, reboot, then reinstall from Software Center or the approved source.",
            "9. For persistent crashes with Microsoft 365 apps, run the Office Repair tool: Control Panel → Programs → Microsoft 365 → Change → Online Repair.",
        ],
        "escalation": [
            "Application crashes persist after reinstall and repair",
            "Crash dump indicates a .NET framework or runtime issue",
            "Business-critical application with no workaround available",
            "Application is not in the standard catalog and needs vendor support",
            "Escalate to Application Support or Desktop Engineering — Priority varies by business impact",
        ],
        "related": ["RB-009", "RB-010"],
    },
    # --- Access (3) ---
    {
        "id": "RB-012",
        "title": "Active Directory Account Lockout Resolution",
        "category": "Access",
        "symptoms": [
            "User receives 'Account is locked out' at Windows login",
            "User cannot authenticate to any corporate service (email, VPN, apps)",
            "Repeated lockouts within minutes of unlocking",
            "'The referenced account is currently locked out' error",
        ],
        "prerequisites": [
            "User's AD username (sAMAccountName)",
            "Access to Active Directory Users and Computers (ADUC) or AD admin center",
            "Account lockout threshold policy (typically 5 failed attempts)",
        ],
        "steps": [
            "1. Verify the lockout: open ADUC → find the user → Properties → Account tab. Check 'Unlock account' checkbox status.",
            "2. Unlock the account: check the 'Unlock account' box and click OK. Or via PowerShell: `Unlock-ADAccount -Identity jsmith`.",
            "3. Check when and where the lockout occurred: on a DC, open Event Viewer → Security log → filter for Event ID 4740. This shows the source computer name.",
            "4. For repeated lockouts, identify the source: run `Get-ADUser jsmith -Properties LockedOut,LastBadPasswordAttempt,BadLogonCount`. Note the LastBadPasswordAttempt time.",
            "5. Common sources of repeated lockouts:\n   - Mobile phone with old cached Exchange password: have user update or remove the email account on their phone\n   - Mapped drives with saved credentials: `cmdkey /list` to find stored creds, `cmdkey /delete:targetname` to remove stale ones\n   - Scheduled tasks running with the user's credentials: check Task Scheduler for tasks using the account\n   - Service accounts: check services running as the user on the source machine",
            "6. If the user has forgotten their password, perform a password reset: ADUC → right-click user → Reset Password. Check 'User must change password at next logon'. Communicate the temporary password securely.",
            "7. After resolving the source, unlock the account one final time and have the user test login.",
            "8. Monitor for 30 minutes to confirm no further lockouts.",
        ],
        "escalation": [
            "Lockout source is a system or service account that cannot be easily changed",
            "Lockouts appear to originate from unknown or external sources (potential brute-force)",
            "User's account is compromised and immediate disable is needed",
            "Escalate to Identity & Access Management or Security team — Priority 1 if compromise suspected",
        ],
        "related": ["RB-013", "RB-014"],
    },
    {
        "id": "RB-013",
        "title": "Shared Drive Permissions and Access Issues",
        "category": "Access",
        "symptoms": [
            "User gets 'Access Denied' when opening a shared folder",
            "User can read files but cannot edit or create new files",
            "User was recently added to a team and needs access to their group's share",
            "'You don't have permission to access this folder' dialog",
        ],
        "prerequisites": [
            "Full UNC path to the share (e.g., `\\\\fileserver01\\DeptShare\\TeamA`)",
            "User's AD username and current group memberships",
            "Name of the user's manager or data owner for approval",
        ],
        "steps": [
            "1. Verify the path is correct: on the user's PC, open Run (Win+R) and type the UNC path. Confirm the error message.",
            "2. Check the user's current group memberships: `net user USERNAME /domain` or PowerShell `Get-ADUser USERNAME -Properties MemberOf | Select -ExpandProperty MemberOf`.",
            "3. Identify the security group that grants access to the share. This is typically documented in the CMDB or can be found by checking the folder's NTFS permissions: right-click → Properties → Security tab.",
            "4. Compare the required group with the user's current groups. If the user is not a member of the required group, submit an access request through the IAM portal or have the user's manager approve the addition.",
            "5. Add the user to the group (if approved): `Add-ADGroupMember -Identity 'FS-TeamA-ReadWrite' -Members 'jsmith'`.",
            "6. The user may need to log off and back on for the new group membership to take effect. Alternatively, run `klist purge` and `gpupdate /force` to refresh the token.",
            "7. Verify access: have the user navigate to the share and confirm they can read, create, and modify files as expected.",
            "8. For read-only vs. read-write: NTFS permissions typically have separate groups (e.g., FS-TeamA-Read and FS-TeamA-ReadWrite). Ensure the user is in the correct group for their needed access level.",
        ],
        "escalation": [
            "No existing security group maps to the requested access",
            "Access requires data owner approval that has not been obtained",
            "Share permissions are broken (inheritance disabled, orphaned SIDs)",
            "Escalate to Identity & Access Management or File Services — Priority 4",
        ],
        "related": ["RB-012", "RB-018"],
    },
    {
        "id": "RB-014",
        "title": "Multi-Factor Authentication (MFA) Reset",
        "category": "Access",
        "symptoms": [
            "User lost or replaced their phone and can't receive MFA codes",
            "Microsoft Authenticator app shows 'No accounts' after phone reset",
            "User is locked out of all cloud services due to MFA challenge failure",
            "'More information required' loop when trying to sign in",
        ],
        "prerequisites": [
            "User's identity verified per the MFA reset verification policy (manager approval, security questions, or in-person ID check)",
            "Access to Azure AD / Entra ID admin portal or helpdesk MFA reset tool",
        ],
        "steps": [
            "1. Verify the user's identity strictly per policy. Do NOT reset MFA based solely on a phone call or email request. Acceptable verification: manager email approval, verified phone callback to HR-listed number, or in-person with photo ID.",
            "2. Access the Azure AD / Entra ID portal: portal.azure.com → Azure Active Directory → Users → find the user.",
            "3. Click 'Authentication methods' in the user's profile. You will see their registered methods (Authenticator app, phone number, FIDO2 key).",
            "4. To reset: click 'Require re-register multifactor authentication'. This invalidates all current MFA methods and forces re-registration at next login.",
            "5. Alternatively, if the user still has access to a backup method (e.g., backup phone number), they can use that to sign in and re-register the Authenticator app themselves.",
            "6. Inform the user: at their next sign-in, they will be prompted to set up MFA again. Walk them through: download Microsoft Authenticator → sign in → follow the QR code setup flow.",
            "7. If the user needs immediate access and the re-registration portal isn't working, issue a Temporary Access Pass (TAP): Azure AD → Users → user → Authentication methods → Add → Temporary Access Pass. Set a short lifetime (1 hour).",
            "8. Document the reset in the ticket, including the verification method used and the admin who performed the reset.",
        ],
        "escalation": [
            "User's identity cannot be verified per policy",
            "Azure AD admin portal is unavailable or the admin lacks permissions",
            "User's account shows signs of compromise (unfamiliar sign-ins)",
            "Escalate to Identity & Access Management or Security — Priority 1 if compromise suspected",
        ],
        "related": ["RB-012"],
    },
    # --- VPN (2) ---
    {
        "id": "RB-015",
        "title": "VPN Connection Drops and Instability",
        "category": "VPN",
        "symptoms": [
            "VPN connects briefly then disconnects after 1-5 minutes",
            "Frequent 'Reconnecting...' messages in the VPN client",
            "Error: 'The VPN connection was interrupted' or 'Connection timed out'",
            "VPN works on some networks (home) but not others (hotel, coffee shop)",
        ],
        "prerequisites": [
            "VPN client name and version (GlobalProtect, Cisco AnyConnect, Zscaler)",
            "User's ISP and connection type (home WiFi, mobile hotspot, hotel)",
            "Approximate time of disconnections",
        ],
        "steps": [
            "1. Verify internet connectivity is stable without VPN: disconnect VPN, open a browser, and confirm sites load. Run a speed test — minimum 5 Mbps down/1 Mbps up recommended for VPN.",
            "2. Check if the VPN client is up to date: open the VPN client → About/Help → compare version with the current approved version. Update if needed from Software Center.",
            "3. Try connecting to an alternate VPN gateway if available. In GlobalProtect: Settings → change portal address. In AnyConnect: dropdown in the connection window.",
            "4. Disable any third-party firewalls, antivirus, or security software temporarily. Some security tools inspect and interfere with VPN tunnels.",
            "5. If on hotel/public WiFi, the network may block VPN protocols. Try: in the VPN client settings, switch from UDP to TCP if available. Some clients support port 443 (HTTPS) which is less likely to be blocked.",
            "6. Check the VPN client logs: GlobalProtect → Settings → Show detailed log. AnyConnect → gear icon → Statistics → Export. Look for timeout or certificate errors.",
            "7. Flush DNS and reset adapter: `ipconfig /flushdns && ipconfig /release && ipconfig /renew && netsh winsock reset`. Reboot after running these commands.",
            "8. If the user is on a congested home WiFi network, suggest connecting the laptop directly to the router via ethernet cable.",
        ],
        "escalation": [
            "VPN drops persist across multiple networks and after client reinstall",
            "VPN client logs show certificate validation errors",
            "Issue coincides with a known VPN infrastructure change or outage",
            "Escalate to Network Security / VPN team — Priority 3",
        ],
        "related": ["RB-016", "RB-006"],
    },
    {
        "id": "RB-016",
        "title": "VPN Client Installation and Initial Setup",
        "category": "VPN",
        "symptoms": [
            "New hire or new laptop needs VPN client installed",
            "VPN client was removed during a system rebuild",
            "Error during VPN client installation: 'Another version is already installed'",
            "User has the client but no VPN profile/configuration",
        ],
        "prerequisites": [
            "Approved VPN client package (check SCCM/Intune or download portal)",
            "User must be on the corporate network or have an alternate access method for initial setup",
            "Local admin rights or SCCM deployment access",
        ],
        "steps": [
            "1. Check if a VPN client is already installed: look in Programs and Features for 'GlobalProtect', 'Cisco AnyConnect', or similar. If an old version exists, uninstall it first.",
            "2. For managed devices, install via SCCM/Intune: Software Center → search 'VPN' → Install. This includes the correct configuration profile.",
            "3. For manual installation: download the approved installer from the internal software portal. Run the installer as administrator.",
            "4. If you get 'Another version is already installed': uninstall the existing version via Programs and Features → reboot → try the installation again.",
            "5. After installation, launch the VPN client. Enter the portal/gateway address provided by the VPN team (e.g., `vpn.company.com`).",
            "6. For GlobalProtect: the client will auto-download the configuration from the portal after the user authenticates with their AD credentials + MFA.",
            "7. For Cisco AnyConnect: if a profile doesn't auto-download, manually import the XML profile. Copy the profile file to `C:\\ProgramData\\Cisco\\Cisco AnyConnect Secure Mobility Client\\Profile\\`.",
            "8. Test the connection: connect to VPN, then verify internal resource access by pinging an internal server or opening the intranet.",
            "9. Confirm the VPN client starts automatically at boot (check Task Manager → Startup tab).",
        ],
        "escalation": [
            "Installation fails with error codes not resolved by reinstall",
            "Device is not managed by SCCM/Intune and requires manual config",
            "VPN portal does not push the correct configuration profile",
            "Escalate to Desktop Engineering (install issues) or VPN team (config issues) — Priority 4",
        ],
        "related": ["RB-015"],
    },
    # --- Email (3) ---
    {
        "id": "RB-017",
        "title": "Outlook Profile Repair and Connectivity Issues",
        "category": "Email",
        "symptoms": [
            "Outlook shows 'Disconnected' or 'Trying to connect...' in the status bar",
            "Outlook repeatedly prompts for password",
            "Error: 'Cannot start Microsoft Outlook. Cannot open the Outlook window'",
            "Email sending/receiving works in OWA but not in the desktop client",
        ],
        "prerequisites": [
            "Outlook version (File → Office Account or Help → About)",
            "Exchange mailbox type (on-premises Exchange or Exchange Online/M365)",
            "Whether the issue started after a recent update or change",
        ],
        "steps": [
            "1. Check Outlook connection status: hold Ctrl and right-click the Outlook icon in the system tray → Connection Status. This shows the server name and connection type (HTTP, RPC).",
            "2. Test connectivity to Exchange: hold Ctrl and right-click the Outlook tray icon → Test E-mail AutoConfiguration. Enter the user's email, uncheck 'Use Guessmart' and 'Secure Guessmart Auth', click Test. Verify the correct server URL is returned.",
            "3. If Outlook prompts for credentials repeatedly: open Credential Manager (Control Panel → Credential Manager) → Windows Credentials. Remove any entries for 'outlook', 'microsoft', or 'office'. Restart Outlook.",
            "4. Repair the Outlook profile: Control Panel → Mail → Show Profiles → select profile → Properties → Email Accounts → Repair. Follow the wizard.",
            "5. If repair fails, create a new profile: Control Panel → Mail → Show Profiles → Add. Enter the user's name and email. Outlook will auto-configure. Set the new profile as default.",
            "6. If Outlook won't start at all, try safe mode: Win+R → `outlook.exe /safe`. If it starts in safe mode, the issue is likely a faulty add-in. Disable add-ins: File → Options → Add-ins → COM Add-ins → uncheck all non-Microsoft add-ins.",
            "7. Run the Office repair tool if the profile issues persist: Control Panel → Programs → Microsoft 365 → Change → Online Repair.",
            "8. Check if the OST file is corrupt or too large: the OST is typically at `%localappdata%\\Microsoft\\Outlook\\`. If it's >50GB, consider reducing the sync slider (File → Account Settings → Account Settings → Change → Mail to keep offline slider).",
        ],
        "escalation": [
            "New Outlook profile also fails to connect",
            "AutoConfiguration returns incorrect server URLs",
            "Issue started after an Exchange migration or hybrid configuration change",
            "Escalate to Messaging/Exchange team — Priority 3",
        ],
        "related": ["RB-019", "RB-020"],
    },
    {
        "id": "RB-019",
        "title": "Outlook Stuck Outbox — Messages Not Sending",
        "category": "Email",
        "symptoms": [
            "Email stuck in Outbox; send/receive does not clear it",
            "Outbox shows a count badge that doesn't decrease",
            "Large attachment email stuck and blocking all other outgoing mail",
            "Error: 'Outlook is trying to send the message...' on shutdown",
        ],
        "prerequisites": [
            "Confirm the user has network connectivity and Outlook shows 'Connected'",
            "Size of the stuck message (large attachments are a common cause)",
        ],
        "steps": [
            "1. Switch Outlook to Work Offline mode: Send/Receive tab → Work Offline. This prevents Outlook from continuously trying to send the stuck message.",
            "2. Open the Outbox folder. Try to open the stuck message. If you can open it, check the recipients and attachment size.",
            "3. If the message has a large attachment (>25MB for Exchange Online, >10MB for some on-prem configs), the attachment exceeds the send limit. Remove the attachment and use a file-sharing link instead (OneDrive, SharePoint).",
            "4. Try to drag the stuck message from Outbox to Drafts. If it won't move, the message may be in a 'sending' state.",
            "5. If the message won't move: close Outlook completely (check Task Manager to ensure OUTLOOK.EXE is not running). Reopen Outlook — the message should now be movable.",
            "6. If still stuck: close Outlook. Navigate to `%localappdata%\\Microsoft\\Outlook\\`. Rename the OST file (e.g., add .bak extension). Reopen Outlook — it will create a new OST and resync from the server. The stuck message will be gone.",
            "7. Disable Work Offline mode and test sending a new email.",
            "8. If messages continue to get stuck, check the send connector limits and transport rules with the Exchange team.",
        ],
        "escalation": [
            "Messages get stuck repeatedly even after OST rebuild",
            "Send connector or transport rule is blocking the user's messages",
            "Issue affects multiple users (server-side issue)",
            "Escalate to Messaging/Exchange team — Priority 3",
        ],
        "related": ["RB-017", "RB-020"],
    },
    {
        "id": "RB-020",
        "title": "Shared Mailbox Configuration and Access",
        "category": "Email",
        "symptoms": [
            "User cannot open a shared mailbox in Outlook",
            "Shared mailbox doesn't appear in the folder pane after being granted access",
            "User can see the shared mailbox but gets permission errors on certain folders",
            "Sent items from the shared mailbox appear in the user's personal Sent Items",
        ],
        "prerequisites": [
            "Shared mailbox email address and display name",
            "User's AD account and current Exchange permissions",
            "Whether Full Access, Send As, or Send on Behalf permissions are needed",
        ],
        "steps": [
            "1. Verify the user has been granted the correct permissions. In Exchange Admin Center or PowerShell: `Get-MailboxPermission -Identity sharedmailbox@company.com | Where {$_.User -like '*jsmith*'}`.",
            "2. If permissions are missing, grant them: `Add-MailboxPermission -Identity sharedmailbox@company.com -User jsmith -AccessRights FullAccess -AutoMapping $true`.",
            "3. With AutoMapping set to $true, the shared mailbox should appear automatically in Outlook within 30-60 minutes. If the user can't wait, they can add it manually: File → Account Settings → Account Settings → Change → More Settings → Advanced → Add the shared mailbox.",
            "4. If the mailbox appears but certain folders show 'Permission denied': the mailbox may have folder-level permissions overriding the mailbox-level FullAccess. Check with: `Get-MailboxFolderPermission -Identity sharedmailbox@company.com:\\Calendar`.",
            "5. For Send As permission: `Add-RecipientPermission -Identity sharedmailbox@company.com -Trustee jsmith -AccessRights SendAs`.",
            "6. For the sent items issue: by default, replies from a shared mailbox go to the user's Sent Items. To fix, enable the shared mailbox sent items feature: `Set-Mailbox sharedmailbox@company.com -MessageCopyForSentAsEnabled $true -MessageCopyForSendOnBehalfEnabled $true`.",
            "7. After making permission changes, the user may need to restart Outlook for changes to take effect.",
            "8. Test: have the user open the shared mailbox, read emails, reply to one, and verify the reply appears in the shared mailbox's Sent Items.",
        ],
        "escalation": [
            "Permissions are correct but the mailbox won't auto-map (possible Exchange hybrid issue)",
            "Shared mailbox is near quota and needs expansion",
            "Shared mailbox needs to be converted to a regular mailbox or vice versa",
            "Escalate to Messaging/Exchange team — Priority 4",
        ],
        "related": ["RB-017", "RB-019"],
    },
    # --- Server (3) ---
    {
        "id": "RB-021",
        "title": "Windows Service Restart Procedure",
        "category": "Server",
        "symptoms": [
            "Application dependent on a Windows service is unresponsive",
            "Service shows status 'Stopped' in services.msc unexpectedly",
            "Monitoring alert: service X is down on server Y",
            "Error: 'The dependency service or group failed to start'",
        ],
        "prerequisites": [
            "Server hostname and service name",
            "Confirm the service restart is approved (check change management if applicable)",
            "RDP or remote PowerShell access to the server",
        ],
        "steps": [
            "1. Connect to the server via RDP or remote PowerShell: `Enter-PSSession -ComputerName SERVER01`.",
            "2. Check the service status: `Get-Service -Name 'ServiceName'` or `sc query ServiceName`. Note whether the status is Stopped, Running, or Start_Pending.",
            "3. Check the service's event logs for errors: `Get-EventLog -LogName Application -Source 'ServiceName' -Newest 10` or Event Viewer → Application/System logs.",
            "4. If the service is stuck in 'Stop Pending': find the PID: `sc queryex ServiceName`. Then kill the process: `taskkill /PID <PID> /F`. Wait 10 seconds.",
            "5. Start the service: `Start-Service -Name 'ServiceName'` or `net start ServiceName`.",
            "6. If the service fails to start, check dependencies: `sc qc ServiceName` — look at the DEPENDENCIES line. Ensure all dependent services are running first.",
            "7. Check the service account: `sc qc ServiceName` — look at SERVICE_START_NAME. If the service runs as a domain account, verify the account is not locked out and the password has not expired.",
            "8. After successful restart, verify the dependent application is functional. Check by loading the app's web interface, running a health check endpoint, or confirming with the application team.",
            "9. Document the restart time, reason, and any errors encountered in the ticket.",
        ],
        "escalation": [
            "Service will not start and error logs indicate configuration corruption",
            "Service account is locked or password expired (IAM team needed)",
            "Restarting the service requires an application-level restart procedure",
            "Escalate to Server Operations or the Application team — Priority varies by service criticality",
        ],
        "related": ["RB-022", "RB-023"],
    },
    {
        "id": "RB-022",
        "title": "Server Disk Space Cleanup and Monitoring",
        "category": "Server",
        "symptoms": [
            "Monitoring alert: disk space below 10% on drive C: or D:",
            "Application writes failing with 'Disk full' or 'Insufficient disk space' errors",
            "Server performance degradation due to low disk space",
            "IIS or SQL logs consuming excessive space",
        ],
        "prerequisites": [
            "Server hostname and the affected drive letter",
            "RDP or remote PowerShell access",
            "Awareness of what applications/data reside on the drive",
        ],
        "steps": [
            "1. Connect to the server and check current disk usage: `Get-PSDrive -PSProvider FileSystem` or `wmic logicaldisk get size,freespace,caption`.",
            "2. Identify the largest space consumers. Use a quick scan: `Get-ChildItem -Path C:\\ -Recurse -ErrorAction SilentlyContinue | Sort-Object Length -Descending | Select-Object -First 20 FullName,@{N='SizeMB';E={[math]::Round($_.Length/1MB,2)}}`.",
            "3. Common space hogs on Windows servers:\n   - IIS logs: `C:\\inetpub\\logs\\LogFiles\\` — safe to compress or delete logs older than 90 days\n   - Windows temp files: `C:\\Windows\\Temp\\` — safe to delete\n   - Windows Update cleanup: run `Dism.exe /online /Cleanup-Image /StartComponentCleanup`\n   - User temp profiles: `C:\\Users\\TEMP*` — delete abandoned temp profiles\n   - SCCM cache: `C:\\Windows\\ccmcache\\` — safe to clear if not mid-deployment",
            "4. Clear IIS logs older than 90 days: `Get-ChildItem 'C:\\inetpub\\logs\\LogFiles' -Recurse -File | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-90)} | Remove-Item -Force`.",
            "5. Clear Windows temp files: `Remove-Item -Path 'C:\\Windows\\Temp\\*' -Recurse -Force -ErrorAction SilentlyContinue`.",
            "6. Check for crash dumps: `C:\\Windows\\MEMORY.DMP` and `C:\\Windows\\Minidump\\`. Delete if no longer needed for investigation.",
            "7. Run Windows Disk Cleanup in server mode: `cleanmgr /d C: /sagerun:1`.",
            "8. After cleanup, verify free space has increased: `Get-PSDrive C`. Confirm the monitoring alert has cleared (may take one polling cycle).",
            "9. If more space is needed and all cleanup is done, evaluate expanding the volume (VM) or adding storage.",
        ],
        "escalation": [
            "Drive is full and no safe files can be deleted (all data is application-critical)",
            "Volume expansion requires SAN or VM team involvement",
            "Disk space issue is recurring and needs a permanent solution (log rotation, quota)",
            "Escalate to Server Operations or Storage team — Priority 2 if services are impacted",
        ],
        "related": ["RB-021", "RB-023", "RB-025"],
    },
    {
        "id": "RB-023",
        "title": "Remote Server Reboot Procedure",
        "category": "Server",
        "symptoms": [
            "Server is unresponsive to RDP and application requests",
            "Server uptime is >90 days and a maintenance reboot is required",
            "Patching requires a post-patch reboot that was not auto-completed",
            "Application team has approved a server restart to clear a memory leak",
        ],
        "prerequisites": [
            "Server hostname and IP address",
            "Change management approval (ticket number) for non-emergency reboots",
            "List of services/applications hosted on the server",
            "Confirm all stakeholders have been notified",
        ],
        "steps": [
            "1. Notify stakeholders that the reboot is starting. Reference the change ticket number.",
            "2. If possible, gracefully stop application services before rebooting. Work with the application team if needed.",
            "3. Attempt a graceful reboot via command line: `shutdown /r /t 60 /c \"Planned reboot per CHG-12345\" /f` — this gives 60 seconds warning and forces applications to close.",
            "4. If the server is unresponsive to remote commands, try remote WMI: `Restart-Computer -ComputerName SERVER01 -Force -Wait`. The `-Wait` parameter waits for the reboot to complete before returning.",
            "5. If WMI fails, try iLO/iDRAC/IPMI out-of-band management console to perform a hardware-level reboot.",
            "6. After issuing the reboot, monitor the server coming back online: `Test-Connection -ComputerName SERVER01 -Count 1 -Quiet` in a loop, or watch the management console.",
            "7. Once the server is back: verify RDP access, check that all critical services are running: `Get-Service | Where-Object {$_.StartType -eq 'Automatic' -and $_.Status -ne 'Running'}`. Start any that failed to auto-start.",
            "8. Verify the application is functional: load the web interface, check health endpoints, confirm database connectivity as applicable.",
            "9. Update the change ticket with the reboot time, duration, and any issues encountered.",
            "10. Notify stakeholders that the server is back online and services are verified.",
        ],
        "escalation": [
            "Server does not come back online within 15 minutes of reboot",
            "iLO/iDRAC console shows hardware errors during POST",
            "Critical services do not start after reboot",
            "Escalate to Server Operations (OS issues) or Data Center team (hardware) — Priority 1 if production",
        ],
        "related": ["RB-021", "RB-022"],
    },
    # --- Storage (2) ---
    {
        "id": "RB-024",
        "title": "Mapped Drive Reconnection Failure",
        "category": "Storage",
        "symptoms": [
            "Mapped drive shows red X icon in File Explorer",
            "Error: 'The network path was not found' when opening a mapped drive",
            "Mapped drives disappear after reboot",
            "Drive letter shows as 'Disconnected Network Drive'",
        ],
        "prerequisites": [
            "The drive letter and full UNC path of the mapped drive",
            "User's AD credentials and group membership",
            "Whether the mapping is via GPO, login script, or manual",
        ],
        "steps": [
            "1. Click on the mapped drive in File Explorer to trigger a reconnection. Sometimes the red X clears after a few seconds.",
            "2. If it doesn't reconnect, verify the file server is accessible: open Run (Win+R) and type the UNC path (e.g., `\\\\fileserver01\\DeptShare`). If this works, the server is fine and the issue is the persistent mapping.",
            "3. Remove the broken mapping: `net use Z: /delete`. Then re-create it: `net use Z: \\\\fileserver01\\DeptShare /persistent:yes`.",
            "4. If the drive disappears after reboot, check if it was created with `/persistent:yes`. Without this flag, manual mappings are session-only.",
            "5. Check if the mapping is supposed to come from a GPO or login script. Run `gpresult /r` and look under 'Applied Group Policy Objects' for drive map policies. If the policy is missing, the user may have moved to an OU where the GPO doesn't apply.",
            "6. If GPO-based: force a policy refresh `gpupdate /force` and log off/on. Check Event Viewer → Application → Group Policy for errors.",
            "7. If the file server name has changed or a DFS path has been updated, the old mapping points to a stale target. Get the correct path from the storage team and update the mapping.",
            "8. For persistent issues on Windows 10/11, check a known bug with SMBv1: if the server requires SMBv1 but it's disabled on the client, connections will fail. Verify: `Get-SmbServerConfiguration | Select EnableSMB1Protocol`. If SMBv1 is needed, enable it (with security team approval) or upgrade the server.",
        ],
        "escalation": [
            "File server is unreachable (network or server issue)",
            "GPO drive mapping is failing for multiple users",
            "DFS namespace needs updating",
            "Escalate to File Services (server/DFS) or Desktop Engineering (GPO) — Priority 3",
        ],
        "related": ["RB-013", "RB-006"],
    },
    {
        "id": "RB-025",
        "title": "Backup Job Failure Investigation",
        "category": "Storage",
        "symptoms": [
            "Backup monitoring shows failed job for a server or application",
            "Error: 'VSS snapshot failed', 'Backup target unreachable', or 'Insufficient disk space on backup target'",
            "Backup has been failing for multiple consecutive days",
            "RPO (Recovery Point Objective) at risk due to failed backups",
        ],
        "prerequisites": [
            "Backup product in use (Veeam, Commvault, Veritas NetBackup, Azure Backup)",
            "Server name and backup job name",
            "Access to the backup management console",
        ],
        "steps": [
            "1. Open the backup management console and locate the failed job. Review the error message and error code.",
            "2. Common failure reasons and resolutions:\n   - **VSS failure**: on the source server, check VSS writers: `vssadmin list writers`. Look for writers in a 'Failed' or 'Waiting for completion' state. Restart the offending service (e.g., restart the 'Volume Shadow Copy' service: `net stop vss && net start vss`).\n   - **Target unreachable**: verify network connectivity between the backup server and the target repository. Ping the target IP. Check if the target share/path requires credential updates.\n   - **Insufficient space on target**: check the backup repository free space. Archive or delete old backup sets per the retention policy. Consider extending the repository storage.",
            "3. Check if the source server was rebooted or a service restarted during the backup window. Backups running during a reboot will fail.",
            "4. For Veeam: open the job session log (right-click job → Statistics). Look for the specific task that failed and the error detail.",
            "5. If the backup agent on the source server is not communicating: restart the backup agent service on the source server. For Veeam: `Restart-Service VeeamBackupSvc`. For Commvault: restart 'Commvault Communications Service'.",
            "6. Retry the backup job manually from the console. Monitor it to ensure it completes successfully.",
            "7. If the job succeeds on retry, it may have been a transient issue. If it fails again with the same error, further investigation is needed.",
            "8. Document the failure, root cause, and resolution in the ticket. Note the RPO gap (how many hours/days of backups were missed) for compliance tracking.",
        ],
        "escalation": [
            "VSS writers remain in failed state after service restarts",
            "Backup repository is full and cannot be expanded without storage team",
            "Backup job has failed for >48 hours and RPO is breached",
            "Backup infrastructure issue (media server down, license expired)",
            "Escalate to Backup/Storage team — Priority 2 if RPO is breached",
        ],
        "related": ["RB-022"],
    },
    # --- Telephony (1) ---
    {
        "id": "RB-018",
        "title": "VoIP Phone Not Registering",
        "category": "Telephony",
        "symptoms": [
            "Desk phone displays 'Registering...' or 'No Service' indefinitely",
            "Phone screen is blank or shows only the Cisco/Poly logo",
            "Phone has dial tone but cannot make or receive calls",
            "Error: 'Registration Rejected' or 'Config file not found'",
        ],
        "prerequisites": [
            "Phone model and MAC address (label on bottom of phone)",
            "Phone's IP address (Settings → Network Status on the phone)",
            "CUCM/UCM server address and user's extension/DN",
        ],
        "steps": [
            "1. Check if the phone has an IP address: on the phone, press Settings/gear → Network → IPv4. If the IP is 0.0.0.0 or starts with 169.254, the phone is not getting DHCP.",
            "2. Check the network port: ensure the ethernet cable is firmly connected to the phone and the wall jack. Try a different cable. Verify the switch port is active: `show interface status` on the switch (network team may need to verify).",
            "3. If no DHCP: check that the switch port is configured for the voice VLAN. The phone should get an IP from the voice VLAN DHCP scope. Restart the phone: unplug power/ethernet for 10 seconds, reconnect.",
            "4. If the phone has an IP but won't register: verify it can reach the call manager. From a PC on the same network: `ping <CUCM_IP>`. If CUCM is unreachable, it's a network routing issue.",
            "5. Check the phone's TFTP/config server setting: Settings → Network → TFTP Server. This should point to the CUCM server. If wrong, it can be corrected via DHCP Option 150 or manually on the phone.",
            "6. On the CUCM admin page: Device → Phone → search for the MAC address. Verify the phone is configured and assigned to the correct Device Pool and CSS (Calling Search Space).",
            "7. If the phone was recently moved to a new desk/port, it may need its device pool updated in CUCM to match the new location.",
            "8. Reset the phone to factory defaults as a last resort: on Cisco phones, press Settings → **##** during boot → select 'Erase' when prompted. The phone will re-register and download its config from CUCM.",
        ],
        "escalation": [
            "Phone not appearing in CUCM — needs to be added/provisioned",
            "Voice VLAN or DHCP scope issues affecting multiple phones",
            "CUCM cluster is down or unreachable from the phone subnet",
            "Escalate to Voice/Telecom team — Priority 2 if user has no phone service",
        ],
        "related": ["RB-006"],
    },
]


def generate_runbook(runbook: dict) -> str:
    """Generate a markdown-formatted runbook from a definition dict."""
    lines = []
    lines.append(f"# {runbook['id']}: {runbook['title']}")
    lines.append("")
    lines.append(f"## Category")
    lines.append("")
    lines.append(runbook["category"])
    lines.append("")
    lines.append("## Symptoms")
    lines.append("")
    for symptom in runbook["symptoms"]:
        lines.append(f"- {symptom}")
    lines.append("")
    lines.append("## Prerequisites")
    lines.append("")
    for prereq in runbook["prerequisites"]:
        lines.append(f"- {prereq}")
    lines.append("")
    lines.append("## Resolution Steps")
    lines.append("")
    for step in runbook["steps"]:
        lines.append(step)
        lines.append("")
    lines.append("## Escalation Criteria")
    lines.append("")
    for crit in runbook["escalation"]:
        lines.append(f"- {crit}")
    lines.append("")
    lines.append("## Related Runbooks")
    lines.append("")
    for related in runbook["related"]:
        lines.append(f"- {related}")
    lines.append("")
    return "\n".join(lines)


def main():
    """Generate all runbook markdown files."""
    os.makedirs(RUNBOOKS_DIR, exist_ok=True)

    for runbook in RUNBOOKS:
        filename = f"{runbook['id']}.md"
        filepath = os.path.join(RUNBOOKS_DIR, filename)
        content = generate_runbook(runbook)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Generated {filepath}")

    print(f"\nGenerated {len(RUNBOOKS)} runbooks in {RUNBOOKS_DIR}")


if __name__ == "__main__":
    main()
