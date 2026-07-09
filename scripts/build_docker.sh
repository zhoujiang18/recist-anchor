#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${1:-medai:latest}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

docker build -t "${IMAGE_NAME}" "${REPO_ROOT}/submission"

