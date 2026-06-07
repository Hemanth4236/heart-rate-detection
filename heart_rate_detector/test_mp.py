import sys

print("Python Version:")
print(sys.version)

print("\nTrying to import MediaPipe...")

try:
    import mediapipe as mp

    print("\nMediaPipe imported successfully!")

    print("\nMediaPipe Location:")
    print(mp.__file__)

    print("\nAvailable Attributes:")
    print(dir(mp))

    if hasattr(mp, "solutions"):
        print("\nSUCCESS: mp.solutions exists")
    else:
        print("\nERROR: mp.solutions does NOT exist")

except Exception as e:
    print("\nMediaPipe Import Failed!")
    print(type(e).__name__)
    print(str(e))