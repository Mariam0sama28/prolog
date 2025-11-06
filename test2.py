from pyswip import Prolog

prolog = Prolog()
prolog.assertz("parent(mariam, osama)")
prolog.assertz("parent(osama, ali)")

print(list(prolog.query("parent(osama, X)")))
