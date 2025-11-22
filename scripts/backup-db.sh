#!/bin/bash

# Database Backup Script for EduFlow
# Backs up MongoDB and optionally uploads to cloud storage

set -e

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
MONGO_URL="${MONGO_URL:-mongodb://localhost:27017}"
DB_NAME="${DB_NAME:-eduflow}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="eduflow_backup_$DATE"
RETENTION_DAYS="${RETENTION_DAYS:-7}"

# S3 Configuration (optional)
S3_BUCKET="${S3_BUCKET:-}"
AWS_REGION="${AWS_REGION:-us-east-1}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🗄️  EduFlow Database Backup"
echo "=========================="
echo ""
echo "Date: $(date)"
echo "Database: $DB_NAME"
echo "Backup Dir: $BACKUP_DIR"
echo ""

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Perform backup
echo "Creating backup..."
if mongodump --uri="$MONGO_URL" --db="$DB_NAME" --out="$BACKUP_DIR/$BACKUP_FILE"; then
    echo -e "${GREEN}✅ Backup created successfully${NC}"
else
    echo -e "${RED}❌ Backup failed${NC}"
    exit 1
fi

# Compress backup
echo "Compressing backup..."
cd "$BACKUP_DIR"
tar -czf "${BACKUP_FILE}.tar.gz" "$BACKUP_FILE"
rm -rf "$BACKUP_FILE"
echo -e "${GREEN}✅ Backup compressed: ${BACKUP_FILE}.tar.gz${NC}"

# Calculate size
BACKUP_SIZE=$(du -h "${BACKUP_FILE}.tar.gz" | cut -f1)
echo "Backup size: $BACKUP_SIZE"

# Upload to S3 (if configured)
if [ -n "$S3_BUCKET" ]; then
    echo ""
    echo "Uploading to S3..."
    if aws s3 cp "${BACKUP_FILE}.tar.gz" "s3://$S3_BUCKET/backups/${BACKUP_FILE}.tar.gz" --region "$AWS_REGION"; then
        echo -e "${GREEN}✅ Uploaded to S3: s3://$S3_BUCKET/backups/${BACKUP_FILE}.tar.gz${NC}"
    else
        echo -e "${YELLOW}⚠️  S3 upload failed (continuing)${NC}"
    fi
fi

# Clean old backups
echo ""
echo "Cleaning old backups (keeping last $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "eduflow_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete
echo -e "${GREEN}✅ Old backups cleaned${NC}"

# List recent backups
echo ""
echo "Recent backups:"
ls -lh "$BACKUP_DIR"/eduflow_backup_*.tar.gz | tail -5

echo ""
echo -e "${GREEN}🎉 Backup completed successfully!${NC}"
echo ""
echo "To restore this backup:"
echo "  tar -xzf $BACKUP_DIR/${BACKUP_FILE}.tar.gz"
echo "  mongorestore --uri=\"$MONGO_URL\" $BACKUP_DIR/${BACKUP_FILE}/$DB_NAME"
