FROM php:7.0.22-fpm

RUN apt-get update && apt-get install -y gcc make git unzip zip wget openssl
RUN apt-get dist-upgrade -y

ENV USR_LOCAL=/usr/local
ENV LOCAL_ETC=${USR_LOCAL}/etc
ENV PHP_INI_DIR=${LOCAL_ETC}/php
ENV PHALCON_VERSION=3.2.2
ENV PHALCON_DEVTOOLS_VERSION=3.2.2

RUN apt-get install -y libpcre3-dev libmcrypt-dev libfreetype6-dev libjpeg62-turbo-dev libpng12-dev libxml2-dev libcurl4-gnutls-dev libpspell-dev zlib1g-dev libbz2-dev libicu-dev g++ mlocate libxslt-dev libaio-dev libyaml-dev
RUN docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/
RUN docker-php-ext-install opcache gd mysqli pdo pdo_mysql mcrypt intl mbstring soap curl xml pspell bz2 bcmath zip dba calendar xsl xmlrpc iconv sockets pcntl tokenizer
RUN docker-php-ext-enable opcache

RUN pecl install apcu \
    && pecl install apcu_bc-1.0.3 \
    && docker-php-ext-enable apcu --ini-name 10-docker-php-ext-apcu.ini \
    && docker-php-ext-enable apc --ini-name 20-docker-php-ext-apc.ini

RUN pecl install yaml-2.0.0 \
    && docker-php-ext-enable yaml --ini-name 30-docker-php-ext-yaml.ini

# Redis for php
# Currently not available through PECL :-(
RUN cd /etc && git clone --depth=1 https://github.com/phpredis/phpredis.git \
    && cd /etc/phpredis \
    && phpize \
    && ./configure \
    && make \
    && make install \
    && touch ${PHP_INI_DIR}/conf.d/ext-redis.ini \
    && echo 'extension=redis.so' >> ${PHP_INI_DIR}/conf.d/ext-redis.ini

WORKDIR /cphalcon
RUN wget https://github.com/phalcon/cphalcon/archive/v${PHALCON_VERSION}.tar.gz --output-document=./phalcon.tar.gz
RUN tar -xzf phalcon.tar.gz && cd cphalcon-${PHALCON_VERSION}/build && ./install
RUN echo 'extension=phalcon.so' | tee  ${PHP_INI_DIR}/conf.d/30-phalcon.ini && rm -rf /cphalcon

WORKDIR /phalcon-devtools
RUN wget https://github.com/phalcon/phalcon-devtools/archive/v${PHALCON_DEVTOOLS_VERSION}.tar.gz --output-document=./phalcon.tar.gz
RUN tar -xzf phalcon.tar.gz && mv phalcon-devtools-${PHALCON_DEVTOOLS_VERSION} /usr/local/phalcon-devtools && ln -s /usr/local/phalcon-devtools/phalcon.php /usr/local/bin/phalcon && chmod ugo+x /usr/local/bin/phalcon

RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
RUN php composer-setup.php --install-dir=/usr/local/bin --filename=composer
RUN php -r "unlink('composer-setup.php');"

RUN composer global require --dev phpunit/phpunit ^5
RUN ln -s ~/.composer/vendor/bin/phpunit /usr/local/bin/

# Timezone
RUN unlink /etc/localtime ; ln -s /usr/share/zoneinfo/Asia/Bangkok /etc/localtime

# Clean repository
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/server

EXPOSE 9000
CMD ["php-fpm"]
