import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.raw_req import RawRequests

class TestRobot(RawRequests):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        html = """\
        <html>
        <body>
            <h1>Hello world!</h1>
            <p>The quick brown fox jumped over the lazy dogs...</p>
        </body>
        </html>
        """
        self._email.set_recipients("sanj19972001@yahoo.com")
        self._email.set_message("Test HTML", html)
        self._email.send()
        self._email.set_message("Test HTML in Plaintext", html, msgtype="plain")
        self._email.send()

if __name__ == "__main__":
    tr = TestRobot(sys.argv)
    tr.execute()
