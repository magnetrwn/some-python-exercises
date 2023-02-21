# Monte Carlo approach to Pi, using multiprocessing Pool for concurrent get_pi() calls

from multiprocessing import Process, Queue, cpu_count
import random

def random_point(max_x, max_y):
  return (random.random()*max_x, random.random()*max_y)

def is_inside_quarter(point, r):
  if (point[0]**2+point[1]**2)**0.5 <= r:
    return True
  return False

def get_pi_worker(try_points, queue):
  while True:
    inside_points = 0
    for _ in range(try_points):
      if is_inside_quarter(random_point(1, 1), 1):
        inside_points+=1
    queue.put(4*(inside_points/try_points))

def get_fixed_charlist(flo):
  return list(str('{0:.15f}'.format(flo)))

def endless_get_pi(rate, processes):

  pi, pi_sum, iteration = 0, 0, 0
  q = Queue()

  for _ in range((processes-1) if processes > 1 else 1):
    Process(target=get_pi_worker, args=(rate, q)).start()

  while True:
    pi_sum = pi_sum+q.get()

    # (this is for colors)
    if iteration%150 == 0:
      old_str = get_fixed_charlist(pi)
    if iteration%300 == 0:
      old_str2 = get_fixed_charlist(pi)
    prev_str = get_fixed_charlist(pi)

    iteration += 1
    pi = pi_sum/iteration

    # (this is for colors)
    curr_str = get_fixed_charlist(pi)
    for idx in range(len(prev_str)):
      if old_str[idx] == curr_str[idx] and old_str2[idx] == curr_str[idx]:
        curr_str[idx] = '\x1B[42m'+curr_str[idx]+'\x1B[0m'
      elif prev_str[idx] == curr_str[idx]:
        curr_str[idx] = '\x1B[32m'+curr_str[idx]+'\x1B[0m'

    print('[ monte-carlo.py | iter:', iteration, 'x', rate, '| pi:', ''.join(curr_str), ']', end='\r')

endless_get_pi(40000, cpu_count())
