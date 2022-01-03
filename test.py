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
    server_user = conn_settings_list[f'{hostname}']['user']
    # password = conn_settings_list[f'{hostname}']['password']
    conn = Connection(host=conn_settings_list[f'{hostname}']['host'], 
        user=conn_settings_list[f'{hostname}']['user'], 
        port=conn_settings_list[f'{hostname}']['port'],
        config=Config(overrides={'sudo': {'password': conn_settings_list[f'{hostname}']['password']}}), 
        connect_kwargs={"password": conn_settings_list[f'{hostname}']['password']})
    # sudopass = Responder(pattern = r"\[sudo\]", response = f'{password}\n')
    #test = conn.sudo("-i ls")   #need to run -i to log in
    #TODO condition if file extension given
    try:
        conn.run('whoami', hide=True)
        result = conn.run(f'find -path \*{path}.* -prune')
        result_root = conn.sudo(f'-i find -path \*{path}.* -prune')
        result_dict = result_manipulator(result.stdout, result_root.stdout, server, server_user)
        print(result_dict)
    except Exception as e:
        print(e)

#multiple arguments
def multi_connection(path):
    result_dict = {}
    for key, val in conn_settings_list.items():
        server = conn_settings_list[f'{key}']['hostname']
        server_user = conn_settings_list[f'{key}']['user']
        conn = Connection(host=conn_settings_list[f'{key}']['host'], 
            user=conn_settings_list[f'{key}']['user'], 
            port=conn_settings_list[f'{key}']['port'],
            config=Config(overrides={'sudo': {'password': conn_settings_list[f'{key}']['password']}}),
            connect_kwargs={"password": conn_settings_list[f'{key}']['password']})
        try:
            conn.run('whoami')  #add hide=True
            result = conn.run(f'find -path \*{path}.* -prune')
            result_root = conn.sudo(f'-i find -path \*{path}.* -prune')
            result_dict[f'{key}'] = result_manipulator(result.stdout, result_root.stdout, server, server_user)
            if len(result_dict) > 0:
                result_dict = result_dict[f'{key}'].update(result_dict)
            print(result_dict)
        except Exception as e:
            print(e)

#one_connection('host1', 'file_test')
multi_connection('file_test')

# def result_manipulator(result, hostname):
#     list_paths = list(result.split(" "))
#     result_dict = dict({f'{hostname}': f'{list_paths}'})
#     return result_dict