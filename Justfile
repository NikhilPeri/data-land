deploy:
  git add .; git commit --amend --reuse-message=HEAD; git push -f origin master; git push -f heroku master

start:
  brew services start postgresql

stop:
  brew services stop postgresql
