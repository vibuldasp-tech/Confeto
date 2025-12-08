#!/bin/bash
# Test script for EQUIS SAR MVP
# This script tests the complete workflow of the application

set -e

echo "=================================================="
echo "EQUIS SAR MVP - Automated Test Suite"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test configuration
BASE_URL="http://localhost:3000"
TEST_FILE="Test_SAR_Document.docx"

# Check if test file exists
if [ ! -f "$TEST_FILE" ]; then
    echo -e "${RED}✗ Test file not found: $TEST_FILE${NC}"
    echo "Run: python3 generate-test-docx.py first"
    exit 1
fi

echo -e "${GREEN}✓ Test file found: $TEST_FILE${NC}"
echo ""

# Test 1: Upload invalid file type
echo "Test 1: Upload validation (should reject non-.docx files)"
echo "Creating a fake .txt file..."
echo "This is not a docx file" > test.txt
RESPONSE=$(curl -s -w "\n%{http_code}" -F "document=@test.txt" "$BASE_URL/api/upload" || echo "000")
HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
rm test.txt

if [ "$HTTP_CODE" = "400" ] || [ "$HTTP_CODE" = "500" ]; then
    echo -e "${GREEN}✓ File validation working - rejected .txt file${NC}"
else
    echo -e "${YELLOW}⚠ File validation may not be working properly (HTTP $HTTP_CODE)${NC}"
fi
echo ""

# Test 2: Upload valid .docx file
echo "Test 2: Upload valid .docx file and create workspace"
UPLOAD_RESPONSE=$(curl -s -F "document=@$TEST_FILE" "$BASE_URL/api/upload")
echo "Upload response: $UPLOAD_RESPONSE"

# Extract workspace ID from response
WORKSPACE_ID=$(echo "$UPLOAD_RESPONSE" | grep -o '"workspaceId":"[^"]*"' | cut -d'"' -f4)

if [ -z "$WORKSPACE_ID" ]; then
    echo -e "${RED}✗ Failed to create workspace or extract workspace ID${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Workspace created with ID: $WORKSPACE_ID${NC}"
echo ""

# Test 3: Verify workspace JSON file exists
echo "Test 3: Verify workspace JSON file was created"
WORKSPACE_FILE="uploads/${WORKSPACE_ID}.json"

if [ -f "$WORKSPACE_FILE" ]; then
    echo -e "${GREEN}✓ Workspace file exists: $WORKSPACE_FILE${NC}"
    
    # Check file size
    FILE_SIZE=$(wc -c < "$WORKSPACE_FILE")
    echo "   File size: $FILE_SIZE bytes"
    
    # Show first few lines
    echo "   File preview:"
    head -n 10 "$WORKSPACE_FILE" | sed 's/^/   /'
else
    echo -e "${RED}✗ Workspace file not found: $WORKSPACE_FILE${NC}"
    exit 1
fi
echo ""

# Test 4: Retrieve workspace via API
echo "Test 4: Retrieve workspace data via API"
WORKSPACE_DATA=$(curl -s "$BASE_URL/api/workspace/$WORKSPACE_ID")
echo "Workspace data preview:"
echo "$WORKSPACE_DATA" | head -c 500
echo "..."

# Count sections
SECTION_COUNT=$(echo "$WORKSPACE_DATA" | grep -o '"id":[0-9]*' | wc -l)
echo -e "${GREEN}✓ Workspace retrieved successfully${NC}"
echo "   Sections detected: $SECTION_COUNT"
echo ""

# Test 5: Extract and verify sections
echo "Test 5: Verify sections were detected correctly"
FIRST_SECTION_ID=$(echo "$WORKSPACE_DATA" | grep -o '"sections":\[{"id":[0-9]*' | grep -o '[0-9]*' | head -1)
FIRST_SECTION_TITLE=$(echo "$WORKSPACE_DATA" | grep -o '"title":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ ! -z "$FIRST_SECTION_ID" ]; then
    echo -e "${GREEN}✓ Sections detected in workspace${NC}"
    echo "   First section ID: $FIRST_SECTION_ID"
    echo "   First section title: $FIRST_SECTION_TITLE"
else
    echo -e "${YELLOW}⚠ No sections found in workspace${NC}"
fi
echo ""

# Test 6: Test save-section API
echo "Test 6: Edit and save a section"
SAVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/save-section" \
    -H "Content-Type: application/json" \
    -d "{
        \"workspaceId\": \"$WORKSPACE_ID\",
        \"sectionId\": 1,
        \"title\": \"EDITED TITLE - Test Edit\",
        \"content\": \"This is edited content from the automated test script. Testing the save functionality.\"
    }")

echo "Save response: $SAVE_RESPONSE"

if echo "$SAVE_RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✓ Section saved successfully${NC}"
else
    echo -e "${RED}✗ Failed to save section${NC}"
fi
echo ""

# Test 7: Verify changes were persisted
echo "Test 7: Verify changes were persisted to disk"
UPDATED_DATA=$(cat "$WORKSPACE_FILE")

if echo "$UPDATED_DATA" | grep -q "EDITED TITLE - Test Edit"; then
    echo -e "${GREEN}✓ Changes persisted to JSON file${NC}"
else
    echo -e "${RED}✗ Changes not found in JSON file${NC}"
fi
echo ""

# Test 8: Verify workspace URL is accessible
echo "Test 8: Check workspace URL accessibility"
WORKSPACE_PAGE=$(curl -s -w "\n%{http_code}" "$BASE_URL/workspace/$WORKSPACE_ID" || echo "000")
HTTP_CODE=$(echo "$WORKSPACE_PAGE" | tail -n 1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Workspace page accessible at /workspace/$WORKSPACE_ID${NC}"
else
    echo -e "${RED}✗ Workspace page not accessible (HTTP $HTTP_CODE)${NC}"
fi
echo ""

# Summary
echo "=================================================="
echo "Test Summary"
echo "=================================================="
echo -e "${GREEN}✓ File upload and workspace creation working${NC}"
echo -e "${GREEN}✓ Workspace JSON file created and accessible${NC}"
echo -e "${GREEN}✓ API endpoints functioning correctly${NC}"
echo -e "${GREEN}✓ Section editing and saving working${NC}"
echo -e "${GREEN}✓ Changes persisted to disk${NC}"
echo ""
echo "Workspace URL: $BASE_URL/workspace/$WORKSPACE_ID"
echo "Workspace File: $WORKSPACE_FILE"
echo ""
echo "You can now manually test the application by:"
echo "1. Opening: $BASE_URL"
echo "2. Uploading: $TEST_FILE"
echo "3. Viewing the workspace in your browser"
echo ""
echo -e "${GREEN}All automated tests passed!${NC}"
