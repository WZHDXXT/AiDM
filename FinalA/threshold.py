import pandas as pd

# Function to calculate threshold and probability
def calculate_lsh(b, r, s_value):
    threshold = (1 / b) ** (1 / r)
    probability = 1 - (1 - s_value ** r) ** b
    return round(threshold, 3), round(probability, 3)

# Define h (signature length) and configurations
h = 80  # Set your signature length here
s_value = 0.5  # Similarity value to calculate probability

# Generate combinations of b and r
configurations = []
bs = [5, 10, 15, 20, 30, 40]
for b in bs:  # Explore band numbers from 10 to 30
    r = h // b
    configurations.append({"b": b, "r": r, "s_value": s_value})

# Calculate results
results = []
for config in configurations:
    b = config["b"]
    r = config["r"]
    s_value = config["s_value"]
    threshold, probability = calculate_lsh(b, r, s_value)
    results.append({
        "b (number of bands)": b,
        "r (rows per band)": r,
        "h (signature length)": h,
        "Approx. threshold (s)": threshold,
        "P (s=0.5)": probability,
    })

# Create a DataFrame
df = pd.DataFrame(results)

# Display the results
print(df)
