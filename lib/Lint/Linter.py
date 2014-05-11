from sys import stderr
import traceback

def print_error(message):
  print >> stderr, 'CRYPTOLINT ERROR:', message
  traceback.print_stack()

class Linter:
  def __init__(self):
    self.previous_ivs = set()
    self.counter_key_combos = set()

  def add_iv(self, iv):
    if len(iv) == 0:
      return
    print 'IV', iv, len(iv)
    if iv in self.previous_ivs:
      print_error('Reuse of IV ' + str(iv))
    else:
      self.previous_ivs.add(iv)
  
  def check_AES_parameters(self, key, *args, **kwargs):
    if len(args) == 0:
      print_error('Default AES mode is unsafe')
    if kwargs.get('counter'):
      combo = (key, kwargs.get('counter').next_value())
      if combo in self.counter_key_combos:
        print_error("Reuse of Counter value and key: this will leak messages!")
      else:
        self.counter_key_combos.add(combo)

