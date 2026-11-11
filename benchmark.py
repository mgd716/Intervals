import time
import itertools
import random

lats = [random.uniform(-90, 90) for _ in range(1000000)]
lngs = [random.uniform(-180, 180) for _ in range(1000000)]

# Current approach
start = time.time()
res1 = [[round(lat, 5), round(lng, 5)] for lat, lng in zip(lats, lngs) if lat is not None and lng is not None][::4]
end = time.time()
print(f"Current approach: {end - start:.4f} seconds")

# Optimized approach
start = time.time()
valid_points = ((lat, lng) for lat, lng in zip(lats, lngs) if lat is not None and lng is not None)
res2 = [[round(lat, 5), round(lng, 5)] for lat, lng in itertools.islice(valid_points, 0, None, 4)]
end = time.time()
print(f"Optimized approach: {end - start:.4f} seconds")

assert res1 == res2
print("Results match!")
