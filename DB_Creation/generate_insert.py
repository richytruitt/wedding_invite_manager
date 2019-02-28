import os
from jinja2 import Environment, FileSystemLoader
import random

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape = False,
    loader = FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks = False
)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def create_insert():
    fname = "insert_invites.sql"
    id_list=[]
    
    with open ("./names.txt", "r") as name_file:
        for line in name_file:

            generated_id = random.randint(0, 9999999999)
        
            while (generated_id in id_list):
                print("Duplicate found, generating new number")
                generated_id = random.randint(0, 9999999999)
        
            id_list.append(generated_id)


            user_id = str(generated_id)

            firstname = line.split()[0]
            lastname = line.split()[1]
            stat = "No Status"
            invite = {
                'first_name': firstname,
                'last_name': lastname,
                'status': stat,
                'id': user_id
            }

            context = {
                'user': invite
            }

            with open (fname, 'a') as f:
                item = render_template('insert_users.jinja', context)
                f.write(item)
    print(id_list)


def main():
    create_insert()

if __name__ =="__main__":
    main()
