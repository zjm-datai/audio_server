FROM python:3.12-slim-bookworm AS base

WORKDIR /app/api

ENV UV_VERSION=0.8.9

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com

RUN pip install --no-cache-dir uv==${UV_VERSION}


FROM base AS packages

WORKDIR /app/api

RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --default-index https://pypi.tuna.tsinghua.edu.cn/simple

FROM base AS production

WORKDIR /app/api

ARG app_uid=1008
RUN groupadd -r -g ${app_uid} app && \
    useradd -r -u ${app_uid} -g ${app_uid} -s /bin/bash app && \
    chown -R app:app /app

ENV VIRTUAL_ENV=/app/api/.venv
COPY --from=packages --chown=app:app ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

COPY --chown=app:app . ./

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]