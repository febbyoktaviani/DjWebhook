from celery import task

@task(name="sum_two_numbers")
def add():
    return(1 + 1)