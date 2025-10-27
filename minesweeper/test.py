from minesweeper import Sentence

cells = set([(0,0), (0,1),(0,2)])
count = 1
sent = Sentence(cells, count)

print(f"{sent}")

sent.mark_safe((0,0))
print(f"{sent}")

print(f"known mines: ")
for cell in sent.known_mines():
  print(f"{cell}")
sent.mark_mine((0,1))
print(f"\n{sent}")

print(f"known safe cells:")
for cell in sent.known_safes():
  print(f"{cell}")