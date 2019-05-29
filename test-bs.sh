#!/usr/bin/env bash
#   Run selective testcases, eg.: $>./test-bs.sh -t 1,2,3,4

usage()
{
    cat << USAGE >&2
Usage: Run selected testcases
    \$> $(basename $0) -t [testcases]
        [testcases]: 
            - testcase numbers, comma separated
            - if empty, run all available testcases
USAGE
    exit 1
}

# process arguments
if [ $# = 0 ]
then 
    echo "No argument found"
    usage
    exit 0;
fi
while [[ $# -gt 0 ]]
do
    case "$1" in
        -t)
        TESTCASES="$2"
        shift 2; shift 1
        ;;
        *)
        echoerr "Unknown argument: $1"
        usage
        exit 1;
        ;;
    esac
done

# Pass TESTCASES to docker-compose as an environment variable
echo "Spin up docker-compose, set TESTCASES='$TESTCASES'"

export TESTCASES=$TESTCASES
export RUN_ENV='bs'
docker-compose up --build --exit-code-from driver --abort-on-container-exit