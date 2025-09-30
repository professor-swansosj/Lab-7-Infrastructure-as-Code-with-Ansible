# Instructions — Lab 7 — Infrastructure as Code with Ansible

> **Before you begin:** Open the dev container; verify Ansible and Python are available. Create the folders `logs/`, `backups/`, `templates/`, `group_vars/`, `host_vars/`, `playbooks/`, and `configs/` if missing.


Follow these steps in order.

> **Logging Requirement:** Write progress to `logs/*.log` as you complete each step.

## Step 1 — Clone repository and setup
**Goal:** Get the lab locally and initialize logs.

**What to do:**  
Clone your Classroom repo and change into it. Ensure `logs/` exists and write an initial
`LAB7_START` line into `logs/setup.log`.


**You’re done when:**  
- You are in the repo root.
- `logs/setup.log` contains `LAB7_START`.


**Log marker to add:**  
`[LAB7_START]`

## Step 2 — Open dev container and verify
**Goal:** Use the standardized environment with Ansible and collections.

**What to do:**  
Reopen in container. Verify Ansible version (2.14+), confirm `cisco.ios` is installed,
and log a `DEVCONTAINER_READY` line with version info to `logs/setup.log`.


**You’re done when:**  
- Ansible version prints successfully.
- `logs/setup.log` shows `DEVCONTAINER_READY ...`.


**Log marker to add:**  
`[DEVCONTAINER_READY]`

## Step 3 — Create inventory and ansible.cfg
**Goal:** Target the DevNet sandbox device.

**What to do:**  
Create `ansible.cfg` with local inventory path, disabled host key checking, and YAML callback.
Create `inventory.yml` with a `routers` group and `router1` host using sandbox details.
Run `ansible-inventory --list` and a simple `ansible all -m ping`.


**You’re done when:**  
- Inventory lists hosts.
- Ping succeeds to router1.
- `logs/ansible_test.log` records `INVENTORY_CREATED`.


**Log marker to add:**  
`[INVENTORY_CREATED]`

## Step 4 — Connectivity test and facts
**Goal:** Validate access and capture device facts.

**What to do:**  
Author `playbooks/test_connectivity.yml` to ping and gather facts using `cisco.ios.ios_facts`,
then append a `CONNECTIVITY_TEST` line to `logs/ansible_test.log`.


**You’re done when:**  
- Playbook finishes successfully and prints model/version.
- Log shows `CONNECTIVITY_TEST` entries.


**Log marker to add:**  
`[CONNECTIVITY_TEST]`

## Step 5 — Variable structure (group_vars and host_vars)
**Goal:** Centralize shared data and per-host overrides.

**What to do:**  
Create `group_vars/all.yml` and `group_vars/routers.yml` for global and router-group data
(e.g., DNS/NTP, default VLANs, standard loopbacks). Create `host_vars/router1.yml` for
device-specific loopbacks and VLANs. Verify access with `ansible-inventory --host router1`.


**You’re done when:**  
- Files exist with valid YAML.
- `logs/ansible_test.log` has `VARIABLES_CREATED`.


**Log marker to add:**  
`[VARIABLES_CREATED]`

## Step 6 — Jinja2 templates
**Goal:** Generate VLAN and loopback configs from variables.

**What to do:**  
Create `templates/vlans.j2` and `templates/loopbacks.j2`. Dry-run render via a small test
play to write outputs under `./configs/`.


**You’re done when:**  
- Both templates render.
- Generated files contain data from group and host vars.


**Log marker to add:**  
`[TEMPLATES_OK]`

## Step 7 — Deploy VLAN configuration
**Goal:** Apply VLANs and verify on device.

**What to do:**  
Create `playbooks/configure_vlans.yml` to render template to `configs/` and apply with
`cisco.ios.ios_config`. Verify via `show vlan brief` and log `VLAN_DEPLOYED`.


**You’re done when:**  
- VLANs appear on device.
- `logs/vlan_deployment.log` shows `VLAN_DEPLOYED`.


**Log marker to add:**  
`[VLAN_DEPLOYED]`

## Step 8 — Deploy loopback interfaces
**Goal:** Apply loopbacks and verify.

**What to do:**  
Create `playbooks/configure_loopbacks.yml` to render and apply Loopback interfaces, verify
with `show ip interface brief | include Loopback`, and log `LOOPBACK_DEPLOYED`.


**You’re done when:**  
- Loopbacks appear on device.
- `logs/loopback_deployment.log` shows `LOOPBACK_DEPLOYED`.


**Log marker to add:**  
`[LOOPBACK_DEPLOYED]`

## Step 9 — Backup device configuration
**Goal:** Save timestamped running config and summarize.

**What to do:**  
Create `playbooks/backup_config.yml` to write device backups into `backups/` with a timestamp
and update `backups/backup_log.txt`. Log `BACKUP_CREATED` to `logs/backup_operations.log`.


**You’re done when:**  
- Backup files exist with timestamps.
- `backup_log.txt` updated.
- `logs/backup_operations.log` shows `BACKUP_CREATED`.


**Log marker to add:**  
`[BACKUP_CREATED]`

## Step 10 — Master run and submit
**Goal:** Execute end-to-end and finalize.

**What to do:**  
Create `playbooks/deploy_all.yml` that imports the other playbooks. Run it, confirm device
state matches rendered configs, and add a final `LAB7_COMPLETE` line with counts.
Commit all files, push, and open a PR to `main`.


**You’re done when:**  
- All playbooks execute without errors.
- Required artifacts and logs exist.
- PR opens and Verify Docs is green.


**Log marker to add:**  
`[LAB7_COMPLETE]`


## Submission Checklist
- [ ] ansible.cfg and inventory.yml exist and validate.
- [ ] group_vars and host_vars load correctly for router1.
- [ ] templates render without errors and produce device configs under configs/.
- [ ] playbooks run without tracebacks; VLANs and loopbacks verified via show commands.
- [ ] backups directory contains timestamped config files; backup_log.txt updated.
- [ ] all required logs exist with specified markers.
- [ ] README and INSTRUCTIONS rendered from template; PR passes Verify Docs.
