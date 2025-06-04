import os

# Bypass encryption for testing purposes
def decrypt_file(input_path, output_path):
    # For testing, just create a dummy file if the output doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write("This is a dummy file for testing monitoring.")
        print(f"Created dummy file at {output_path} for testing")
    else:
        print(f"File {output_path} already exists, using it for testing")

# Don't run this automatically
# decrypt_file("data/circulars2.enc", "data/circulars.pdf")
