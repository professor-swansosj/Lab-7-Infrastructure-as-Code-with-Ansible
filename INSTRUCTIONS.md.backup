# Lab Instructions

## Lab Title
**Infrastructure as Code with Ansible**

## Version
`v1.0`

## Estimated Time
`120-150 Minutes`

---

## Learning Objectives
By the end of this lab, you will be able to:
- **Objective 1** – Create and configure Ansible inventory files to manage network devices
- **Objective 2** – Use Ansible to test connectivity and gather facts from Cisco devices in DevNet Always-On Sandbox
- **Objective 3** – Implement host_vars and group_vars to organize device-specific and group-specific variables
- **Objective 4** – Create Jinja2 templates to dynamically generate network configurations 
- **Objective 5** – Build Ansible playbooks that configure VLANs and loopback interfaces using structured data
- **Objective 6** – Develop a backup playbook that saves device configurations locally
- **Objective 7** – Apply Infrastructure as Code principles for scalable network automation

These objectives build foundational skills for aspiring **network engineers** and **infrastructure specialists**.

---

## Tools & Technologies
You will use:
- **Development Environment**
    - Visual Studio Code + Dev Containers extension
    - Git & GitHub Classroom repository
    - Linux CLI (zsh)
- **Automation & IaC**
    - Ansible 
    - Jinja2 templating engine
    - YAML configuration files
- **Language & Libraries**
    - Python 3.x (for custom modules if needed)
    - ansible-core
    - cisco.ios collection
- **Target Devices**
    - Cisco DevNet Always-On Sandbox - Cisco Catalyst 8k or 9k
    - SSH/NETCONF connectivity

---

## Prerequisites
Before starting, make sure you:
- **Linux CLI basics**: navigating directories, running commands, editing files
- **Git & GitHub fundamentals**: clone, commit, push, pull requests
- **YAML syntax**: understanding of YAML structure and formatting
- **Networking concepts**: VLANs, loopback interfaces, SSH, IP addressing
- **Basic Ansible knowledge**: familiarity with playbooks, tasks, and modules (from lecture/reading)

---

## Deliverables
Commit and push the following to your Classroom repo:

### 1) Ansible Configuration Files
- `ansible.cfg` - Ansible configuration file with appropriate settings
- `inventory.yml` - Inventory file defining target devices and groups

### 2) Variable Files
- `group_vars/all.yml` - Global variables for all devices
- `group_vars/routers.yml` - Variables specific to router group
- `host_vars/router1.yml` - Variables specific to individual router

### 3) Jinja2 Templates (in `templates/`)
- `templates/vlans.j2` - Template for VLAN configuration
- `templates/loopbacks.j2` - Template for loopback interface configuration

### 4) Ansible Playbooks (in `playbooks/`)
- `playbooks/test_connectivity.yml` - Basic connectivity and facts gathering
- `playbooks/configure_vlans.yml` - Deploy VLAN configurations
- `playbooks/configure_loopbacks.yml` - Deploy loopback configurations  
- `playbooks/backup_config.yml` - Backup device configurations

### 5) Generated Files (in `backups/`)
- `backups/router1_config_YYYYMMDD_HHMMSS.txt` - Timestamped device backup
- `backups/backup_log.txt` - Log of backup operations

### 6) Logs (in `logs/`)
- `logs/ansible_test.log` - Contains connectivity test results
- `logs/vlan_deployment.log` - VLAN configuration deployment logs
- `logs/loopback_deployment.log` - Loopback configuration deployment logs
- `logs/backup_operations.log` - Backup operation logs

> ⚠️ **Important:** Autograding will validate file presence, YAML syntax, successful playbook execution, and backup file generation. Do not rename deliverables. Details on point awards located in the Grading section.

---

## Logging Requirements
Include the following logging function in any custom scripts:

```python
from datetime import datetime, timezone
import os

def log_ansible_operation(message, log_file):
    """Log ansible operations with timestamp"""
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {message}\n")

# Usage examples:
# log_ansible_operation("ANSIBLE_START", "logs/ansible_test.log")
# log_ansible_operation("INVENTORY_LOADED devices=2", "logs/ansible_test.log")
```

---

