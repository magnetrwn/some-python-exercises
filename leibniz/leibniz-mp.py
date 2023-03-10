# Leibniz approach to Pi, with multiprocessing (every process calculates
# two pieces of the leibniz series, then skips cpu_count() pieces for the
# other processes to calculate them)

# WARNING: once the queue is filled, calculation slows down drastically,
#          based on the single-process loop of endless_get_pi()!
#          Try to balance the two default variables for best speed on your
#          platform.

from multiprocessing import Process, Queue, cpu_count

_QUEUE_PUT_GROUPS = 2048
_QUEUE_SIZE = 262144

def get_leibniz_piece_worker(start_from, q, group_by=_QUEUE_PUT_GROUPS):
  d = 1+start_from*4
  while True:
    pi = 0
    for _ in range(group_by):
      pi += 1/d
      d += 2
      pi -= 1/d
      d += 2+(cpu_count()-1)*4
    q.put(pi)

def get_fixed_charlist(flo):
  return list(str('{0:.15f}'.format(flo)))

def endless_get_pi(rate, queue_size=_QUEUE_SIZE, group_by=_QUEUE_PUT_GROUPS):
  pi, showtext, shown = 0, 0, 0
  pi_text = get_fixed_charlist(0.0)
  pi_text_old = get_fixed_charlist(0.0)

  q = Queue(queue_size)

  for p in range(cpu_count()):
    Process(target=get_leibniz_piece_worker, args=(p, q, group_by)).start()

  while True:
    pi += q.get()
    showtext += 1
    if showtext == rate:
      showtext = 0
      shown += 1
      pi_text = get_fixed_charlist(4*pi)
      for idx in range(len(pi_text)):
        if pi_text[idx] == pi_text_old[idx]:
          pi_text[idx] = '\x1B[42m'+pi_text[idx]+'\x1B[0m'
        else:
          break
      if shown == 32:
        shown = 0
        pi_text_old = get_fixed_charlist(4*pi)
      print('[ leibniz-mp.py | pi:', ''.join(pi_text), ']', end='\r')

endless_get_pi(2048)
