import yaml
import subprocess
import os
import argparse
from jinja2 import Environment, FileSystemLoader

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_terraform_files(data, template_dir='templates/terraform', output_dir='terraform'):
    env = Environment(loader=FileSystemLoader(template_dir))
    if 's3_buckets' in data:
        template = env.get_template('s3.tf.j2')
        rendered_content = template.render({'s3_buckets': data['s3_buckets']})
        with open(os.path.join(output_dir, "s3.tf"), 'w') as f:
            f.write(rendered_content)
    # VPC
    if 'vpc' in data:
        template = env.get_template('vpc.tf.j2')
        rendered_content = template.render({'vpc': data['vpc']})
        with open(os.path.join(output_dir, "vpc.tf"), 'w') as f:
            f.write(rendered_content)

    # IAM
    if 'iam' in data:
        template = env.get_template('iam.tf.j2')
        rendered_content = template.render({'iam': data['iam']})
        with open(os.path.join(output_dir, "iam.tf"), 'w') as f:
            f.write(rendered_content)

    # EC2 Instances
    if 'ec2_instances' in data:
        template = env.get_template('ec2.tf.j2')
        rendered_content = template.render({'ec2_instances': data['ec2_instances']})
        with open(os.path.join(output_dir, "ec2.tf"), 'w') as f:
            f.write(rendered_content)         
            
    # Subnets
    if 'subnets' in data:
        template = env.get_template('subnet.tf.j2')
        rendered_content = template.render({'subnets': data['subnets']})
        with open(os.path.join(output_dir, "subnets.tf"), 'w') as f:
            f.write(rendered_content)
    print("Terraform files generated.")

def apply_terraform(output_dir='terraform'):
    subprocess.run(["terraform", "init"], cwd=output_dir)
    subprocess.run(["terraform", "apply", "-auto-approve"], cwd=output_dir)

def generate_ansible_playbooks(data, template_dir='templates/ansible', output_dir='ansible'):
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

def generate_kubernetes_files(data, template_dir='templates/kubernetes', output_dir='kubernetes'):
    env = Environment(loader=FileSystemLoader(template_dir))

    # Deployments
    if 'deployments' in data:
        template = env.get_template('deployment.yaml.j2')
        for deployment in data['deployments']:
            rendered_content = template.render({'deployment': deployment})
            with open(os.path.join(output_dir, f"{deployment['name']}_deployment.yaml"), 'w') as f:
                f.write(rendered_content)

    # Services
    if 'services' in data:
        template = env.get_template('service.yaml.j2')
        for service in data['services']:
            rendered_content = template.render({'service': service})
            with open(os.path.join(output_dir, f"{service['name']}_service.yaml"), 'w') as f:
                f.write(rendered_content)

    # Ingress
    if 'ingress' in data:
        template = env.get_template('ingress.yaml.j2')
        for ingress in data['ingress']:
            rendered_content = template.render({'ingress': ingress})
            with open(os.path.join(output_dir, f"{ingress['name']}_ingress.yaml"), 'w') as f:
                f.write(rendered_content)

    print("Kubernetes configuration files generated.")

def apply_kubernetes_configs(output_dir='kubernetes'):
    for file in os.listdir(output_dir):
        if file.endswith(".yaml") or file.endswith(".yml"):
            subprocess.run(["kubectl", "apply", "-f", os.path.join(output_dir, file)])
def main():
    parser = argparse.ArgumentParser(description="Infrastructure Automation Script")
    parser.add_argument("--config", required=True, help="Path to the infra_setup.yaml file")
    parser.add_argument("--terraform-dir", default="terraform", help="Directory to store Terraform files")
    parser.add_argument("--ansible-dir", default="ansible", help="Directory to store Ansible playbooks")
    parser.add_argument("--kubernetes-dir", default="kubernetes", help="Directory to store Kubernetes configurations")
    parser.add_argument("--apply-terraform", action="store_true", help="Apply Terraform scripts")
    parser.add_argument("--apply-ansible", action="store_true", help="Run Ansible playbooks")
    parser.add_argument("--apply-kubernetes", action="store_true", help="Apply Kubernetes configurations")
    parser.add_argument("--run-all", action="store_true", help="Run all steps: Terraform, Ansible, and Kubernetes")

    args = parser.parse_args()

    data = load_yaml(args.config)

    if args.run_all or args.apply_terraform:
        os.makedirs(args.terraform_dir, exist_ok=True)
        generate_terraform_files(data.get('terraform', {}), output_dir=args.terraform_dir)
        apply_terraform(output_dir=args.terraform_dir)

    if args.run_all or args.apply_ansible:
        os.makedirs(args.ansible_dir, exist_ok=True)
        generate_ansible_playbooks(data.get('ansible', {}), output_dir=args.ansible_dir)
        run_ansible_playbooks(output_dir=args.ansible_dir)

    if args.run_all or args.apply_kubernetes:
        os.makedirs(args.kubernetes_dir, exist_ok=True)
        generate_kubernetes_files(data.get('kubernetes', {}), output_dir=args.kubernetes_dir)
        apply_kubernetes_configs(output_dir=args.kubernetes_dir)

if __name__ == "__main__":
    main()