# Lab 7 Infrastructure as Code with Ansible

## :triangular_flag_on_post: Learning Goals
- **Understand the purpose of Ansible** in network automation as an Infrastructure as Code (IaC) tool
- **Identify the core building blocks of Ansible projects**, including the configuration file (ansible.cfg), inventory files, host variables, and group variables
- **Explain how Ansible uses YAML syntax** to define playbooks, variables, and tasks
- **Use Jinja2 templates** to dynamically generate device configurations from variables
- **Differentiate between host-specific variables** (host_vars) and group-level variables (group_vars), and explain when to use each
- **Explore Ansible Galaxy** to discover, install, and leverage pre-built roles and collections for network automation
- **Run a simple Ansible playbook** to apply configurations to network devices or generate outputs from templates
- **Practice creating a Jinja2 template** that adds multiple loopback interfaces using values defined in both group_vars and host_vars
- **Reinforce best practices** in separating logic (playbooks) from data (variables) and templates for scalable, reusable automation

## :globe_with_meridians: Overview:
In this lab, you’ll be introduced to **Ansible**, one of the most widely used Infrastructure as Code (IaC) tools for network automation. Ansible allows you to define device configurations, automation tasks, and workflows in simple, human-readable YAML files, separating the logic of what you want to accomplish from the data that drives it. This structure makes automation scalable, repeatable, and easier to maintain than ad hoc scripts.

You’ll start by learning the core building blocks of an Ansible project: the configuration file (`ansible.cfg`), the inventory of devices you want to manage, and how to assign variables at the **host** and **group** levels. You’ll then explore how Ansible uses **Jinja2 templates** to dynamically generate configurations from those variables. Along the way, you’ll also see how **Ansible Galaxy** provides collections and roles to extend functionality with reusable, community-driven code. The lab will wrap up with a practical exercise where you create a Jinja2 template to add multiple loopback interfaces, once using group variables and once using host variables, reinforcing how different variable scopes drive configuration outcomes. By the end, you’ll understand the basic Ansible workflow and how it fits into modern network automation practices.

### What is Ansible and Why Use It?
Ansible is an **open-source automation tool** that simplifies the way you configure, manage, and orchestrate IT systems, including network devices. At its core, Ansible lets you describe what you want a system to look like—interfaces configured, services enabled, policies applied—in simple, human-readable YAML files called playbooks. Instead of manually applying changes device by device, Ansible executes those playbooks to enforce a consistent state across your infrastructure.

What makes Ansible especially powerful in networking is that it’s agentless—you don’t have to install software on your routers or switches. Ansible connects using existing protocols like SSH or HTTPS (for RESTCONF/NETCONF) and pushes configurations in a repeatable way. This means you can manage hundreds of devices the same way you’d manage one, with the added benefit of **version control, repeatability, and scalability**.

For students, Ansible represents a step up from the scripts you’ve been writing so far. While Python scripts let you experiment and automate one task at a time, Ansible gives you a **framework**: a standardized way to organize your automation with configuration files, variables, and templates. This approach is the foundation of **Infrastructure as Code (IaC)**—treating infrastructure definitions the same way developers treat software—making changes more predictable, collaborative, and easy to roll back if needed.

### Ansible Project Structure
Ansible organizes automation work into a simple but powerful directory layout. At the top level, you’ll usually find a few key files and folders that define how Ansible should behave, what devices it will manage, and what data it should use. A minimal project might look like this:

```python

ansible-project/
├── ansible.cfg        # Configuration file
├── inventory.yml      # List of hosts and groups
├── group_vars/        # Variables applied to groups of hosts
│   └── all.yml
├── host_vars/         # Variables applied to individual hosts
│   └── router1.yml
├── playbook.yml       # Defines the tasks Ansible should run
└── templates/         # Jinja2 templates for configurations
    └── loopbacks.j2

```

- `ansible.cfg` tells Ansible where to find things like the inventory and sets default behavior.

- `inventory.yml` lists your devices, often grouped (e.g., routers, switches).

- `group_vars/` and `host_vars/` hold YAML files with variables for groups or individual hosts.

- `playbook.yml` defines the automation tasks to execute.

- `templates/` contains Jinja2 templates for generating device configs.

This structure helps separate logic (playbooks and templates) from data (inventories and variables). By keeping things modular, you can reuse the same playbook with different inventories or templates, making your automation scalable and consistent.

### The Ansible Configuration File (`ansible.cfg`)
The `ansible.cfg` file is where you define default settings that control how Ansible behaves. While Ansible comes with global defaults, adding a local `ansible.cfg` to your project folder ensures that everyone running the project uses the same configuration. This makes labs, teamwork, and production automation more predictable.

A typical `ansible.cfg` might look like this:

```ini

[defaults]
inventory = ./inventory.yml
host_key_checking = False
retry_files_enabled = False
stdout_callback = yaml

```

- `inventory` tells Ansible where to find the list of hosts.

- `host_key_checking = False` disables SSH key prompts, which is convenient in labs.

- `retry_files_enabled = False` prevents clutter by turning off retry file generation.

- `stdout_callback = yaml` makes output more human-readable.

You can add many more options—like defining roles paths, collections paths, or privilege escalation behavior—but in most cases, a short config file is enough. By keeping this file in your project directory, you reduce friction for students: they don’t have to remember long commands or worry about inconsistent environments.

### The Inventory File
The inventory file is Ansible’s source of truth for which devices or servers it will manage. It defines the hosts you want to automate and organizes them into logical groups. Inventories can be written in INI format or YAML, but YAML is more common in modern projects because it’s easier to read and extend.

