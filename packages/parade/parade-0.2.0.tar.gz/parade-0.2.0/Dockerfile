FROM python:3-alpine
MAINTAINER He Bai <bai.he@outlook.com>

RUN apk add --no-cache --virtual .build-deps  \
		bzip2-dev \
		coreutils \
		dpkg-dev dpkg \
		expat-dev \
		gcc \
        g++ \
		gdbm-dev \
		libc-dev \
		libffi-dev \
		linux-headers \
		make \
		ncurses-dev \
		openssl \
		libressl-dev \
		pax-utils \
		readline-dev \
		sqlite-dev \
		tcl-dev \
		tk \
		tk-dev \
		xz-dev \
		zlib-dev \
    && apk add --no-cache postgresql-dev \
	&& apk add --no-cache mariadb-dev \
	&& apk add --no-cache subversion \
	&& pip install --upgrade pip \
	&& pip --no-cache-dir install pandas \
	&& pip --no-cache-dir install dash \
	&& pip --no-cache-dir install dash-html-components \
	&& pip --no-cache-dir install dash-core-components \
	&& pip --no-cache-dir install dash-table \
	&& pip --no-cache-dir install objgraph \
	&& pip --no-cache-dir install parade==0.1.22.4 \
	&& apk del .build-deps

EXPOSE 5000

VOLUME /workspace
WORKDIR /workspace

#ENTRYPOINT parade
#CMD server

