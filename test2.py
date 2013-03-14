import dl, time
a=dl.open('/lib64/libc.so.6')
a.call('time'), time.time()
