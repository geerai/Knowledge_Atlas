#!/bin/bash
# KA Server Snapshot Script
# Run on xrlab.ucsd.edu to capture full server state
# Output: /tmp/ka_server_snapshot.txt
# Usage: bash ka_server_snapshot.sh

OUT="/tmp/ka_server_snapshot.txt"
echo "=== KA SERVER SNAPSHOT $(date) ===" > "$OUT"

# 1. Where are the repos?
echo -e "\n=== REPO LOCATIONS ===" >> "$OUT"
for d in /srv/atlas /var/www /home/*/REPOS ~/REPOS /var/www/html/ka; do
  if [ -d "$d" ]; then
    echo "FOUND: $d" >> "$OUT"
    ls -la "$d" >> "$OUT" 2>&1
  fi
done

# 2. Find the KA root by locating ka_auth_server.py
KA_ROOT=$(find /srv /var/www /home -maxdepth 4 -name "ka_auth_server.py" -printf '%h\n' 2>/dev/null | head -1)
if [ -z "$KA_ROOT" ]; then
  # Fallback: look for ka_home.html
  KA_ROOT=$(find /srv /var/www /home -maxdepth 4 -name "ka_home.html" -printf '%h\n' 2>/dev/null | head -1)
fi
echo -e "\n=== KA ROOT: ${KA_ROOT:-NOT FOUND} ===" >> "$OUT"

if [ -z "$KA_ROOT" ]; then
  echo "ERROR: Could not find KA root. Dumping broad search..." >> "$OUT"
  find /srv /var/www /home -maxdepth 3 -type d 2>/dev/null >> "$OUT"
  echo -e "\n=== SNAPSHOT INCOMPLETE ===" >> "$OUT"
  echo "File saved to $OUT ($(wc -l < "$OUT") lines)"
  exit 1
fi

# 3. Full file listing of KA root (HTML, JS, CSS, PY only)
echo -e "\n=== KA ROOT FILES ===" >> "$OUT"
find "$KA_ROOT" -maxdepth 1 \( -name "*.html" -o -name "*.js" -o -name "*.css" -o -name "*.py" \) | sort >> "$OUT"

# 4. 160sp directory
echo -e "\n=== 160SP ALL FILES ===" >> "$OUT"
find "$KA_ROOT/160sp" -type f 2>/dev/null | sort >> "$OUT"

echo -e "\n=== 160SP CONTEXT FILES ===" >> "$OUT"
ls -la "$KA_ROOT/160sp/context/" 2>/dev/null >> "$OUT"

# 5. Git state
echo -e "\n=== GIT STATUS ===" >> "$OUT"
cd "$KA_ROOT" 2>/dev/null
git status --short >> "$OUT" 2>&1
echo -e "\n=== GIT BRANCHES (all) ===" >> "$OUT"
git branch -a >> "$OUT" 2>&1
echo -e "\n=== GIT LOG (last 20 commits) ===" >> "$OUT"
git log --oneline -20 >> "$OUT" 2>&1
echo -e "\n=== GIT REMOTE ===" >> "$OUT"
git remote -v >> "$OUT" 2>&1

# 6. All database files anywhere under KA
echo -e "\n=== DATABASE FILES ===" >> "$OUT"
find "$KA_ROOT" -name "*.db" -exec ls -lh {} \; >> "$OUT" 2>&1

# 7. Auth DB and any other DBs — schema + data
echo -e "\n=== DATABASE CONTENTS ===" >> "$OUT"
for db in "$KA_ROOT"/data/ka_auth.db "$KA_ROOT"/data/ka_workflow.db "$KA_ROOT"/data/*.db "$KA_ROOT"/*.db; do
  [ -f "$db" ] || continue
  echo -e "\n--- DATABASE: $db ---" >> "$OUT"
  echo "Tables:" >> "$OUT"
  sqlite3 "$db" ".tables" >> "$OUT" 2>&1
  echo -e "\nFull schema:" >> "$OUT"
  sqlite3 "$db" ".schema" >> "$OUT" 2>&1
  # Try common table names for student data
  for tbl in users students registrations track_assignments teams submissions grades workflow_items assignments profiles; do
    COUNT=$(sqlite3 "$db" "SELECT count(*) FROM $tbl;" 2>/dev/null)
    if [ -n "$COUNT" ] && [ "$COUNT" != "0" ]; then
      echo -e "\n--- $tbl ($COUNT rows) ---" >> "$OUT"
      sqlite3 "$db" -header -csv "SELECT * FROM $tbl LIMIT 50;" >> "$OUT" 2>&1
    fi
  done
  # Also dump any table we didn't guess
  TABLES=$(sqlite3 "$db" ".tables" 2>/dev/null)
  for tbl in $TABLES; do
    COUNT=$(sqlite3 "$db" "SELECT count(*) FROM $tbl;" 2>/dev/null)
    echo "  $tbl: $COUNT rows" >> "$OUT"
  done
done

# 8. Workflow store (JS or JSON file that ka_approve.html reads)
echo -e "\n=== WORKFLOW STORE FILES ===" >> "$OUT"
for f in "$KA_ROOT"/data/ka_payloads/workflow.js "$KA_ROOT"/data/ka_payloads/workflow.json "$KA_ROOT"/data/workflow.js "$KA_ROOT"/data/workflow.json; do
  if [ -f "$f" ]; then
    echo -e "\n--- $f ($(wc -c < "$f") bytes) ---" >> "$OUT"
    cat "$f" >> "$OUT" 2>&1
  fi
done

# 9. Server process info
echo -e "\n=== RUNNING PROCESSES ===" >> "$OUT"
ps aux | grep -iE "ka_auth|uvicorn|fastapi|gunicorn|python.*ka" | grep -v grep >> "$OUT" 2>&1

echo -e "\n=== SYSTEMD SERVICES ===" >> "$OUT"
for pattern in ka atlas knowledge; do
  find /etc/systemd/system -name "${pattern}*" -exec echo "--- {} ---" \; -exec cat {} \; >> "$OUT" 2>&1
done
systemctl list-units --type=service --state=running 2>/dev/null | grep -iE "ka|atlas|uvicorn" >> "$OUT" 2>&1

# 10. Environment variables (from service files or .env)
echo -e "\n=== ENV FILES ===" >> "$OUT"
for f in "$KA_ROOT"/.env "$KA_ROOT"/data/.env /etc/default/ka*; do
  if [ -f "$f" ]; then
    echo "--- $f ---" >> "$OUT"
    # Redact secrets but show structure
    sed 's/=.*/=<REDACTED>/' "$f" >> "$OUT" 2>&1
  fi