Here’s a simple YAML inventory example for a network lab:

```yaml

all:
  children:
    routers:
      hosts:
        router1:
          ansible_host: 192.168.1.10
        router2:
          ansible_host: 192.168.1.11
    switches:
      hosts:
        switch1:
          ansible_host: 192.168.1.20


```

In this structure:

- `all` is the top-level group that contains everything.

- `routers` and `switches` are sub-groups with their own hosts.

- Each host (like `router1`) is given a reachable IP via `ansible_host`.

An inventory can also include connection details, such as `ansible_user`, `ansible_password`, or platform-specific variables. By grouping devices, you can apply variables or tasks to many hosts at once—such as deploying a configuration template to every router in the `routers` group. This separation of hosts into groups makes Ansible powerful and scalable, even in small labs.

### Host Variables (`host_vars`)
While the inventory defines which devices Ansible will manage, sometimes you need to assign unique values to a specific host. That’s where host variables come in. Host variables are stored in the `host_vars/` directory, with one YAML file per host, named exactly the same as the host in the inventory. This lets Ansible automatically load the right variables for the right device.

Here’s an example:

```

ansible-project/
├── inventory.yml
├── host_vars/
│   └── router1.yml

```

`router1.yml`:

```yaml

hostname: R1
loopbacks:
  - { id: 1, ip: 10.1.1.1/32 }
  - { id: 2, ip: 10.1.2.1/32 }

```

In this case:

- The variables apply only to `router1`.

- You can define anything here—hostnames, interface lists, credentials, or feature toggles.

- Ansible automatically loads this file when running tasks against `router1`.

`host_vars` is especially useful when devices have small but important differences, like unique loopback addresses or hostnames. Instead of hardcoding these details into playbooks, you keep them cleanly separated, making the automation more reusable and easier to maintain.

### Group Variables (`group_vars`)
While host variables define values for individual devices, group variables let you assign common settings to an entire group of hosts at once. This avoids duplication and keeps your project clean when many devices share the same configuration values. Group variables are stored in the group_vars/ directory, and the file name matches the group name from your inventory.

Here’s an example:

```

ansible-project/
├── inventory.yml
├── group_vars/
│   └── routers.yml

```

`routers.yml`:

```yaml

ntp_servers:
  - 192.168.100.10
  - 192.168.100.11

loopbacks:
  - { id: 1, ip: 10.10.1.1/32 }
  - { id: 2, ip: 10.10.2.1/32 }

```

In this setup:

- All hosts in the `routers` group inherit the same `ntp_servers` and `loopbacks`.

- You can still override or add unique details with host_vars if needed.

- Group variables are perfect for defining shared services (like DNS or NTP), standard interface templates, or policies that apply to every device of a type.

By using `group_vars` alongside `host_vars`, you can strike a balance: keep common data centralized while allowing host-specific customization. This separation of concerns is what makes Ansible scalable in real-world automation projects.

### Using Jinja2 Templates in Ansible
Ansible uses Jinja2 templates to turn variables into dynamic configuration files. Instead of writing a static config for every device, you can create a single template that pulls in values from your `group_vars` and `host_vars`. This makes your automation reusable and ensures consistency across devices, while still allowing flexibility where needed.

Jinja2 templates live in the `templates/` directory of your project and usually have a `.j2` extension. They look a lot like normal configuration files, but with placeholders for variables wrapped in double curly braces `{{ }}`. For example:

```jinja

hostname {{ hostname }}

{% for loopback in loopbacks %}
interface Loopback{{ loopback.id }}
 ip address {{ loopback.ip }}
{% endfor %}

```

In this template:

- `{{ hostname }}` pulls the hostname variable from either `host_vars` or `group_vars`.

- The `{% for %}` loop creates multiple loopback interfaces based on a list of dictionaries.

When you run a playbook that references this template, Ansible fills in the values for each device and generates a complete, ready-to-deploy configuration. This approach separates data (variables) from logic (templates), which is a core principle of Infrastructure as Code. By mastering Jinja2 in Ansible, you can scale your automation from a single lab router to an entire production environment with minimal changes.

### Ansible Galaxy and Collections
Ansible isn’t just about what you write yourself—it also comes with a huge ecosystem of reusable content. That’s where Ansible Galaxy comes in. Galaxy is the community hub for sharing and downloading Ansible roles, collections, and modules that others have already built. Instead of reinventing the wheel, you can install these packages and immediately gain access to tasks, templates, and modules that solve common problems in networking and IT automation.

In modern Ansible, the primary unit of shared content is the collection. A collection is a bundle of roles, modules, and plugins organized together for a specific purpose. For example, Cisco provides collections like `cisco.ios` or `cisco.nxos` that contain modules to configure interfaces, routing, and system settings directly on their devices. Once installed, you can reference these modules in your playbooks just like built-in Ansible functionality.

Here’s an example of installing the Cisco IOS collection:

```bash

ansible-galaxy collection install cisco.ios

```

With this, you can immediately start using tasks like `ios_config` or `ios_command` without writing low-level code. By learning to leverage Ansible Galaxy, you gain two things: exposure to industry-grade modules and the ability to build on top of best practices from the community. This makes your automation projects faster to build, easier to maintain, and more aligned with real-world workflows.

---

## :card_file_box: File Structure:

'''
file structure
'''

---

## Components
text

### 1. **Component 1**
text

### 2. **Component 2**
text

### 3. **Component 3**
text

## :memo: Instructions
1. text
2. text
3. text

## :page_facing_up: Logging
text

## :green_checkmark: Grading Breakdown
- x pts: 
- x pts:
- x pts: