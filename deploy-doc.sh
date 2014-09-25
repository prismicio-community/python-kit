cd docs && \
make html && \
cd _build/html && \
touch .nojekyll && \
git init . && \
git add . && \
git commit -m "Update documentation."; \
git push "git@github.com:prismicio/python-kit.git" master:gh-pages --force && \
rm -rf .git

