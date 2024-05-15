import hashlib

# with open("input.txt") as f:
#     digest = hashlib.file_digest(f, "sha512")
# print(digest.hexdigest())
m = hashlib.sha512()
m.update(b"The phony war is over and it will soon be time to discover who's hot and who's not on the 2023 Formula 1 grid. Red Bull ended last season in dominant shape, winning all bar one of the grand prix in the second half of the 22-round championship. Because of that - and their 2021 budget cap breach - they have less time to spend on developing their RB19. Will that allow Ferrari and Mercedes to reduce their advantage?")
print(m.hexdigest())
h = hashlib.sha512(b"The phony war is over and it will soon be time to discover who's hot and who's not on the 2023 Formula 1 grid. Red Bull ended last season in dominant shape, winning all bar one of the grand prix in the second half of the 22-round championship. Because of that - and their 2021 budget cap breach - they have less time to spend on developing their RB19. Will that allow Ferrari and Mercedes to reduce their advantage?").hexdigest()
FILEOUT = open('check.txt', 'w')
FILEOUT.write(h)
FILEOUT.close()