## Overview
In this lab, you will transition from script-based automation to **Infrastructure as Code (IaC)** using Ansible. You'll learn how to organize network automation using Ansible's structured approach: inventories, variables, templates, and playbooks. 

You'll start by setting up connectivity to DevNet sandbox devices, then progress through creating reusable configurations for VLANs and loopback interfaces using Jinja2 templates. Finally, you'll implement a backup solution that demonstrates how IaC principles apply to operational tasks.

💡 **Why this matters:** Ansible represents the industry standard for configuration management and Infrastructure as Code. Unlike one-off scripts, Ansible provides idempotent, scalable, and version-controlled automation that can manage thousands of devices consistently. This lab builds the foundation for enterprise-grade network automation.

---

## Instructions

Follow these steps in order:

### Step 1 – Clone Repository and Setup Environment
**What you're doing:** Setting up your development environment with all necessary dependencies.

```bash
git clone <your-repo-url>
cd Lab-7-Infrastructure-as-Code-with-Ansible
```

**Log Requirements:**
```bash
echo "$(date -Iseconds) - LAB7_START" >> logs/setup.log
```

**Done when:**
- You're in the lab directory
- `git status` shows clean working directory
- `logs/setup.log` contains LAB7_START entry

### Step 2 – Open Dev Container and Verify Environment
**What you're doing:** Launching the preconfigured development environment with Ansible and dependencies.

1. Launch VS Code in the repository directory
2. When prompted, choose "Reopen in Container" 
3. Wait for container build and dependency installation

**Verify installation:**
```bash
# Check Ansible installation
ansible --version
ansible-galaxy collection list | grep cisco.ios

# Test Python dependencies
python -c "import yaml, jinja2; print('Dependencies OK')"

# Log environment status
echo "$(date -Iseconds) - DEVCONTAINER_READY ansible=$(ansible --version | head -1)" >> logs/setup.log
```

**Done when:**
- Container is running without errors
- Ansible version 2.14+ is installed
- `cisco.ios` collection is available
- `logs/setup.log` shows DEVCONTAINER_READY

### Step 3 – Identify Target Device and Create Basic Inventory
**What you're doing:** Setting up your Ansible inventory to manage DevNet sandbox devices.

1. **Identify your target device:**
   - Visit Cisco DevNet Always-On Sandbox
   - Choose either Catalyst 8000V or 9000 device
   - Note the hostname/IP, SSH port, username, and password

2. **Test connectivity manually:**
```bash
# Replace with your sandbox details
ssh admin@sandbox-iosxe-latest-1.cisco.com
```

3. **Create Ansible configuration:**
Create `ansible.cfg`:
```ini
[defaults]
inventory = ./inventory.yml
host_key_checking = False
timeout = 30
stdout_callback = yaml
log_path = ./logs/ansible.log

[ssh_connection]
ssh_args = -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no
```

4. **Create basic inventory:**
Create `inventory.yml`:
```yaml
all:
  children:
    routers:
      hosts:
        router1:
          ansible_host: sandbox-iosxe-latest-1.cisco.com
          ansible_user: admin
          ansible_password: C1sco12345
          ansible_network_os: ios
          ansible_connection: network_cli
```

**Test your inventory:**
```bash
ansible-inventory --list
ansible all -m ping
```

**Log Requirements:**
```bash
echo "$(date -Iseconds) - INVENTORY_CREATED devices=$(ansible-inventory --list | grep -c ansible_host)" >> logs/ansible_test.log
```

**Done when:**
- `ansible.cfg` and `inventory.yml` exist
- `ansible all -m ping` succeeds
- `logs/ansible_test.log` shows INVENTORY_CREATED

### Step 4 – Test Connectivity and Gather Facts
**What you're doing:** Verifying Ansible can connect to devices and collect information.

