from src import instances, errors


def lambda_handler(event, context):
    try:
        print(instances.stop_instances())
    except errors.Error as err:
        err.to_dict()
