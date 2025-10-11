# Instructions — Lab 7 — Infrastructure as Code with Ansible

## Objectives
- Create a complete Ansible project scaffold for network automation.
- Use inventory, group_vars, and host_vars to model multiple IOS-XE devices.
- Author two Jinja2 templates; render per-device configs from group and host data.
- Run dry-run (check mode), deploy changes, and verify with post-checks.
- Capture artifacts (rendered configs, diffs, post-check outputs) and log markers for grading.
- Demonstrate idempotency: a second run makes no changes.

## Prerequisites
- Python 3.11 (via the provided dev container)
- Accounts: GitHub, Cisco DevNet
- Devices/Sandboxes: Cisco DevNet Always-On Catalyst 8000v (IOS-XE), Cisco DevNet Always-On Catalyst 9k (IOS-XE)
- Technical: - Ansible basics (inventory, playbooks, modules, check mode).
- YAML + Jinja2 templating.
- Network CLI fundamentals (SSH to IOS-XE).
- GitHub Classroom workflow (clone, commit, push, PR).
- Credentials for both sandboxes (do NOT hardcode in repo).

## Overview
You will build a real Ansible IaC project for two IOS-XE devices (Cat8k and Cat9k). Create a proper scaffold (inventory, ansible.cfg, group_vars, host_vars, templates, playbooks). Define some loopback interfaces in group_vars (shared) and some in host_vars (device-specific), render configs from two Jinja2 templates, validate with check mode, then deploy and post-check. Save rendered configs, dry-run diffs, and post-check command outputs to the repo. Ensure a final idempotency run reports no changes.


> **Before you begin:** Open the dev container. Install collections with Ansible Galaxy. Verify connectivity to both devices (SSH reachable). Ensure you can write to `data/` and `logs/`.


