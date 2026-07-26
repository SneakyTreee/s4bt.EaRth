import subprocess
import sys
import os

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    processes = []
    try:
        scan = subprocess.Popen(
            [sys.executable, "plantScan.py"],
            cwd=base_dir
        )
        processes.append(scan)
        web = subprocess.Popen(
            [sys.executable, "webserver.py"],
            cwd=base_dir
        )
        processes.append(web)

        print("🌱 EaRth gestartet")
        print(f"   plantScan.py  PID {scan.pid}")
        print(f"   webserver.py  PID {web.pid}")
        print("   Strg+C zum Beenden")

        scan.wait()
        web.wait()
    except KeyboardInterrupt:
        print("\n🛑 Beende alle Prozesse...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait()
        print("✅ Alles gestoppt")

if __name__ == "__main__":
    main()
