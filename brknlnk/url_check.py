from multiprocessing.pool import ThreadPool
import csv
from utils import uri_validator
from dataclasses import dataclass
from collections import namedtuple
import tqdm
import urllib.request, urllib.error
import datetime

@dataclass
class URLResult:
    url: str
    code: str
    code_num: int
    response_time: float
    info: str

class URLCheck:
    def __init__(self, data, conf):
        self.data = data
        self.conf = conf
        self.results = []
        self.progbar = tqdm.tqdm(total=len(data), leave=False)
        
        if len(data) == 1:
            if uri_validator(data[0]):
                self.check_link(data[0])
            elif data[0].endswith(".csv"):
                if not data[0].startswith("http"):
                    self.handle_as_file()
        elif len(data) > 1:
            self.handle_as_list()


    def get_result_info(self):
        results = namedtuple("results", ["passed", "failed", "warning"])
        passed = 0
        failed = 0
        warning = 0
        for i in self.results:
            if i.info == "passed":
                passed += 1
            if i.info == "failed":
                failed += 1
            if i.info == "warning":
                warning += 1
        return results(passed,failed, warning)
    
    def calc_info(self, code):
        if code:
            if code >= 200 and code < 300:
                return "passed"
            if code >= 300 and code < 600:
                return "failed"
        else:
            return "warning"
    
    def handle_as_file(self):
        out_list = []
        try:
            with open(self.data[0], "r") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for row in reader:
                    out_list.append(row[0])
            self.handle_as_list(out_list)
        except FileNotFoundError:
            self.progbar.write(f"Could not open file {self.data[0]} because it does not exist.")
            exit()

    def handle_as_list(self, data=None):
        if data is None:
            data = self.data
        self.progbar.total = len(data)

        results = ThreadPool(self.conf.workers)
        
        for i in results.imap_unordered(self.check_link, data):
            if self.conf.exit_on_fail:
                if i.info == "failed" or i.info == "warning":
                    results.close()
                    self.progbar.clear()
                    print(f"Exited because of failed/warning in URL response from {i.url}")
                    exit(1)

    def check_link(self, url):
        start_time = datetime.datetime.now()
        returned_code = None
        returned_code_num = None
        try:
            connection = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": self.conf.user_agent}), timeout=self.conf.timeout)
        except urllib.error.HTTPError as error:
            returned_code_num = error.code
            returned_code = f"HTTPError: {error.code}"
        except urllib.error.URLError as error:
            returned_code = f"URLError: {error.reason}"
        except:
            returned_code = f"UNKNOWN"
        else:
            # status code 200
            returned_code_num = connection.getcode()
            returned_code = f"HTTPError: {connection.getcode()}"
        
        end_time = datetime.datetime.now()
        delta = end_time - start_time
        elapsed = round(delta.microseconds * .000001, 6)
        result = URLResult(url, returned_code, returned_code_num, elapsed, self.calc_info(returned_code_num))

        self.results.append(result)
        if "stdout-all" in self.conf.output:
            self.progbar.write(str(result))
        
        if "stdout-passed" in self.conf.output:
            if result.info == "passed":
                self.progbar.write(str(result))
        
        if "stdout-warning" in self.conf.output:
            if result.info == "warning":
                self.progbar.write(str(result))
        
        if "stdout-failed" in self.conf.output:
            if result.info == "failed":
                self.progbar.write(str(result))

        self.progbar.update(1)
        return result