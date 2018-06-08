The server runs on ubuntu/latest

to build the same version of ruby do the following steps:

git clone https://github.com/ruby/ruby.git
cd ruby
git checkout a5ec07c73fb667378ed617da6031381ee2d832b0 
git apply ../sandbox_patch
autoconf
./configure
make install
mv LFA.so /usr/local/lib/ruby/site_ruby/2.4.0/x86_64-linux/LFA.so

then check that ruby 'sample.rb' runs properly (if you have ruby pre-installed on the machine check that you are running the right version of ruby) 
