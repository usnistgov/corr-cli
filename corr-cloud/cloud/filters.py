import datetime
from cloud import app

def ff(i, st):
    if i == 0:
        return
    else:
        if i == 1:
            st = st[:-1]
        return '{0} {1}'.format(i, st)

@app.template_filter('hms')
def _jinja2_filter_hms(time):
    td = datetime.timedelta(seconds=time)
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    ss_ = [ff(i, st) for i, st in [[days, 'days'], [hours, 'hours'], [minutes, 'minutes'], [seconds, 'seconds']]]
    ss = [s for s in ss_ if s is not None]
    return ', '.join(ss)


