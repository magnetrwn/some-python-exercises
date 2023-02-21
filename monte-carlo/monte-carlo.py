# Example: Monte Carlo approach to Pi

import random

def random_point(max_x, max_y):
  return (random.random()*max_x, random.random()*max_y)

def is_inside_quarter(point, r):
  if (point[0]**2+point[1]**2)**0.5 <= r:
    return True
  return False

def get_pi(try_points):
  inside_points = 0
  for i in range(try_points):
    if is_inside_quarter(random_point(1, 1), 1):
      inside_points+=1
  return 4*(inside_points/try_points)

def endless_get_pi(rate):
  pi, pi_sum, i = 0, 0, 0
  while True:
    i += 1
    pi_sum = pi_sum+get_pi(rate)
    
    if i%150 == 1:
      old_str = list(str('{0:.15f}'.format(pi)))
    if i%300 == 1:
      old_str2 = list(str('{0:.15f}'.format(pi)))
    prev_str = list(str('{0:.15f}'.format(pi)))
    
    pi = pi_sum/i
    
    curr_str = list(str('{0:.15f}'.format(pi)))
    for idx in range(len(prev_str)):
      if old_str[idx] == curr_str[idx] and old_str2[idx] == curr_str[idx]:
        curr_str[idx] = '\x1B[42m'+curr_str[idx]+'\x1B[0m'
      elif prev_str[idx] == curr_str[idx]:
        curr_str[idx] = '\x1B[32m'+curr_str[idx]+'\x1B[0m'
      else:
        break
    
    print('[ monte-carlo.py | iter:', i, 'x', rate, '| pi:', ''.join(curr_str), ']', end='\r')

endless_get_pi(12000)
