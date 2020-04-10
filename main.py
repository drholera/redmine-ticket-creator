from pick import pick
from environment import Environment

def select_env():
    title = "For what environment do we need a deployment ticket?"
    options = ["dev", "stage", "preprod", "prod",]

    return pick(options, title)
    

if __name__ == '__main__':
    user_selection = select_env()[0]
    if user_selection:
        env = Environment(user_selection)
        if(env.check_connection()):
            # todo: Add creation ticket handler here.
            pass
    else:
        print('Unexpected error. Shutting down')
        exit(1)