Create `playbooks/test_connectivity.yml`:
```yaml
---
- name: Test Connectivity and Gather Facts
  hosts: all
  gather_facts: yes
  
  tasks:
    - name: Test reachability with ping
      ansible.builtin.ping:
      register: ping_result
      
    - name: Gather device facts
      cisco.ios.ios_facts:
        gather_subset: all
      register: device_facts
      
    - name: Display basic device information
      ansible.builtin.debug:
        msg: 
          - "Device: {{ inventory_hostname }}"
          - "Hostname: {{ ansible_facts.net_hostname | default('Unknown') }}"
          - "Model: {{ ansible_facts.net_model | default('Unknown') }}"
          - "Version: {{ ansible_facts.net_version | default('Unknown') }}"
          
    - name: Log connectivity test results
      ansible.builtin.lineinfile:
        path: ./logs/ansible_test.log
        line: "{{ ansible_date_time.iso8601 }} - CONNECTIVITY_TEST host={{ inventory_hostname }} status=SUCCESS model={{ ansible_facts.net_model | default('Unknown') }}"
        create: yes
```

**Run the playbook:**
```bash
ansible-playbook playbooks/test_connectivity.yml
```

**Done when:**
- Playbook runs successfully
- Device facts are displayed
- `logs/ansible_test.log` shows CONNECTIVITY_TEST entries

### Step 5 – Create Variable Structure (group_vars and host_vars)
**What you're doing:** Organizing device configuration data using Ansible's variable hierarchy.

1. **Create global variables:**
Create `group_vars/all.yml`:
```yaml
---
# Global variables for all devices
ntp_servers:
  - 64.6.64.6
  - 129.6.15.28

dns_servers:
  - 8.8.8.8
  - 8.8.4.4

snmp_community: lab_readonly

# Default VLANs for all devices
default_vlans:
  - { id: 10, name: "Management" }
  - { id: 20, name: "Users" }
  - { id: 30, name: "Servers" }
```

2. **Create router group variables:**
Create `group_vars/routers.yml`:
```yaml
---
# Variables specific to router group
router_vlans:
  - { id: 100, name: "WAN_Transit" }
  - { id: 101, name: "MPLS_VPN" }
  - { id: 102, name: "Internet_Edge" }

# Standard loopbacks for routers
standard_loopbacks:
  - { id: 0, ip: "10.0.0.1", mask: "255.255.255.255", description: "Router_ID" }
  - { id: 100, ip: "192.168.100.1", mask: "255.255.255.255", description: "Management" }
```

3. **Create host-specific variables:**
Create `host_vars/router1.yml`:
```yaml
---
# Variables specific to router1
device_hostname: "LAB-RTR-01"

# Host-specific loopbacks
custom_loopbacks:
  - { id: 1, ip: "10.1.1.1", mask: "255.255.255.255", description: "BGP_RouterID" }
  - { id: 2, ip: "10.1.2.1", mask: "255.255.255.255", description: "OSPF_RouterID" }
  - { id: 3, ip: "10.1.3.1", mask: "255.255.255.255", description: "Lab_Testing" }

# Host-specific VLANs
host_vlans:
  - { id: 200, name: "Lab_VLAN_1" }
  - { id: 201, name: "Lab_VLAN_2" }
  - { id: 202, name: "Lab_VLAN_3" }
```

**Test variable loading:**
```bash
ansible-inventory --host router1
ansible router1 -m debug -a "var=hostvars[inventory_hostname]"
```

**Log Requirements:**
```bash
echo "$(date -Iseconds) - VARIABLES_CREATED group_vars=3 host_vars=1" >> logs/ansible_test.log
```

**Done when:**
- All variable files exist with correct YAML syntax
- Variables can be accessed by inventory hostname
- `logs/ansible_test.log` shows VARIABLES_CREATED

### Step 6 – Create Jinja2 Templates
**What you're doing:** Building reusable configuration templates that incorporate your variables.

1. **Create VLAN template:**
Create `templates/vlans.j2`:
```jinja2
!
! VLAN Configuration Generated by Ansible
! Timestamp: {{ ansible_date_time.iso8601 }}
! Device: {{ inventory_hostname }}
!
{% if default_vlans is defined %}
! Default VLANs (from group_vars/all.yml)
{% for vlan in default_vlans %}
vlan {{ vlan.id }}
 name {{ vlan.name }}
{% endfor %}
{% endif %}

{% if router_vlans is defined %}
! Router Group VLANs (from group_vars/routers.yml)
{% for vlan in router_vlans %}
vlan {{ vlan.id }}
 name {{ vlan.name }}
{% endfor %}
{% endif %}

{% if host_vlans is defined %}
! Host-Specific VLANs (from host_vars/{{ inventory_hostname }}.yml)
{% for vlan in host_vlans %}
vlan {{ vlan.id }}
 name {{ vlan.name }}
{% endfor %}
{% endif %}
!
```

