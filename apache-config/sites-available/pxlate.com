<VirtualHost *:80>
  Servername pxlate.com
  DocumentRoot /home/pxlate/web

  # Expire times
  <IfModule mod_expires.c>
    ExpiresActive on
    ExpiresDefault "access plus 2 seconds"
    ExpiresByType text/html "access plus 2 seconds"
    ExpiresByType image/png "access plus 10 years"
  </IfModule>

  FileETag none

  <Directory /home/pxlate/web>
    AllowOverride All
  </Directory>
</VirtualHost>
