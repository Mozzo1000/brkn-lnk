
import argparse
from url_check import URLCheck

def main():
    parser = argparse.ArgumentParser("brkn-lnk", description="Check if link is broken")
    parser.add_argument("url", help="Link to check", nargs='+')
    parser.add_argument("--workers", type=int, default=20, help="Number of concurrent requests made")
    parser.add_argument("--timeout", type=int, default=5, help="Time to wait for a response before failing a request, supplied in seconds.")
    parser.add_argument("-o", "--output", nargs="+", default="stdout-info", choices=["stdout-info", "stdout-all", "stdout-passed", "stdout-warning", "stdout-failed"])
    parser.add_argument("--user-agent", default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.3", help="User agent for HTTP requests.")
    parser.add_argument("--exit-on-fail", action='store_true', help="Terminate the program and return exit code 1 on any failed or warning responses.")

    url = parser.parse_args().url
    print("Checking links..")
    checker = URLCheck(url, conf=parser.parse_args())
    
    if "stdout-info" in parser.parse_args().output:
        if checker.results:
            print(f"✅ Passed: {checker.get_result_info().passed}")
            print(f"⚠️ Warning: {checker.get_result_info().warning}")
            print(f"❌ Failed: {checker.get_result_info().failed}")
        else:
            print("No results to show")


if __name__ == "__main__":
    main()