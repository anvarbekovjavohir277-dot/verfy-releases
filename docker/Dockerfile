# Verfy in a container, for CI: the CLI from PyPI, with Node.js (servers started with npx) and uv (servers started
# with uvx). Built and published by .github/workflows/docker.yml as ghcr.io/verfy-dev/verfy.
#
#   docker run --rm -v "$PWD:/work" ghcr.io/verfy-dev/verfy lock check
FROM node:22-bookworm-slim

ARG VERFY_VERSION
RUN test -n "$VERFY_VERSION" \
 && apt-get update -qq \
 && apt-get install -y -qq --no-install-recommends python3 python3-venv ca-certificates git > /dev/null \
 && rm -rf /var/lib/apt/lists/* \
 && python3 -m venv /opt/verfy \
 && /opt/verfy/bin/pip install --quiet --no-cache-dir --disable-pip-version-check "verfy==${VERFY_VERSION}" uv \
 && /opt/verfy/bin/verfy --version

# the update check only runs in an interactive terminal, so a container never reaches out on its own
ENV PATH="/opt/verfy/bin:${PATH}" \
    VERFY_HOME=/tmp/verfy
WORKDIR /work
LABEL org.opencontainers.image.source="https://github.com/verfy-dev/verfy-releases" \
      org.opencontainers.image.description="Verfy: lockfile and guard for the MCP tools your AI agents use" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.url="https://verfy.dev"
ENTRYPOINT ["verfy"]
CMD ["--help"]
