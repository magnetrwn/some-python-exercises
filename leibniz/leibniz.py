# Leibniz approach to Pi

def get_pi(try_times):
  pi, d = 0, 1
  for _ in range(try_times):
    pi += 1/d
    d += 2
    pi -= 1/d
    d += 2
  return 4*pi

def get_fixed_charlist(flo):
  return list(str('{0:.15f}'.format(flo)))

def endless_get_pi(rate):
  pi, d, showtext, shown = 0, 1, 0, 0
  pi_text = '0.000000000000000'
  pi_text_old = '0.000000000000000'
  while True:
    pi += 1/d
    d += 2
    pi -= 1/d
    d += 2
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
      if shown == 64:
        shown = 0
        pi_text_old = get_fixed_charlist(4*pi)
      print('[ leibniz.py | denominator:', len(str(d)),'digits | pi:', ''.join(pi_text), ']', end='\r')

endless_get_pi(262144)
