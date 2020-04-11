from pick import pick
from environment import Environment

def select_env():
    title = "For what environment do we need a deployment ticket?"
    config = Environment.get_config()
    options = list(config['deployment_groups'].keys())

    return pick(options, title)
    

if __name__ == '__main__':
    user_selection = select_env()[0]
    if user_selection:
        env = Environment(user_selection)
        if(env.check_connection()):
            env.group_ticket_list()
            # todo: Add creation ticket handler here.
            pass
    else:
        print('Unexpected error. Shutting down')
        exit(1)