2. **Create Loopback template:**
Create `templates/loopbacks.j2`:
```jinja2
!
! Loopback Interface Configuration Generated by Ansible
! Timestamp: {{ ansible_date_time.iso8601 }}
! Device: {{ inventory_hostname }}
!
{% if standard_loopbacks is defined %}
! Standard Loopbacks (from group_vars/routers.yml)
{% for loopback in standard_loopbacks %}
interface Loopback{{ loopback.id }}
 description {{ loopback.description }}
 ip address {{ loopback.ip }} {{ loopback.mask }}
 no shutdown
{% endfor %}
{% endif %}

{% if custom_loopbacks is defined %}  
! Custom Loopbacks (from host_vars/{{ inventory_hostname }}.yml)
{% for loopback in custom_loopbacks %}
interface Loopback{{ loopback.id }}
 description {{ loopback.description }}
 ip address {{ loopback.ip }} {{ loopback.mask }}
 no shutdown
{% endfor %}
{% endif %}
!
```

**Test template rendering:**
```bash
# Create a quick test playbook to verify templates
cat > test_templates.yml << 'EOF'
---
- hosts: router1
  tasks:
    - name: Test VLAN template
      template:
        src: templates/vlans.j2
        dest: ./test_vlan_output.txt
        
    - name: Test Loopback template  
      template:
        src: templates/loopbacks.j2
        dest: ./test_loopback_output.txt
EOF

ansible-playbook test_templates.yml
cat test_vlan_output.txt
cat test_loopback_output.txt
```

**Done when:**
- Both templates exist and render without errors
- Generated configurations show data from different variable scopes
- Template syntax is valid Jinja2

### Step 7 – Deploy VLAN Configuration
**What you're doing:** Creating and running a playbook that configures VLANs using your template.

Create `playbooks/configure_vlans.yml`:
```yaml
---
- name: Configure VLANs from Template
  hosts: routers
  gather_facts: yes
  
  tasks:
    - name: Generate VLAN configuration from template
      ansible.builtin.template:
        src: ../templates/vlans.j2
        dest: ./configs/{{ inventory_hostname }}_vlans.cfg
      delegate_to: localhost
      
    - name: Display generated VLAN configuration
      ansible.builtin.debug:
        msg: "VLAN configuration generated for {{ inventory_hostname }}"
        
    - name: Apply VLAN configuration to device
      cisco.ios.ios_config:
        src: ./configs/{{ inventory_hostname }}_vlans.cfg
        backup: yes
        backup_options:
          filename: "{{ inventory_hostname }}_pre_vlan_backup.cfg"
          dir_path: ./backups/
      register: vlan_result
      
    - name: Verify VLAN creation
      cisco.ios.ios_command:
        commands:
          - show vlan brief
      register: vlan_verification
      
    - name: Display VLAN verification
      ansible.builtin.debug:
        var: vlan_verification.stdout_lines
        
    - name: Log VLAN deployment
      ansible.builtin.lineinfile:
        path: ./logs/vlan_deployment.log
        line: "{{ ansible_date_time.iso8601 }} - VLAN_DEPLOYED host={{ inventory_hostname }} vlans_configured={{ (default_vlans | length) + (router_vlans | default([]) | length) + (host_vlans | default([]) | length) }}"
        create: yes
      delegate_to: localhost
```

**Create configs directory and run playbook:**
```bash
mkdir -p configs backups
ansible-playbook playbooks/configure_vlans.yml
```

**Verification:**
```bash
# Check generated config
cat configs/router1_vlans.cfg

# Verify on device
ansible router1 -m cisco.ios.ios_command -a "commands='show vlan brief'"
```

**Done when:**
- VLAN configuration is generated and applied
- Device shows new VLANs in `show vlan brief`
- `logs/vlan_deployment.log` shows successful deployment

### Step 8 – Deploy Loopback Configuration  
**What you're doing:** Applying loopback interface configurations using structured data and templates.

