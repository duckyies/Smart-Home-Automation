print("Trying to import Device for test...")
try:
    from ..devices import Device
    print("Device import test: Successful!")
except ImportError as e:
    print(f"Device import test: Failed! Error: {e}")
    print(f"ImportError details: {e}") # Print detailed error