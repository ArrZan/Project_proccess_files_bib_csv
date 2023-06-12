sweets = ["cupcake", "candy", "lollipop", "cake", "lollipop", "cheesecake", "candy", "cupcake"]
unique_sweets = []
for sweet in sweets:
    if sweet not in unique_sweets:
        unique_sweets.append(sweet)

print(unique_sweets)
print(set(sweets))
