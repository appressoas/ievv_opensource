from django_rq import job


@job
def add(x, y):
    print('Add was called! with x:{}, y:{}'.format(x, y))
    return x + y
