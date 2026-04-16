#!/usr/bin/env python3
"""
Knowledge Atlas API Test Harness

Comprehensive test suite that exercises every API endpoint with dummy data.
Tests auth, assignments, articles, submissions, claims, and student progress.
Generates a minimal PDF in-memory for upload testing.
"""

import requests
import json
import sys
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8765"
TEST_USER_EMAIL = f"test_student_{int(time.time())}@ucsd.edu"
TEST_USER_PASSWORD = "TestPassword123!"
TEST_USER_NAME = "Test Student"

# ANSI color codes (accessible: green/red, not blue)
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Test tracking
test_results = {"passed": 0, "failed": 0, "skipped": 0}
test_user_id = None
auth_token = None
refresh_token = None
current_password = TEST_USER_PASSWORD

def create_minimal_pdf():
    """Create a minimal valid PDF in memory."""
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT /F1 12 Tf 100 700 Td (Test PDF) Tj ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000273 00000 n
0000000367 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
446
%%EOF
"""
    return BytesIO(pdf_content)

def print_test_header(test_name):
    """Print a formatted test header."""
    print(f"\n{CYAN}▶ {test_name}{RESET}")

def print_result(expected, actual, passed, details=""):
    """Print test result with colors."""
    if passed:
        print(f"  {GREEN}✓ PASS{RESET} | Expected: {expected} | Got: {actual}")
        test_results["passed"] += 1
    else:
        print(f"  {RED}✗ FAIL{RESET} | Expected: {expected} | Got: {actual}")
        if details:
            print(f"       {RED}Details: {details}{RESET}")
        test_results["failed"] += 1

def print_skip(reason):
    """Print skipped test."""
    print(f"  {YELLOW}⊘ SKIP{RESET} | {reason}")
    test_results["skipped"] += 1

def check_server_alive():
    """Check if server is running."""
    print_test_header("Health Check - Server Alive")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_result("Status 200", f"Status {response.status_code}", True)
            return True
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text)
            return False
    except requests.exceptions.ConnectionError:
        print(f"\n{RED}❌ FATAL: Server not running at {BASE_URL}{RESET}")
        print(f"   Start the server with: python3 scripts/ka_local_server_setup.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}❌ FATAL: {e}{RESET}")
        sys.exit(1)

def test_register():
    """Test user registration."""
    global test_user_id
    print_test_header("POST /auth/register - Create Test User")

    payload = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "first_name": "Test",
        "last_name": "Student"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if response.status_code == 201:
            data = response.json()
            test_user_id = data.get("id") or data.get("user_id")
            print_result("Status 201 + user_id", f"Status {response.status_code}", True)
            return True
        elif response.status_code == 409:
            # User might already exist
            print_skip("User already registered")
            return True
        else:
            print_result(
                "Status 201",
                f"Status {response.status_code}",
                False,
                response.text[:200]
            )
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_login():
    """Test user login and get tokens."""
    global auth_token, refresh_token, test_user_id
    print_test_header("POST /auth/login - Get JWT Tokens")

    payload = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        if response.status_code == 200:
            data = response.json()
            auth_token = data.get("access_token")
            refresh_token = data.get("refresh_token")
            if not auth_token:
                print_result("access_token present", "None", False)
                return False
            print_result("Status 200 + tokens", f"Status {response.status_code} + tokens", True)
            return True
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_get_me():
    """Test GET /auth/me - Get user profile."""
    print_test_header("GET /auth/me - Verify User Profile")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            data = response.json()
            email_match = data.get("email") == TEST_USER_EMAIL
            print_result(
                f"Status 200 + email={TEST_USER_EMAIL}",
                f"Status {response.status_code} + email={data.get('email')}",
                email_match
            )
            return email_match
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_update_track_track1():
    """Test POST /auth/update-track - Set to track1."""
    print_test_header("POST /auth/update-track - Set Track to track1")

    if not auth_token:
        print_skip("No auth token available")
        return False

    payload = {"track": "track1"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.post(f"{BASE_URL}/auth/update-track", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            track_match = data.get("track") == "track1"
            print_result(
                "Status 200 + track=track1",
                f"Status {response.status_code} + track={data.get('track')}",
                track_match
            )
            return track_match
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_update_track_track2():
    """Test POST /auth/update-track - Change to track2."""
    print_test_header("POST /auth/update-track - Change Track to track2")

    if not auth_token:
        print_skip("No auth token available")
        return False

    payload = {"track": "track2"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.post(f"{BASE_URL}/auth/update-track", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            track_match = data.get("track") == "track2"
            print_result(
                "Status 200 + track=track2",
                f"Status {response.status_code} + track={data.get('track')}",
                track_match
            )
            return track_match
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_update_track_invalid():
    """Test POST /auth/update-track - Invalid track (should return 400)."""
    print_test_header("POST /auth/update-track - Reject Invalid Track")

    if not auth_token:
        print_skip("No auth token available")
        return False

    payload = {"track": "invalid_track_xyz"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.post(f"{BASE_URL}/auth/update-track", json=payload, headers=headers)
        if response.status_code == 400:
            print_result("Status 400 (Bad Request)", f"Status {response.status_code}", True)
            return True
        else:
            print_result("Status 400", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_change_password():
    """Test POST /auth/change-password."""
    print_test_header("POST /auth/change-password - Update Password")

    if not auth_token:
        print_skip("No auth token available")
        return False

    global current_password
    new_password = "NewPassword456!"
    payload = {
        "current_password": current_password,
        "new_password": new_password
    }
    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.post(f"{BASE_URL}/auth/change-password", json=payload, headers=headers)
        # Accept 200 or 204 (No Content)
        success = response.status_code in [200, 204]
        if success:
            current_password = new_password
        print_result(
            "Status 200 or 204",
            f"Status {response.status_code}",
            success
        )
        return success
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_change_email():
    """Test POST /auth/change-email."""
    print_test_header("POST /auth/change-email - Update Email")

    if not auth_token:
        print_skip("No auth token available")
        return False

    new_email = f"test_student_updated_{int(time.time())}@ucsd.edu"
    payload = {"current_password": current_password, "new_email": new_email}
    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.post(f"{BASE_URL}/auth/change-email", json=payload, headers=headers)
        success = response.status_code in [200, 204]
        print_result(
            "Status 200 or 204",
            f"Status {response.status_code}",
            success
        )
        return success
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_forgot_password():
    """Test POST /auth/forgot-password - Request password reset."""
    print_test_header("POST /auth/forgot-password - Request Password Reset")

    payload = {"email": TEST_USER_EMAIL}

    try:
        response = requests.post(f"{BASE_URL}/auth/forgot-password", json=payload)
        # Accept 200 (OK) or 202 (Accepted)
        success = response.status_code in [200, 202]
        print_result(
            "Status 200 or 202",
            f"Status {response.status_code}",
            success
        )
        return success
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_refresh_token():
    """Test POST /auth/refresh - Refresh access token."""
    print_test_header("POST /auth/refresh - Refresh Access Token")

    if not refresh_token:
        print_skip("No refresh token available")
        return False

    payload = {"refresh_token": refresh_token}

    try:
        response = requests.post(f"{BASE_URL}/auth/refresh", json=payload)
        if response.status_code == 200:
            data = response.json()
            has_access_token = "access_token" in data
            print_result(
                "Status 200 + access_token",
                f"Status {response.status_code}" + (" + access_token" if has_access_token else ""),
                has_access_token
            )
            return has_access_token
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_get_assignments():
    """Test GET /api/assignments - Get assignments."""
    print_test_header("GET /api/assignments - List Assignments")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{BASE_URL}/api/assignments", headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Endpoint returns a dict with assignment info (or "assigned": False)
            print_result("Status 200 + data", f"Status {response.status_code} + type={type(data).__name__}", True)
            return True
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_get_article_stats():
    """Test GET /api/articles/stats - Get article statistics."""
    print_test_header("GET /api/articles/stats - Article Statistics")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{BASE_URL}/api/articles/stats", headers=headers)
        if response.status_code == 200:
            print_result("Status 200", f"Status {response.status_code}", True)
            return True
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_get_my_submissions():
    """Test GET /api/articles/my-submissions - Get user submissions."""
    print_test_header("GET /api/articles/my-submissions - My Submissions")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{BASE_URL}/api/articles/my-submissions", headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Endpoint may return dict with submissions key or a list
            print_result("Status 200 + data", f"Status {response.status_code} + type={type(data).__name__}", True)
            return True
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_submit_article():
    """Test POST /api/articles/submit - Upload a PDF."""
    print_test_header("POST /api/articles/submit - Upload PDF")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        # Create a minimal PDF
        pdf_file = create_minimal_pdf()
        # FastAPI endpoint param is "files" (List[UploadFile])
        files = [("files", ("test_article.pdf", pdf_file, "application/pdf"))]

        response = requests.post(f"{BASE_URL}/api/articles/submit", files=files, headers=headers)
        success = response.status_code in [200, 201, 202]
        print_result(
            "Status 200/201/202",
            f"Status {response.status_code}",
            success
        )
        return success
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_check_duplicate():
    """Test POST /api/articles/check-duplicate - Duplicate check."""
    print_test_header("POST /api/articles/check-duplicate - Check for Duplicates")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"title": "Test Article"}

    try:
        response = requests.post(f"{BASE_URL}/api/articles/check-duplicate", json=payload, headers=headers)
        success = response.status_code in [200, 204]
        print_result(
            "Status 200 or 204",
            f"Status {response.status_code}",
            success
        )
        return success
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_get_available_questions():
    """Test GET /api/articles/questions/available - List available questions."""
    print_test_header("GET /api/articles/questions/available - Available Questions")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{BASE_URL}/api/articles/questions/available", headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Endpoint may return dict with questions key or a list
            print_result("Status 200 + data", f"Status {response.status_code} + type={type(data).__name__}", True)
            return True
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_claim_question():
    """Test POST /api/articles/questions/claim - Claim a question."""
    print_test_header("POST /api/articles/questions/claim - Claim Question")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}
    # Use a test question ID; actual ID may vary (server seeds Q01-Q30)
    payload = {"question_id": "Q01"}

    try:
        response = requests.post(f"{BASE_URL}/api/articles/questions/claim", json=payload, headers=headers)
        success = response.status_code in [200, 201, 202]
        print_result(
            "Status 200/201/202",
            f"Status {response.status_code}",
            success
        )
        return success
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_get_my_claim():
    """Test GET /api/articles/questions/my-claim - Get user's claim."""
    print_test_header("GET /api/articles/questions/my-claim - My Claim")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{BASE_URL}/api/articles/questions/my-claim", headers=headers)
        success = response.status_code in [200, 204]  # 204 if no claim exists
        print_result(
            "Status 200 or 204",
            f"Status {response.status_code}",
            success
        )
        return success
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_release_claim():
    """Test POST /api/articles/questions/release - Release claim."""
    print_test_header("POST /api/articles/questions/release - Release Claim")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        payload = {"question_id": "Q01"}
        response = requests.post(f"{BASE_URL}/api/articles/questions/release", json=payload, headers=headers)
        success = response.status_code in [200, 204]
        print_result(
            "Status 200 or 204",
            f"Status {response.status_code}",
            success
        )
        return success
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def test_get_student_progress():
    """Test GET /api/student/progress - Get student progress."""
    print_test_header("GET /api/student/progress - Student Progress")

    if not auth_token:
        print_skip("No auth token available")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{BASE_URL}/api/student/progress", headers=headers)
        if response.status_code == 200:
            print_result("Status 200", f"Status {response.status_code}", True)
            return True
        else:
            print_result("Status 200", f"Status {response.status_code}", False, response.text[:200])
            return False
    except Exception as e:
        print_result("Success", f"Exception: {e}", False)
        return False