Create `playbooks/configure_loopbacks.yml`:
```yaml
---
- name: Configure Loopback Interfaces from Template
  hosts: routers
  gather_facts: yes
  
  tasks:
    - name: Generate loopback configuration from template
      ansible.builtin.template:
        src: ../templates/loopbacks.j2
        dest: ./configs/{{ inventory_hostname }}_loopbacks.cfg
      delegate_to: localhost
      
    - name: Display generated loopback configuration
      ansible.builtin.debug:
        msg: "Loopback configuration generated for {{ inventory_hostname }}"
        
    - name: Apply loopback configuration to device
      cisco.ios.ios_config:
        src: ./configs/{{ inventory_hostname }}_loopbacks.cfg
        backup: yes
        backup_options:
          filename: "{{ inventory_hostname }}_pre_loopback_backup.cfg"
          dir_path: ./backups/
      register: loopback_result
      
    - name: Verify loopback interfaces
      cisco.ios.ios_command:
        commands:
          - show ip interface brief | include Loopback
      register: loopback_verification
      
    - name: Display loopback verification
      ansible.builtin.debug:
        var: loopback_verification.stdout_lines
        
    - name: Count configured loopbacks
      ansible.builtin.set_fact:
        total_loopbacks: "{{ (standard_loopbacks | default([]) | length) + (custom_loopbacks | default([]) | length) }}"
        
    - name: Log loopback deployment
      ansible.builtin.lineinfile:
        path: ./logs/loopback_deployment.log
        line: "{{ ansible_date_time.iso8601 }} - LOOPBACK_DEPLOYED host={{ inventory_hostname }} interfaces_configured={{ total_loopbacks }}"
        create: yes
      delegate_to: localhost
```

**Run the playbook:**
```bash
ansible-playbook playbooks/configure_loopbacks.yml
```

**Verification:**
```bash
# Check generated config
cat configs/router1_loopbacks.cfg

# Verify interfaces on device
ansible router1 -m cisco.ios.ios_command -a "commands='show ip interface brief | include Loopback'"
```

**Done when:**
- Loopback configuration is generated and applied successfully
- Device shows new loopback interfaces
- `logs/loopback_deployment.log` shows successful deployment

### Step 9 – Create Backup Playbook
**What you're doing:** Implementing a backup solution that saves device configurations with timestamps.

Create `playbooks/backup_config.yml`:
```yaml
---
- name: Backup Device Configurations
  hosts: all
  gather_facts: yes
  
  vars:
    backup_timestamp: "{{ ansible_date_time.year }}{{ ansible_date_time.month }}{{ ansible_date_time.day }}_{{ ansible_date_time.hour }}{{ ansible_date_time.minute }}{{ ansible_date_time.second }}"
    
  tasks:
    - name: Create backup directory
      ansible.builtin.file:
        path: ./backups
        state: directory
      delegate_to: localhost
      run_once: true
      
    - name: Backup running configuration
      cisco.ios.ios_config:
        backup: yes
        backup_options:
          filename: "{{ inventory_hostname }}_config_{{ backup_timestamp }}.txt"
          dir_path: ./backups/
      register: backup_result
      
    - name: Get device facts for backup log
      cisco.ios.ios_facts:
        gather_subset: hardware
      register: device_info
      
    - name: Log backup operation
      ansible.builtin.lineinfile:
        path: ./logs/backup_operations.log
        line: "{{ ansible_date_time.iso8601 }} - BACKUP_CREATED host={{ inventory_hostname }} file={{ inventory_hostname }}_config_{{ backup_timestamp }}.txt size={{ backup_result.backup_path | filesize if backup_result.backup_path is defined else 'unknown' }}"
        create: yes
      delegate_to: localhost
      
    - name: Update backup log summary
      ansible.builtin.lineinfile:
        path: ./backups/backup_log.txt
        line: "{{ ansible_date_time.iso8601 }} - {{ inventory_hostname }} - {{ inventory_hostname }}_config_{{ backup_timestamp }}.txt - {{ ansible_facts.net_model | default('Unknown') }}"
        create: yes
      delegate_to: localhost
      
    - name: Display backup confirmation
      ansible.builtin.debug:
        msg: 
          - "Backup completed for {{ inventory_hostname }}"
          - "File: {{ inventory_hostname }}_config_{{ backup_timestamp }}.txt"
          - "Model: {{ ansible_facts.net_model | default('Unknown') }}"
```

