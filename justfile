# Important! Keep this rule at the top of the file!
# This insures that if you run `just` with no arguments, all the existing rules
# will be shown.
list:
    just --list

build:
    docker build -t pup.py .

run:
    docker run --rm --network host -it pup.py

bg_run:
    docker run --rm --network host --detach pup.py

run_command:
    curl -X POST http://127.0.0.1:8000/drive/1

run_command_live:
    curl -X POST https://puppy.conor.ooo/drive/1

stop:
    docker ps -a --filter "ancestor=pup.py" -q | xargs -r docker stop
