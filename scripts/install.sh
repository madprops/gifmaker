#!/usr/bin/env bash

root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"

content=$(cat <<EOF
#!/usr/bin/env bash
$parent/venv/bin/python $parent/src/main.py "\${@}"
EOF
)

echo "$content" > /tmp/gifmaker_tmp.sh
sudo sudo mv /tmp/gifmaker_tmp.sh /usr/bin/gifmaker
sudo sudo chmod +x /usr/bin/gifmaker
echo "Script created at /usr/bin/gifmaker"