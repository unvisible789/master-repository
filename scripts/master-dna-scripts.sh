#!/bin/bash
#############################################################
# MASTER DNA SCRIPT COLLECTION                              #
# Utility snippets for DevOps, API, GitHub, ChatGPT, system #
#############################################################

# ---- 1. Basic Shell Automation ----

# List disk usage, sorted
du -h --max-depth=1 | sort -hr

# Find and delete files older than 30 days
find /path/to/dir -type f -mtime +30 -delete

# Monitor a process and alert if it's not running
process="nginx"
if ! pgrep $process; then
  echo "$process is not running!" | mail -s "Alert: $process down" you@example.com
fi

# ---- 2. API Interaction Templates ----

# cURL: GET request
curl -X GET "https://api.example.com/resource" -H "Authorization: Bearer YOUR_TOKEN"

# cURL: POST request with JSON
curl -X POST "https://api.example.com/resource" \
  -H "Content-Type: application/json" \
  -d '{"key1":"value1","key2":"value2"}'

# Python: GET request
python3 -c 'import requests; print(requests.get("https://api.example.com/resource").json())'

# ---- 3. GitHub Utilities ----

# Clone all repos from a user/org (requires GitHub CLI)
gh repo list ORG_OR_USER --limit 100 | while read -r repo _; do gh repo clone "$repo"; done

# Create an issue via GitHub CLI
gh issue create --title "Bug Report" --body "Describe the bug..."

# Fetch PRs assigned to you
gh pr list --assignee @me

# ---- 4. ChatGPT/OpenAI API ----

# Bash: Call OpenAI API (requires jq)
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_OPENAI_API_KEY" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Hello, world!"}]}' | jq '.choices[0].message.content'

# Python: Call OpenAI API
python3 -c '
import openai
openai.api_key = "YOUR_OPENAI_API_KEY"
resp = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": "Hello, world!"}]
)
print(resp.choices[0].message["content"])
'

# ---- 5. System Administration ----

# List open ports
sudo netstat -tulnp

# Backup a directory
tar -czvf backup.tar.gz /path/to/dir

# ---- 6. File Management ----

# Sync directories (rsync)
rsync -avh /src/dir/ /dest/dir/

# Search for text in all files recursively
grep -rnw '/path/to/dir' -e "search_term"

# ---- 7. Monitoring & Alerting ----

# CPU usage
top -bn1 | grep "Cpu(s)"

# Disk space alert
df -h | awk '$5 > 90 {print $0}'

# ---- 8. Miscellaneous Utilities ----

# Generate a random password
openssl rand -base64 16

# Encode/decode base64
echo "hello" | base64
echo "aGVsbG8=" | base64 --decode

# Convert JSON to YAML (requires yq)
cat file.json | yq -P

##############################################################
# End of Master DNA Scripts                                  #
# Copy, adapt, and extend as needed.                         #
##############################################################
