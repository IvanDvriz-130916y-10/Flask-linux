import io
import sys
import traceback
import unittest
from utils.context_managers import Redirect


class TestRedirect(unittest.TestCase):
    def test_capture_stdout(self):
        buffer = io.StringIO()
        with Redirect(stdout=buffer):
            print("Hello stdout.txt")
        self.assertTrue("Hello stdout.txt" in buffer.getvalue())

    def test_capture_stderr_traceback(self):
        err_buffer = io.StringIO()
        with Redirect(stderr=err_buffer):
            try:
                raise ValueError("Hello stderr.txt")
            except Exception:
                sys.stderr.write(traceback.format_exc())
        output = err_buffer.getvalue()
        self.assertIn("ValueError", output)
        self.assertIn("Hello stderr.txt", output)

    def test_nested_redirections_restore(self):
        outer = io.StringIO()
        inner = io.StringIO()
        orig_stdout = sys.stdout
        orig_stderr = sys.stderr

        with Redirect(stdout=outer):
            print("outer-1")
            with Redirect(stdout=inner):
                print("inner")
            print("outer-2")

        self.assertIn("outer-1", outer.getvalue())
        self.assertIn("outer-2", outer.getvalue())
        self.assertIn("inner", inner.getvalue())

        self.assertIs(sys.stdout, orig_stdout)
        self.assertIs(sys.stderr, orig_stderr)

    def test_redirect_without_args_does_nothing(self):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        with Redirect():
            pass
        self.assertIs(sys.stdout, old_stdout)
        self.assertIs(sys.stderr, old_stderr)

if __name__ == "__main__":
    unittest.main()