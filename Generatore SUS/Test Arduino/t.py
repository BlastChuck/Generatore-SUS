import requests
from collections import Counter

# Arduino server URL
arduino_url = "http://77.32.113.106"  # Replace "arduino_ip_address" with the actual IP address of your Arduino device

# Function to load presets from Arduino server
def load_presets():
    response = requests.get(f"{arduino_url}/api/loadDefaults")
    if response.status_code == 200:
        presets = response.json()
        print("Presets loaded successfully:")
        print("Min:", presets['min'])
        print("Max:", presets['max'])
        print("Exclude:", presets['exclude'])
        return presets
    else:
        print("Failed to load presets")
        return None

# Function to generate random numbers from Arduino server using presets
def generate_random_numbers(num_requests, presets):
    numbers = []
    for i in range(num_requests):
        response = requests.get(f"{arduino_url}/api/random", params=presets)
        if response.status_code == 200:
            numbers.append(int(response.text))
            print(f"Request {i+1}/{num_requests} - Random number: {response.text}")
        else:
            print(f"Failed to generate random number for request {i+1} - Status code: {response.status_code}")
    return numbers

# Load presets from Arduino server
presets = load_presets()

# If presets are loaded successfully, generate random numbers using those presets
if presets:
    # Send 1000 requests to generate random numbers using presets
    random_numbers = generate_random_numbers(1000, presets)

    # Calculate the probability of each number appearing
    counter = Counter(random_numbers)
    total_requests = len(random_numbers)
    probabilities = {num: count / total_requests * 100 for num, count in counter.items()}

    # Calculate total percentage
    total_percentage = sum(probabilities.values())

    # Print the probabilities as percentages
    print("\nProbability of each number appearing:")
    for num, prob in sorted(probabilities.items()):
        print(f"Number {num}: {prob:.2f}%")
    print(f"\nTotal percentage: {total_percentage:.2f}%")