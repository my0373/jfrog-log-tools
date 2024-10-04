import unittest
from datetime import datetime, timedelta

from jfrog_utils.jfrog_logs import (
    get_random_dates,
    get_fake_ipv4,
    get_fake_ipv6,
    get_random_user,
    get_random_method,
    get_random_response_code,
    get_random_content_length,
    gen_v6_line,
    gen_v7in_line,
    gen_v7out_line,
    get_logfile_version,
    anonymise_v6_logfile,
    anonymise_v7in_logfile
)

class TestJfrogLogs(unittest.TestCase):
    def test_anonymise_v6_logfile(self):
        with open('test_log_v6.log', 'w') as f:
            f.write("20230101120000|100|REQUEST|192.168.1.1|admin|GET|/home/admin/file.zip|HTTP/1.1|200|1234\n")
        anonymise_v6_logfile('test_log_v6.log', 'test_log_v6_anonymised.log')
        with open('test_log_v6_anonymised.log', 'r') as f:
            anonymised_line = f.readline().strip()
        expected_line = "20230101120000|100|REQUEST|ADDRESS_REDACTED|USER_REDACTED|GET|URL_REDACTED|HTTP/1.1|200|1234"
        self.assertEqual(anonymised_line, expected_line)

    def test_anonymise_v7in_logfile(self):
        with open('test_log_v7in.log', 'w') as f:
            f.write("2023-01-01T12:00:00|abcdef1234567890|192.168.1.1|admin|GET|/home/admin/file.zip|200|1234|5678|100|JFrog Access Java Client/4.1.12\n")
        anonymise_v7in_logfile('test_log_v7in.log', 'test_log_v7in_anonymised.log')
        with open('test_log_v7in_anonymised.log', 'r') as f:
            anonymised_line = f.readline().strip()
        expected_line = "2023-01-01T12:00:00|abcdef1234567890|ADDRESS_REDACTED|USER_REDACTED|GET|URL_REDACTED|200|1234|5678|100|JFrog Access Java Client/4.1.12"
        self.assertEqual(anonymised_line, expected_line)


    def test_get_logfile_version_v6(self):
        with open('test_log_v6.log', 'w') as f:
            f.write("20230101120000|100|REQUEST|192.168.1.1|admin|GET|/home/admin/file.zip|HTTP/1.1|200|1234\n")
        version = get_logfile_version('test_log_v6.log')
        self.assertEqual(version, "v6")

    def test_get_logfile_version_v7in(self):
        with open('test_log_v7in.log', 'w') as f:
            f.write("2023-01-01T12:00:00|abcdef1234567890|192.168.1.1|admin|GET|/home/admin/file.zip|200|1234|5678|100|JFrog Access Java Client/4.1.12\n")
        version = get_logfile_version('test_log_v7in.log')
        self.assertEqual(version, "v7in")

    def test_get_logfile_version_unknown(self):
        with open('test_log_unknown.log', 'w') as f:
            f.write("Some random log line that doesn't match any known format\n")
        version = get_logfile_version('test_log_unknown.log')
        self.assertEqual(version, "unknown")

    def test_get_random_dates(self):
        random_date = get_random_dates(days=7)
        self.assertIsInstance(random_date, datetime)
        self.assertTrue(datetime.now() - timedelta(days=7) <= random_date <= datetime.now())

    def test_get_fake_ipv4(self):
        ipv4 = get_fake_ipv4()
        self.assertIsInstance(ipv4, str)
        self.assertEqual(len(ipv4.split('.')), 4)
        for part in ipv4.split('.'):
            self.assertTrue(0 <= int(part) <= 255)

    def test_get_fake_ipv6(self):
        ipv6 = get_fake_ipv6()
        self.assertIsInstance(ipv6, str)
        self.assertEqual(len(ipv6.split(':')), 8)

    def test_get_random_user(self):
        user = get_random_user()
        self.assertIn(user, ["admin", "anonymous", "crazydave", "upload_user", "jenkins", "non_authenticated_user"])

    def test_get_random_method(self):
        method = get_random_method()
        self.assertIn(method, ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"])

    def test_get_random_response_code(self):
        code = get_random_response_code()
        self.assertIn(code, [200, 201, 202, 204, 302, 400, 401, 403, 404, 405, 500])

    def test_get_random_content_length(self):
        length = get_random_content_length()
        self.assertIsInstance(length, int)
        self.assertTrue(0 <= length <= 9999999999)

    def test_gen_v6_line(self):
        line = gen_v6_line("ipv4")
        self.assertIsInstance(line, str)
        parts = line.split('|')
        self.assertEqual(len(parts), 10)

    def test_gen_v7in_line(self):
        line = gen_v7in_line("ipv6")
        self.assertIsInstance(line, str)
        parts = line.split('|')
        self.assertEqual(len(parts), 11)

    def test_gen_v7out_line(self):
        line = gen_v7out_line("ipv6")
        self.assertIsInstance(line, str)
        parts = line.split('|')
        self.assertEqual(len(parts), 10)

if __name__ == '__main__':
    unittest.main()