**Run backup playbook:**
```bash
ansible-playbook playbooks/backup_config.yml
```

**Verify backups:**
```bash
ls -la backups/
cat backups/backup_log.txt
```

**Done when:**
- Backup files are created with timestamp
- `backups/backup_log.txt` contains backup entries
- `logs/backup_operations.log` shows BACKUP_CREATED entries

### Step 10 – Final Testing and Documentation
**What you're doing:** Running comprehensive tests and documenting your IaC implementation.

1. **Run all playbooks in sequence:**
```bash
# Test connectivity
ansible-playbook playbooks/test_connectivity.yml

# Deploy configurations  
ansible-playbook playbooks/configure_vlans.yml
ansible-playbook playbooks/configure_loopbacks.yml

# Create backup
ansible-playbook playbooks/backup_config.yml
```

2. **Create a master playbook:**
Create `playbooks/deploy_all.yml`:
```yaml
---
- import_playbook: test_connectivity.yml
- import_playbook: configure_vlans.yml  
- import_playbook: configure_loopbacks.yml
- import_playbook: backup_config.yml
```

3. **Final verification:**
```bash
# Run master playbook
ansible-playbook playbooks/deploy_all.yml

# Verify final state
ansible all -m cisco.ios.ios_command -a "commands='show vlan brief'"
ansible all -m cisco.ios.ios_command -a "commands='show ip interface brief | include Loopback'"
```

4. **Create final log entry:**
```bash
echo "$(date -Iseconds) - LAB7_COMPLETE all_playbooks=4 backups=$(ls backups/*.txt | wc -l) templates=2" >> logs/final_status.log
```

**Done when:**
- All playbooks run successfully
- Device configurations match template outputs
- Backup files exist with proper timestamps
- All log files contain required entries

### Step 11 – Commit and Submit
**What you're doing:** Finalizing your work and submitting to GitHub Classroom.

```bash
# Add all files
git add .

# Commit with descriptive message
git commit -m "Lab 7 Complete: Ansible IaC with VLANs, Loopbacks, and Backups

- Created inventory and ansible.cfg
- Implemented group_vars and host_vars structure
- Built Jinja2 templates for VLANs and loopbacks  
- Deployed configurations using playbooks
- Created automated backup solution
- Generated all required logs and verification files"

# Push to GitHub
git push origin main
```

**Final verification:**
1. Check GitHub repository for all required files
2. Verify GitHub Actions (if configured) pass
3. Ensure all deliverables are present

**Done when:**
- Repository contains all required files and directories
- Commit history shows your work progression
- All playbooks are functional and tested

---

## :wrench: Troubleshooting & Common Pitfalls

### 1. **Ansible Connection Issues**
- **Symptom:** `UNREACHABLE` or `SSH authentication failed`
- **Fix:** 
  - Verify device credentials in inventory
  - Test manual SSH connection first
  - Check `ansible.cfg` for correct connection settings
  - Ensure `host_key_checking = False` is set

### 2. **YAML Syntax Errors**
- **Symptom:** `yaml: scanner error` or playbook parsing fails
- **Fix:**
  - Use consistent indentation (spaces, not tabs)
  - Validate YAML syntax: `yamllint inventory.yml`
  - Check quotes and special characters in strings

### 3. **Template Rendering Issues**
- **Symptom:** Variables not appearing in generated configs
- **Fix:**
  - Verify variable scope (group_vars vs host_vars)
  - Test with `ansible-inventory --host hostname`
  - Check Jinja2 syntax in templates
  - Use `debug` module to inspect variables

### 4. **Module Not Found Errors**
- **Symptom:** `cisco.ios.ios_config is not a module`
- **Fix:**
  - Install cisco collection: `ansible-galaxy collection install cisco.ios`
  - Verify collection installation: `ansible-galaxy collection list`
  - Check requirements.txt includes cisco.ios

### 5. **Permission Denied on Device**
- **Symptom:** `Authorization failed` when applying configurations
- **Fix:**
  - Ensure user has appropriate privileges
  - Use `ansible_become: yes` if needed
  - Verify device supports configuration mode access

