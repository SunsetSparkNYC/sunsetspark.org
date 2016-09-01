task :serve do
  exec('bundler exec jekyll serve --config _config.yml,_config_dev.yml -w')
end

task :test do
  ENV['NOKOGIRI_USE_SYSTEM_LIBRARIES'] = 'true'
  require 'html-proofer'
  sh "bundle exec jekyll build"
  HTMLProofer.check_directory("./_site").run
end

