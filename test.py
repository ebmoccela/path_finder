from fabric import *
import yaml

with open("db_settings.yml", "r") as ymlfile:
    conn_settings_list = yaml.safe_load(ymlfile)

def result_manipulator(result, result_sudo, hostname, user):
    keys = [f'{user}@{hostname}', f'root@{hostname}']
    values = []
    if result != "":
        list_paths = list(result.strip().split("\n"))
        values.append(list_paths)
    if result != "":
        sudo_list_paths = list(result_sudo.strip().split("\n"))
        values.append(sudo_list_paths)

    if len(list_paths) > 0 and len(sudo_list_paths) > 0:
        results = dict(zip(keys, values))
        return results
    elif len(list_paths) > 0:
        results = dict({f'{user}@{hostname}': f'{list_paths}'})
        return results
    else:
        results = dict({f'root@{hostname}': f'{sudo_list_paths}'})
        return results

#one argument
def one_connection(hostname, path):
    # config = Config(overrides={'sudo': {'password': conn_settings_list[f'{hostname}']['password']}})
    server = conn_settings_list[f'{hostname}']['hostname']
    user = conn_settings_list[f'{hostname}']['user']
    # password = conn_settings_list[f'{hostname}']['password']
    conn = Connection(host=conn_settings_list[f'{hostname}']['host'], 
        user=conn_settings_list[f'{hostname}']['user'], 
        port=conn_settings_list[f'{hostname}']['port'],
        config=Config(overrides={'sudo': {'password': conn_settings_list[f'{hostname}']['password']}}), 
        connect_kwargs={"password": conn_settings_list[f'{hostname}']['password']})
    # sudopass = Responder(pattern = r"\[sudo\]", response = f'{password}\n')
    #test = conn.sudo("-i ls")   #need to run -i to log in
    #TODO condition if file extension given
    result = conn.run(f'find -path \*{path}.* -prune')
    result_root = conn.sudo(f'-i find -path \*{path}.* -prune')
    result_dict = result_manipulator(result.stdout, result_root.stdout, server, user)
    print(result_dict)

#multiple arguments
def multi_connection():
    for key, val in conn_settings_list.items():
        conn = Connection(host=val['host'], user=val['user'], port=val['port'], connect_kwargs={"password": val['password']})
        conn.run('whoami')
# sudo_pass = Config(overrides={'sudo': {'password': 'pizzatime'}})
# conn.run('ls', pty=True, watchers=[sudopass])

one_connection('host1', 'file_test')

# def result_manipulator(result, hostname):
#     list_paths = list(result.split(" "))
#     result_dict = dict({f'{hostname}': f'{list_paths}'})
#     return result_dict