## Resources
- [Ansible Documentation](https://docs.ansible.com/)- [cisco.ios Ansible Collection](https://docs.ansible.com/ansible/latest/collections/cisco/ios/)- [ansible.netcommon Collection](https://docs.ansible.com/ansible/latest/collections/ansible/netcommon/)- [Jinja2 Templates](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html)- [Check Mode & Idempotency](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#check-mode)
## Deliverables
- Ansible project scaffold: `ansible.cfg`, `inventories/`, `group_vars/`, `host_vars/`, `playbooks/`, `templates/`, `requirements.yml`.
- `group_vars/all.yml` (shared settings + shared loopbacks), optional group files (e.g., `group_vars/iosxe.yml`).
- `host_vars/cat8k.yml` and `host_vars/cat9k.yml` (device-specific loopbacks and facts).
- Two Jinja2 templates: `templates/base.j2` and `templates/loopbacks.j2`.
- Rendered configs under `data/rendered/<inventory_hostname>.cfg`.
- Dry-run diffs under `data/dryrun/<inventory_hostname>.diff`.
- Post-check outputs under `data/postcheck/<inventory_hostname>.txt`.
- `logs/lab7.log` with required markers.
- Pull request open to `main` with all artifacts committed.
- Grading: **75 points**

Follow these steps in order.

> **Logging Requirement:** Write progress to `logs/lab7.log` as you complete each step.

## Step 1 — Clone the Repository
**Goal:** Get your starter locally.

**What to do:**  
Clone your GitHub Classroom repo and `cd` into it. Create `data/{rendered,dryrun,postcheck}/`,
`logs/`, and `playbooks/`, `templates/`, `inventories/`, `group_vars/`, `host_vars/` as needed.
Initialize the log: `echo 'LAB7_START' >> logs/lab7.log`


**You're done when:**  
- Folders exist and `LAB7_START` recorded.


**Log marker to add:**  
`[LAB7_START]`

## Step 2 — Dev Container & Collections
**Goal:** Standardize the toolchain.

**What to do:**  
Reopen in container. Create `requirements.yml` with `cisco.ios` and `ansible.netcommon`.
Run: `ansible-galaxy collection install -r requirements.yml`
Record versions with `ansible --version` and log:
  - `[STEP 2] Dev Container Started`
  - `GALAXY_OK: cisco.ios`
  - `GALAXY_OK: ansible.netcommon`


**You're done when:**  
- Collections installed; Ansible available.


**Log marker to add:**  
`[[STEP 2] Dev Container Started, GALAXY_OK: cisco.ios, GALAXY_OK: ansible.netcommon]`

## Step 3 — Project Scaffold & ansible.cfg
**Goal:** Create a clean, reproducible layout.

**What to do:**  
Write `ansible.cfg` with defaults:
  - inventory = inventories/inventory.yml
  - host_key_checking = False
  - retry_files_enabled = False
  - stdout_callback = yaml
Log `PROJECT_SCAFFOLD_OK`.


**You're done when:**  
- `ansible.cfg` present and points to your inventory.


**Log marker to add:**  
`[PROJECT_SCAFFOLD_OK]`

## Step 4 — Inventory for Two Devices
**Goal:** Define Cat8k and Cat9k with groups.

**What to do:**  
Create `inventories/inventory.yml` using YAML inventory (e.g., group `iosxe`).
Each host should set:
  - ansible_host
  - ansible_network_os: cisco.ios.ios
  - ansible_connection: network_cli
  - ansible_user / password via env or prompt (not committed)
Log `INVENTORY_OK`.


**You're done when:**  
- `ansible-inventory --list` shows both hosts.


**Log marker to add:**  
`[INVENTORY_OK]`

## Step 5 — Group Vars & Host Vars
**Goal:** Model shared vs device-specific data.

**What to do:**  
In `group_vars/all.yml`, define:
  - `domain_name`, `logging_server`, and a list `loopbacks_shared` (e.g., Loopback10, Loopback11).
In `host_vars/cat8k.yml` and `host_vars/cat9k.yml`, define:
  - `hostname`, and a list `loopbacks_host` (device-specific interfaces, e.g., Loopback100/101).
Log `VARS_OK`.


**You're done when:**  
- Variables load without errors: `ansible-inventory --graph` works.


**Log marker to add:**  
`[VARS_OK]`

## Step 6 — Two Templates (Jinja2)
**Goal:** Separate baseline from interfaces.

**What to do:**  
Create:
  - `templates/base.j2` (hostname, domain, banner, logging, etc.)
  - `templates/loopbacks.j2` (renders both `loopbacks_shared` and `loopbacks_host`)
Keep templates idempotent (no duplicate interface creation). Log `TEMPLATES_OK`.


**You're done when:**  
- Templates render without exceptions using `ansible -m template` (delegate_to localhost).


**Log marker to add:**  
`[TEMPLATES_OK]`

## Step 7 — Render Configs Locally
**Goal:** Materialize per-device configs for review.

**What to do:**  
Create `playbooks/render.yml` that uses the `template` module with `delegate_to: localhost` to
produce `data/rendered/{{ inventory_hostname }}.cfg` by combining base and loopback templates
(you can assemble via `set_fact` + `copy`, or render two files and concatenate).
Run: `ansible-playbook playbooks/render.yml`
Log `RENDER_OK:<host>` for each device.


**You're done when:**  
- `data/rendered/cat8k.cfg` and `data/rendered/cat9k.cfg` exist and include both shared and host loopbacks.


**Log marker to add:**  
`[RENDER_OK]`

## Step 8 — Dry-Run (Check Mode)
**Goal:** Preview changes safely.

**What to do:**  
Create `playbooks/deploy.yml` using `cisco.ios.ios_config` to push rendered snippets.
Run with `--check` and capture diff to `data/dryrun/<host>.diff` (use `--diff`).
Log `DRYRUN_OK`.


**You're done when:**  
- Diff files exist for both devices and show intended changes.


**Log marker to add:**  
`[DRYRUN_OK]`

## Step 9 — Deploy & Post-Check
**Goal:** Apply configuration and verify.

**What to do:**  
Run `ansible-playbook playbooks/deploy.yml` (no `--check`).
Then run `playbooks/postcheck.yml` using `cisco.ios.ios_command` to collect:
  - `show ip interface brief | include Loopback`
  - `show running-config | section Loopback`
Save outputs to `data/postcheck/<host>.txt`. Log `DEPLOY_OK` and `POSTCHECK_OK`.


**You're done when:**  
- Loopbacks appear in post-check outputs for both devices.


**Log marker to add:**  
`[DEPLOY_OK, POSTCHECK_OK]`

## Step 10 — Idempotency Run
**Goal:** Second apply should report no changes.

**What to do:**  
Re-run `ansible-playbook playbooks/deploy.yml` and confirm `changed=0` for all tasks.
Append `IDEMPOTENT_OK` to the log if no changes were required.


**You're done when:**  
- Idempotent run shows zero changes.


**Log marker to add:**  
`[IDEMPOTENT_OK]`

## Step 11 — Finalize & Submit
**Goal:** Commit artifacts and open PR.

**What to do:**  
Append `LAB7_END` to `logs/lab7.log`. Commit all changes and push.
Open a pull request targeting `main`.


**You're done when:**  
- PR open; all artifacts present.


**Log marker to add:**  
`[LAB7_END]`


## FAQ
**Q:** Where do credentials go?  
**A:** Use env vars, prompts, or Ansible Vault; do not commit passwords. You can reference `ansible_user`/`ansible_password` via vars without storing secrets.

**Q:** network_cli vs httpapi?  
**A:** `network_cli` with `cisco.ios.ios` is fine for this lab. HTTPAPI/NETCONF are covered in other modules.

**Q:** Templates render but deploy fails.  
**A:** Ensure snippets are valid IOS-XE syntax and that `ios_config` sends lines in correct order.


## 🔧 Troubleshooting & Pro Tips
**Collections mismatch**  
*Symptom:* Module not found (e.g., ios_config).  
*Fix:* Install with `ansible-galaxy collection install -r requirements.yml` and set `ansible_network_os: cisco.ios.ios`.

**Idempotency noise**  
*Symptom:* Playbook always reports changes.  
*Fix:* Make templates deterministic and avoid commands that always change state (e.g., timestamps).

**Diff capture**  
*Symptom:* No diffs written.  
*Fix:* Run with `--check --diff` and redirect stdout to `data/dryrun/<host>.diff` or use callback plugins.


## Grading Breakdown
| Step | Requirement | Points |
|---|---|---|
| Step 2 | Dev container ready; Galaxy collections installed (`GALAXY_OK:*`) | 8 |
| Step 3 | Project scaffold + ansible.cfg configured (`PROJECT_SCAFFOLD_OK`) | 7 |
| Step 4 | Two-device inventory loads (`INVENTORY_OK`) | 8 |
| Step 5 | group_vars + host_vars defined (`VARS_OK`) | 8 |
| Step 6 | Two Jinja2 templates complete (`TEMPLATES_OK`) | 8 |
| Step 7 | Configs rendered for both devices (`RENDER_OK:<host>`) | 8 |
| Step 8 | Dry-run diffs captured (`DRYRUN_OK`) | 8 |
| Step 9 | Deployed and post-checked on both devices (`DEPLOY_OK`, `POSTCHECK_OK`) | 12 |
| Step 10 | Idempotency proven (`IDEMPOTENT_OK`) | 6 |
| Submission | PR open; `LAB7_START`/`LAB7_END`; log hygiene | 2 |
| **Total** |  | **75** |

## Autograder Notes
- Log file: `logs/lab7.log`
- Required markers: `LAB7_START`, `[STEP 2] Dev Container Started`, `GALAXY_OK: cisco.ios`, `GALAXY_OK: ansible.netcommon`, `PROJECT_SCAFFOLD_OK`, `INVENTORY_OK`, `VARS_OK`, `TEMPLATES_OK`, `RENDER_OK`, `DRYRUN_OK`, `DEPLOY_OK`, `POSTCHECK_OK`, `IDEMPOTENT_OK`, `LAB7_END`

## Submission Checklist
- [ ] Inventory lists Cat8k and Cat9k and connects with `network_cli`.
- [ ] `group_vars/all.yml` includes shared loopbacks; each host_vars file includes host-specific loopbacks.
- [ ] Two templates exist and render combined configs to `data/rendered/`.
- [ ] Dry-run diffs saved to `data/dryrun/`; post-check outputs saved to `data/postcheck/`.
- [ ] `logs/lab7.log` contains all required markers; PR open to `main`.
