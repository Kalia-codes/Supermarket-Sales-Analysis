import subprocess
import sys


def run_script(script_name):
    print("\n" + "=" * 60)
    print(f"RUNNING: {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, f"src/{script_name}"],
        check=False
    )

    if result.returncode != 0:
        print(f"\nERROR: {script_name} failed.")
        sys.exit(result.returncode)


print("=" * 60)
print("SUPERMARKET SALES ANALYSIS PROJECT")
print("=" * 60)

# Step 1: Run sales analysis
run_script("sales_analysis.py")

# Step 2: Generate charts
run_script("create_charts.py")

print("\n" + "=" * 60)
print("PROJECT EXECUTION COMPLETED")
print("=" * 60)
print("\nGenerated charts are available in the charts/ folder.")