# Homebrew Ruby. macOS /usr/bin/bundle is system Ruby 2.6 and cannot install these gems.
RUBY_BIN := /opt/homebrew/opt/ruby/bin
export PATH := $(RUBY_BIN):$(PATH)

.PHONY: run
run:
	@test -x $(RUBY_BIN)/bundle || { echo "Homebrew Ruby not found. Install it with: brew install ruby"; exit 1; }
	$(RUBY_BIN)/bundle install
	$(RUBY_BIN)/bundle exec jekyll serve
