#!/usr/bin/env bash
# Nightly backup of the production database. Run by cron on the VM (see DEPLOY.md).
#
# Makes a safe copy with SQLite's backup API (fine while the API is running),
# keeps 14 days of copies in ~/backups, and, if RCLONE_REMOTE is set,
# also copies tonight's backup off the server (e.g. RCLONE_REMOTE=gdrive:nova-bot-backups).
#
# Backups contain real member info: they stay private (mode 600) and never go in git.
set -euo pipefail
umask 077

cd "$(dirname "$0")/.."
BACKUP_DIR="${BACKUP_DIR:-$HOME/backups}"
mkdir -p "$BACKUP_DIR"

DB="$(grep -E '^DATABASE_PATH=' .env | cut -d= -f2- || true)"
DB="${DB:-spots.db}"
OUT="$BACKUP_DIR/spots-$(date -u +%Y-%m-%d).db"

.venv/bin/python - "$DB" "$OUT" <<'EOF'
import sqlite3, sys
src = sqlite3.connect(sys.argv[1])
dst = sqlite3.connect(sys.argv[2])
with dst:
    src.backup(dst)
dst.close()
src.close()
EOF

find "$BACKUP_DIR" -name 'spots-*.db' -mtime +14 -delete

if [ -n "${RCLONE_REMOTE:-}" ]; then
    rclone copy "$OUT" "$RCLONE_REMOTE"
fi

echo "$(date -u +%FT%TZ) backed up $DB -> $OUT"