done

# 11. Checksums of all 160sp HTML files (for diffing against local)
echo -e "\n=== 160SP FILE CHECKSUMS (md5) ===" >> "$OUT"
find "$KA_ROOT/160sp" -name "*.html" -exec md5sum {} \; 2>/dev/null | sort >> "$OUT"

# 12. Checksums of root HTML/JS files too
echo -e "\n=== ROOT FILE CHECKSUMS (md5) ===" >> "$OUT"
find "$KA_ROOT" -maxdepth 1 \( -name "*.html" -o -name "*.js" \) -exec md5sum {} \; 2>/dev/null | sort >> "$OUT"

# 13. Key 160sp pages — full content of the ones most likely edited on server
for f in ka_track_signup.html ka_dashboard.html ka_approve.html ka_schedule.html ka_student_setup.html ka_tracks.html ka_track1_tagging.html ka_track2_pipeline.html ka_track3_vr.html ka_track4_ux.html instructor_prep.html; do
  FULL="$KA_ROOT/160sp/$f"
  if [ -f "$FULL" ]; then
    LINES=$(wc -l < "$FULL")
    echo -e "\n=== FULL CONTENT: 160sp/$f ($LINES lines) ===" >> "$OUT"
    cat "$FULL" >> "$OUT"
  fi
done

# 14. Key root-level pages (homepages, auth pages)
for f in ka_home.html ka_home_student.html ka_user_home.html ka_login.html ka_register.html; do
  FULL="$KA_ROOT/$f"
  if [ -f "$FULL" ]; then
    LINES=$(wc -l < "$FULL")
    echo -e "\n=== FULL CONTENT: $f ($LINES lines) ===" >> "$OUT"
    cat "$FULL" >> "$OUT"
  fi
done

# 15. .htaccess and CORS config
echo -e "\n=== HTACCESS FILES ===" >> "$OUT"
find "$KA_ROOT" -name ".htaccess" -exec echo "--- {} ---" \; -exec cat {} \; >> "$OUT" 2>&1

# 16. Apache/nginx config for KA
echo -e "\n=== WEB SERVER CONFIG ===" >> "$OUT"
for f in /etc/apache2/sites-enabled/*ka* /etc/apache2/sites-enabled/*atlas* /etc/nginx/sites-enabled/*ka* /etc/nginx/sites-enabled/*atlas* /etc/nginx/conf.d/*ka* /etc/apache2/sites-available/*ka*; do
  if [ -f "$f" ]; then
    echo "--- $f ---" >> "$OUT"
    cat "$f" >> "$OUT" 2>&1
  fi
done

# 17. Data payloads inventory
echo -e "\n=== KA PAYLOADS INVENTORY ===" >> "$OUT"
ls -lhS "$KA_ROOT/data/ka_payloads/" >> "$OUT" 2>&1

# 18. Storage mount
echo -e "\n=== STORAGE MOUNT ===" >> "$OUT"
df -h /mnt/ka_storage >> "$OUT" 2>&1
ls -la /mnt/ka_storage/ >> "$OUT" 2>&1
df -h >> "$OUT" 2>&1

# 19. Student data directory (if exists)
echo -e "\n=== STUDENT DATA DIR ===" >> "$OUT"
ls -la "$KA_ROOT/data/student/" >> "$OUT" 2>&1

# 20. Other repos on server
echo -e "\n=== OTHER REPOS ===" >> "$OUT"
for d in $(dirname "$KA_ROOT")/*; do
  if [ -d "$d/.git" ]; then
    echo "REPO: $d" >> "$OUT"
    cd "$d" && git log --oneline -3 >> "$OUT" 2>&1
    echo "" >> "$OUT"
  fi
done

echo -e "\n=== SNAPSHOT COMPLETE ===" >> "$OUT"
LINES=$(wc -l < "$OUT")
SIZE=$(du -h "$OUT" | cut -f1)
echo "Snapshot saved to $OUT ($LINES lines, $SIZE)"
echo "Transfer with: scp xrlab:$OUT ."
