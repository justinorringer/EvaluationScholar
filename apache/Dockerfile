FROM ubuntu:latest

ENV TZ=US/Eastern

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update; \
    apt -y upgrade; \
    apt install -y apache2 apache2-bin shibboleth-sp-common shibboleth-sp-utils libapache2-mod-shib;

#RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
#    rm -rf /var/lib/apt/lists/*

#RUN echo '<Location /Shibboleth.sso>' >> /etc/apache2/conf-available/shib2.conf
#RUN echo '  SetHandler shib' >> /etc/apache2/conf-available/shib2.conf
#RUN echo '  AuthType None' >> /etc/apache2/conf-available/shib2.conf
#RUN echo '  Require all granted' >> /etc/apache2/conf-available/shib2.conf
#RUN echo '  RewriteEngine On' >> /etc/apache2/conf-available/shib2.conf
#RUN echo '  RewriteRule ^/Shibboleth.sso.* - [L]' >> /etc/apache2/conf-available/shib2.conf
#RUN echo '</Location>' >> /etc/apache2/conf-available/shib2.conf
RUN a2enmod rewrite expires shib ssl headers proxy proxy_http proxy_html
#RUN a2enconf shib2

COPY ./shibboleth/* /etc/shibboleth/

VOLUME /var/www/html

COPY run.sh /
RUN chmod +x /run.sh

RUN apt-get install dos2unix
RUN dos2unix ./run.sh

#RUN cd /etc/shibboleth/ \
#    && shib-keygen

#ENTRYPOINT ["service", "shibd", "start", ";"]

#CMD ["apache2ctl", "-D", "FOREGROUND"]

CMD ["/run.sh"]