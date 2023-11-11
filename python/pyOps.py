import yaml
import subprocess
import os
from jinja2 import Environment, FileSystemLoader

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_terraform_files(data, template_dir='templates', output_dir='terraform'):
    env = Environment(loader=FileSystemLoader(template_dir))
    # Example: Generate Terraform files for S3
    if 's3_buckets' in data:
        template = env.get_template('s3.tf.j2')
        rendered_content = template.render({'s3_buckets': data['s3_buckets']})
        with open(os.path.join(output_dir, "s3.tf"), 'w') as f:
            f.write(rendered_content)
    # Add similar sections for other Terraform resources like VPC, EC2, etc.
    print("Terraform files generated.")

def apply_terraform(output_dir='terraform'):
    subprocess.run(["terraform", "init"], cwd=output_dir)
    subprocess.run(["terraform", "apply", "-auto-approve"], cwd=output_dir)

def generate_ansible_playbooks(data, template_dir='templates', output_dir='ansible'):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('playbook.yaml.j2')
    for playbook in data.get('playbooks', []):
        rendered_content = template.render(playbook)
        playbook_path = os.path.join(output_dir, f"{playbook['name']}_playbook.yaml")
        with open(playbook_path, 'w') as f:
            f.write(rendered_content)
    print("Ansible playbooks generated.")

def run_ansible_playbooks(output_dir='ansible'):
    for playbook in os.listdir(output_dir):
        if playbook.endswith(".yaml") or playbook.endswith(".yml"):
            subprocess.run(["ansible-playbook", os.path.join(output_dir, playbook)])

def generate_kubernetes_files(data, template_dir='templates', output_dir='kubernetes'):
    env = Environment(loader=FileSystemLoader(template_dir))
    # Example: Generate Kubernetes deployment files
    # Add similar sections for other Kubernetes resources like services, ingress, etc.
    print("Kubernetes files generated.")

def apply_kubernetes_configs(output_dir='kubernetes'):
    for file in os.listdir(output_dir):
        if file.endswith(".yaml") or file.endswith(".yml"):
            subprocess.run(["kubectl", "apply", "-f", os.path.join(output_dir, file)])

def main():
    data = load_yaml('infra_setup.yaml')

    # Generate and Apply Terraform Scripts
    os.makedirs('terraform', exist_ok=True)
    generate_terraform_files(data.get('terraform', {}))
    apply_terraform()

    # Generate and Run Ansible Playbooks
    os.makedirs('ansible', exist_ok=True)
    generate_ansible_playbooks(data.get('ansible', {}))
    run_ansible_playbooks()

    # Generate and Apply Kubernetes Configurations
    os.makedirs('kubernetes', exist_ok=True)
    generate_kubernetes_files(data.get('kubernetes', {}))
    apply_kubernetes_configs()

if __name__ == "__main__":
    main()