### 6. **File Path Issues**
- **Symptom:** `template not found` or `file not found`
- **Fix:**
  - Use relative paths from playbook location
  - Verify directory structure matches instructions
  - Check file permissions and existence

---

## :bulb: Pro Tips

### **Variable Precedence Mastery**
```bash
# Test variable precedence
ansible-playbook -e "test_var=command_line" playbook.yml
# Order: command line > host_vars > group_vars > all
```

### **Template Testing**
```bash
# Quick template test without applying to device
ansible-playbook --check --diff playbooks/configure_vlans.yml
```

### **Inventory Management**
```bash
# Dynamic inventory verification
ansible-inventory --graph
ansible-inventory --host router1 --yaml
```

### **Backup Automation**
```yaml
# Add to crontab for scheduled backups
- name: Schedule daily backups
  cron:
    name: "Daily config backup"
    hour: "2"
    minute: "0"
    job: "cd {{ ansible_env.PWD }} && ansible-playbook playbooks/backup_config.yml"
```

### **Error Handling**
```yaml
# Add to playbooks for better error handling
  handlers:
    - name: Cleanup on failure
      file:
        path: ./configs/{{ inventory_hostname }}_failed.cfg
        state: absent
      listen: "config failed"
```

### **Variable Validation**
```yaml
# Validate required variables exist
- name: Validate required variables
  assert:
    that:
      - device_hostname is defined
      - custom_loopbacks is defined
    fail_msg: "Required variables not found in host_vars"
```

---

## Grading and Points Breakdown

> **ZERO CREDIT CONDITIONS:**
> - Missing `ansible.cfg` or `inventory.yml` files (0 pts for entire lab)
> - Playbooks fail to execute due to syntax errors (-50% total points)
> - No backup files generated (-20 pts)
> - Hard-coded credentials in any file (-10 pts)

| Step | Requirement | Points |
|------|-------------|--------|
| **Environment Setup** | Dev container functional, Ansible installed | 8 |
| **Inventory & Config** | Valid `ansible.cfg` and `inventory.yml` files | 10 |
| **Connectivity Testing** | Successful ping and facts gathering | 10 |
| **Variable Structure** | Proper `group_vars/` and `host_vars/` organization | 12 |
| **Jinja2 Templates** | Working VLAN and loopback templates | 15 |
| **VLAN Deployment** | Successful VLAN configuration via playbook | 12 |
| **Loopback Deployment** | Successful loopback configuration via playbook | 12 |
| **Backup Implementation** | Working backup playbook with timestamped files | 15 |
| **Logging & Documentation** | All required log entries and file structure | 8 |
| **Code Quality** | Clean YAML, proper Git commits, error handling | 8 |

**Bonus Points (up to +10):**
- Advanced Jinja2 features (conditionals, loops, filters)
- Custom Ansible modules or roles
- Comprehensive error handling and rollback procedures
- Integration with external systems (monitoring, ticketing)

**Total: 110 points (100 base + 10 bonus)**

---

## Submission Checklist

### :green_checkmark: **Files & Structure**
- [ ] `ansible.cfg` configured correctly
- [ ] `inventory.yml` with valid device entries
- [ ] `group_vars/all.yml` and `group_vars/routers.yml`
- [ ] `host_vars/router1.yml` with device-specific variables
- [ ] `templates/vlans.j2` and `templates/loopbacks.j2`
- [ ] All 4 playbooks in `playbooks/` directory
- [ ] Backup files in `backups/` with timestamps
- [ ] Complete log files in `logs/` directory

### :green_checkmark: **Functionality**  
- [ ] All playbooks execute without errors
- [ ] Device shows configured VLANs and loopbacks
- [ ] Backup files contain actual device configurations
- [ ] Templates generate valid device configurations

### :green_checkmark: **Git & Submission**
- [ ] All files committed and pushed to GitHub
- [ ] Commit messages are descriptive and professional
- [ ] Repository structure matches requirements
- [ ] No credentials or secrets in version control

**Final Check:** Run `ansible-playbook playbooks/deploy_all.yml` one final time to ensure everything works end-to-end before submission.