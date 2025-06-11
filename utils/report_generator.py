import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path


class AllureReportGenerator:
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.allure_results_dir = self.project_root / "allure-results"
        self.reports_base_dir = self.project_root / "reports"

    def generate_timestamped_report(self, test_suite_name: str = "test_execution"):
        """Generate Allure report with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"{test_suite_name}_{timestamp}"
        report_dir = self.reports_base_dir / "allure" / report_name

        # Ensure directories exist
        self.reports_base_dir.mkdir(exist_ok=True)
        (self.reports_base_dir / "allure").mkdir(exist_ok=True)

        try:
            # Generate Allure report
            cmd = [
                "allure", "generate",
                str(self.allure_results_dir),
                "--output", str(report_dir),
                "--clean"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Create a "latest" symlink/copy for easy access
            latest_dir = self.reports_base_dir / "allure" / "latest"
            if latest_dir.exists():
                if latest_dir.is_dir():
                    shutil.rmtree(latest_dir)
                else:
                    latest_dir.unlink()

            # Copy instead of symlink for Windows compatibility
            shutil.copytree(report_dir, latest_dir)

            print(f"✅ Allure report generated successfully!")
            print(f"📁 Report location: {report_dir}")
            print(f"🔗 Latest report: {latest_dir}")
            print(f"🌐 Open report: {report_dir / 'index.html'}")

            return str(report_dir)

        except subprocess.CalledProcessError as e:
            print(f"❌ Error generating Allure report: {e}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None

    def open_report(self, report_path: str = None):
        """Open the Allure report in default browser"""
        if not report_path:
            report_path = self.reports_base_dir / "allure" / "latest"

        index_file = Path(report_path) / "index.html"
        if index_file.exists():
            os.startfile(str(index_file))  # Windows
        else:
            print(f"❌ Report not found at: {index_file}")

    def serve_report(self, report_path: str = None, port: int = 8080):
        """Serve Allure report using allure serve command"""
        try:
            if report_path:
                cmd = ["allure", "serve", str(report_path), "--port", str(port)]
            else:
                cmd = ["allure", "serve", str(self.allure_results_dir), "--port", str(port)]

            print(f"🚀 Starting Allure server on port {port}...")
            subprocess.run(cmd, check=True)

        except subprocess.CalledProcessError as e:
            print(f"❌ Error serving Allure report: {e}")
        except KeyboardInterrupt:
            print("\n🛑 Allure server stopped")


def generate_report_after_tests(test_suite_name: str = "automation_tests"):
    """Convenience function to generate report after test execution"""
    generator = AllureReportGenerator()
    return generator.generate_timestamped_report(test_suite_name)


def open_latest_report():
    """Convenience function to open the latest report"""
    generator = AllureReportGenerator()
    generator.open_report()


def serve_latest_results():
    """Convenience function to serve the latest test results"""
    generator = AllureReportGenerator()
    generator.serve_report()