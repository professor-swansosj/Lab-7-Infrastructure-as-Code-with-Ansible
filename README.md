# Lab 7 — Infrastructure as Code with Ansible

**Course:** Software Defined Networking  
**Module:** Network Automation Fundamentals • **Lab #:** 7  
**Estimated Time:** 120–150 minutes

## Objectives
- Create and configure Ansible inventories for network devices.
- Test connectivity and gather facts from Cisco devices (DevNet Always-On).
- Organize data with host_vars and group_vars for clean variable scope.
- Author Jinja2 templates to generate VLAN and loopback configs.
- Build playbooks to configure VLANs and loopbacks from structured data.
- Implement a backup playbook that saves device configurations locally.
- Apply Infrastructure as Code (IaC) principles for scalable network automation.

## Prerequisites
- Python 3.11 (via the provided dev container)
- Accounts: GitHub
- Devices/Sandboxes: Cisco DevNet Always-On Sandbox — Catalyst 8k or 9k (SSH/NETCONF)

## Overview
Move from script-based automation to **Infrastructure as Code** with Ansible. You’ll define a project with inventories, variables, templates, and playbooks; connect to a DevNet sandbox device; deploy VLANs and loopbacks via Jinja2; and implement a timestamped backup workflow. The result is idempotent, version-controlled automation you can scale and reuse.


## Resources
- [Ansible Documentation](https://docs.ansible.com/)- [Ansible Galaxy — cisco.ios](https://galaxy.ansible.com/cisco/ios)- [Jinja2 Templates](https://jinja.palletsprojects.com/)- [YAML Syntax (YAML.org)](https://yaml.org/spec/)- [Cisco DevNet Sandboxes](https://developer.cisco.com/site/sandbox/)

## FAQ
**Q:** Playbook fails with unreachable or SSH auth errors.  
**A:** Verify inventory credentials, test manual SSH first, and set host_key_checking False in ansible.cfg.

**Q:** YAML parsing errors on playbooks or vars.  
**A:** Use spaces (not tabs), quote strings with colons, and run `yamllint` locally.

**Q:** Templates render but variables are empty.  
**A:** Check variable scope and names; test with `ansible-inventory --host <name>` and `debug` tasks.

**Q:** Module `cisco.ios.ios_config` not found.  
**A:** Install the collection: `ansible-galaxy collection install cisco.ios` and verify with `ansible-galaxy collection list`.



## Deliverables
- Standardized README with objectives, overview, grading, and tips.
- Stepwise INSTRUCTIONS for inventory, templates, playbooks, backups, and logs.
- Grading: **100 points**

## Grading Breakdown
| Step | Requirement | Points |
|---|---|---|
| Environment Setup | Dev container functional; Ansible installed | 8 |
| Inventory & Config | Valid ansible.cfg and inventory.yml | 10 |
| Connectivity Testing | Ping + facts gathering succeed | 10 |
| Variable Structure | Correct group_vars and host_vars organization | 12 |
| Jinja2 Templates | Working VLAN and loopback templates | 15 |
| VLAN Deployment | VLAN configuration applied and verified | 12 |
| Loopback Deployment | Loopbacks applied and verified | 12 |
| Backup Implementation | Timestamped backups and logs | 15 |
| Logging & Docs | All required log entries and structure | 8 |
| Code Quality | Clean YAML, commits, and error handling | 8 |
| **Total** |  | **100** |

## 🔧 Troubleshooting & Pro Tips
**Inventory sanity**  
*Symptom:* Ping fails to all hosts  
*Fix:* Run `ansible-inventory --list` and confirm `ansible_host`, user, and connection vars.

**Template paths**  
*Symptom:* template not found  
*Fix:* Use paths relative to the playbook (`../templates/*.j2`) or set `template` task paths carefully.

**Privilege issues**  
*Symptom:* Auth failed when applying configs  
*Fix:* Ensure device user has privileges; set `ansible_become: yes` if needed.



## Autograder Notes
- Log file: `logs/*.log`
- Required markers: `LAB7_START`, `DEVCONTAINER_READY`, `INVENTORY_CREATED`, `CONNECTIVITY_TEST`, `VARIABLES_CREATED`, `VLAN_DEPLOYED`, `LOOPBACK_DEPLOYED`, `BACKUP_CREATED`, `LAB7_COMPLETE`

## License
© 2025 Your Name — Classroom use.

# HAPPY CODING!