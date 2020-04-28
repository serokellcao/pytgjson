# TODO Unused!
def tautology(x):
  return (x is x, {})
# TODO Unused!
def bind_monad_filtermap(ma, f):
  (m, a) = ma
  # We can encode capabilities with lists
  # But this sort of strictness is unused in this code yet
  assert(m == 'MONAD_FILTERMAP')
  return (m, f(a))

