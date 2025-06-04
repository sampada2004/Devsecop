import os

# Bypass encryption for testing purposes
def encrypt_file(input_path, output_path):
    # For testing, just create a dummy file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write("This is a dummy encrypted file for testing monitoring.")
    print(f"Created dummy encrypted file at {output_path} for testing")

# Don't run this automatically
# encrypt_file("data/circulars2.pdf", "data/circulars2.enc")
