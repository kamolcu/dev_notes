# OSX

1. Install phalcon developer tools as global package.
```sh
composer global require phalcon/devtools:dev-master
```
2. Make symbolic link
```sh
ln -s ~/.composer/vendor/phalcon/devtools/phalcon.php /usr/local/bin/phalcon
chmod ugo+x /usr/local/bin/phalcon
```
3. Install phalcon via home brew for php 5.6
```sh
brew install homebrew/php/php56-phalcon
```