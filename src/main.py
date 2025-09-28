# Lab 7 Infrastructure as Code with Ansible - Starter File

"""
This is a starter file for students who want to create custom Ansible modules
or helper scripts for their automation tasks.

Example usage:
- Custom fact gathering
- Configuration validation
- Advanced logging functions
- Integration with external APIs
"""

from datetime import datetime, timezone
import os
import yaml
import json

def log_ansible_operation(message, log_file):
    """
    Log ansible operations with timestamp
    
    Args:
        message (str): Log message to write
        log_file (str): Path to log file
    """
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {message}\n")

def validate_yaml_file(file_path):
    """
    Validate YAML syntax in a file
    
    Args:
        file_path (str): Path to YAML file to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)
    except FileNotFoundError:
        return False, f"File not found: {file_path}"

def load_inventory_vars(inventory_file):
    """
    Load and return variables from inventory file
    
    Args:
        inventory_file (str): Path to inventory YAML file
        
    Returns:
        dict: Parsed inventory data
    """
    try:
        with open(inventory_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return {}

if __name__ == "__main__":
    # Example usage
    print("Ansible Lab 7 - Infrastructure as Code Helper Functions")
    
    # Test logging
    log_ansible_operation("LAB7_HELPER_START", "logs/helper.log")
    
    # Test YAML validation
    test_files = ["inventory.yml", "group_vars/all.yml", "host_vars/router1.yml"]
    for file_path in test_files:
        if os.path.exists(file_path):
            valid, error = validate_yaml_file(file_path)
            status = "VALID" if valid else f"INVALID - {error}"
            log_ansible_operation(f"YAML_VALIDATION file={file_path} status={status}", "logs/helper.log")
            print(f"{file_path}: {status}")
    
    log_ansible_operation("LAB7_HELPER_END", "logs/helper.log")
