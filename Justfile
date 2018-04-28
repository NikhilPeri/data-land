deploy:
  git add .; git commit --amend --reuse-message=HEAD; git push -f origin master; git push -f heroku master
