from src import instances, errors


def lambda_handler(event, context):
    try:
        print(instances.start_instances())
    except errors.Error as err:
        err.to_dict()
