import time
import os
import webbrowser
from simple_monitoring import start_monitoring, generate_html_report

def main():
    print("Starting RITBuddy Monitoring System...")
    monitor_thread = start_monitoring()
    
    print("\n" + "="*50)
    print("Monitoring system is now running!")
    print("="*50)
    print("\nMetrics are being collected in the 'metrics' directory.")
    print("A report will be generated when you stop the monitoring.")
    print("\nPress Ctrl+C to stop monitoring and generate a report.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nGenerating monitoring report...")
        report_file = generate_html_report()
        abs_path = os.path.abspath(report_file)
        print(f"Report generated: {abs_path}")
        
        # Open the report in the default browser
        webbrowser.open('file://' + abs_path)
        
        print("\nMonitoring system stopped. You can restart it anytime by running this script again.")

if __name__ == "__main__":
    main()
