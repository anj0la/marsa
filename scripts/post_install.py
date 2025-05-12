import subprocess
import sys

def main():
    try:
        subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
            check=True
        )
    except subprocess.CalledProcessError:
        print("Failed to download spaCy model.")
        sys.exit(1)

if __name__ == "__main__":
    main()