def cleanup_test_user():
    """Attempt to delete the test user (optional cleanup)."""
    print(f"\n{CYAN}▶ Cleanup - Delete Test User{RESET}")

    if not auth_token:
        print_skip("No auth token available")
        return

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        # Try DELETE /auth/me or similar endpoint
        response = requests.delete(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code in [200, 204]:
            print(f"  {GREEN}✓ PASS{RESET} | Test user deleted")
        else:
            print(f"  {YELLOW}⊘ SKIP{RESET} | Cleanup endpoint not available (status {response.status_code})")
    except Exception as e:
        print(f"  {YELLOW}⊘ SKIP{RESET} | Cleanup failed: {e}")

def print_summary():
    """Print test summary."""
    total = test_results["passed"] + test_results["failed"]
    print(f"\n" + "="*70)
    print(f"{BOLD}TEST SUMMARY{RESET}")
    print("="*70)
    print(f"{GREEN}✓ Passed:  {test_results['passed']}{RESET}")
    print(f"{RED}✗ Failed:  {test_results['failed']}{RESET}")
    print(f"{YELLOW}⊘ Skipped: {test_results['skipped']}{RESET}")
    print(f"{BOLD}Total:    {total}{RESET}")
    print("="*70 + "\n")

    if test_results["failed"] == 0:
        print(f"{GREEN}🎉 All tests passed!{RESET}\n")
        return 0
    else:
        print(f"{RED}❌ {test_results['failed']} test(s) failed{RESET}\n")
        return 1

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print(f"{BOLD}KNOWLEDGE ATLAS API TEST HARNESS{RESET}")
    print("="*70)
    print(f"Server: {BASE_URL}")
    print(f"Test User: {TEST_USER_EMAIL}")
    print(f"Test Time: {datetime.now().isoformat()}")
    print("="*70)

    try:
        # Step 1: Health check
        if not check_server_alive():
            sys.exit(1)

        # Step 2: Authentication tests
        test_register()
        test_login()
        test_get_me()

        # Step 3: Track tests
        test_update_track_track1()
        test_update_track_track2()
        test_update_track_invalid()

        # Step 4: Account management tests
        test_refresh_token()       # before change-password (which may invalidate tokens)
        test_forgot_password()     # before change-email (which changes the registered email)
        test_change_password()
        test_change_email()

        # Step 5: Assignment and article tests
        test_get_assignments()
        test_get_article_stats()
        test_get_my_submissions()
        test_submit_article()
        test_check_duplicate()

        # Step 6: Question/claim tests
        test_get_available_questions()
        test_claim_question()
        test_get_my_claim()
        test_release_claim()

        # Step 7: Progress test
        test_get_student_progress()

        # Cleanup
        cleanup_test_user()

        # Summary
        exit_code = print_summary()
        sys.exit(exit_code)

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test run cancelled by user{RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}❌ Unexpected error: {e}{RESET}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
