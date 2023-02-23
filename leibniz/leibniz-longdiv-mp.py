# Leibniz approach to Pi, with very slow long division and multiprocessing

from multiprocessing import Process, Queue, cpu_count

_PRECISION_DIGITS = 12

def get_division_classic(n, d, i):
  o = 0
  for _ in range(i):
    r = 0
    while n >= d:
      r += 1
      n -= d
    o += r
    o *= 10
    n *= 10
  return o

def get_leibniz_piece_worker(start_from, q, pd=_PRECISION_DIGITS):
  d = 1+start_from*4
  while True:
    pi = get_division_classic(1, d, pd)
    d += 2
    pi -= get_division_classic(1, d, pd)
    d += 2+(cpu_count()-1)*4
    q.put(pi)

def endless_get_pi(rate, pd=_PRECISION_DIGITS):
  pi, showtext, shown = 0, 0, 0
  pi_text = list(str(get_division_classic(0, 1, pd)))
  pi_text_old = list(str(get_division_classic(0, 1, pd)))
  
  q = Queue()
  
  for p in range(cpu_count()):
    Process(target=get_leibniz_piece_worker, args=(p, q, pd)).start()
  
  while True:
    pi += q.get()
    showtext += 1
    if showtext == rate:
      showtext = 0
      shown += 1
      pi_text = list(str(4*pi))
      pi_text.insert(1, '.')
      for idx in range(len(pi_text)):
        if pi_text[idx] == pi_text_old[idx]:
          pi_text[idx] = '\x1B[42m'+pi_text[idx]+'\x1B[0m'
        else:
          break
      if shown == 64:
        shown = 0
        pi_text_old = list(str(4*pi))
        pi_text_old.insert(1, '.')
      print('[ leibniz-longdiv-mp.py | pi:', ''.join(pi_text), ']', end='\r')

endless_get_pi(512, 64)
