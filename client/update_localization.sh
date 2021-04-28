pybabel extract . -o localization/base.pot
pybabel update -i localization/base.pot -d localization
pybabel compile -d localization
