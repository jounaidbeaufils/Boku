from random import choice

from priorityq.mapped_queue import MappedQueueWithUndo
from minmax.heuristictile import HeuristicTile

q = MappedQueueWithUndo()
tup1 = (choice(range(4)), choice(range(4)), choice(range(4)))
tup2 = (choice(range(4)), choice(range(4)), choice(range(4)))
tup3 = (choice(range(4)), choice(range(4)), choice(range(4)))

q.push(HeuristicTile(tup1, choice(range(10))))
q.push(HeuristicTile(tup2, choice(range(10))))
q.push(HeuristicTile(tup3, choice(range(10))))

top_tup = q.pop()
print(f"top_tup: {top_tup}")

q.push(top_tup)
q.remove(top_tup)

new_top_tup = q.pop()
print(f"new_top_tup: {new_top_tup}")

print("internal representation of the queue:")
q2 = MappedQueueWithUndo()
for _ in range(5):
    q2.push(choice(range(10)))


print("\nq2.h:")
print(q2.h)

print("\nq2.__iter__():")
for elt in q2:
    print(elt)
print("\nq2.pop()")
for _ in range (len(q2.h)):
    print(q2.pop())
