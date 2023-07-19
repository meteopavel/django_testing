#!/bin/bash

print_message () {
    # Print the line with message (first argument) on the full terminal width
    # using second argument to fill the space.
    # The default color is green. To switch to red pass a third argument with any value.
    local terminal_width=$(tput cols)
    local message=$1
    local symbol=$2
    local half_way=$((($terminal_width-${#message})/2))
    local left_filler_len=$(printf "%${half_way}s")
    local right_filler_len=$(printf "%$(($terminal_width-$half_way-${#message}))s")
    if [[ ! -z "$3" ]]; then echo -e "\033[0;31m"; else echo -e "\033[0;32m"; fi
    echo -e "${left_filler_len// /$symbol}$message${right_filler_len// /$symbol}\033[0m"
}


if python -m flake8 --config=setup.cfg 1>&2;
then
    print_message " flake8 завершил проверку кода, ошибок не обнаружено " "="
    echo $LF 1>&2
    if python structure_test.py
    then
        cd ya_news
        export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:="yanews.settings"}"
        if pytest --tb=line 1>&2;
        then
            cd ../ya_note
            unset DJANGO_SETTINGS_MODULE
            export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:="yanote.settings"}"
            if pytest --tb=line 1>&2;
            then
                exit 0
            else
                status=$?
                print_message " При запуске упали ваши тесты для проекта YaNote. Проверьте тесты этого проекта " "=" 1
                echo \`\`\` 1>&2
                exit $status
            fi
        else
            status=$?
            print_message " При запуске упали ваши тесты для проекта YaNews. Проверьте тесты этого проекта " "=" 1
            echo \`\`\` 1>&2
            exit $status
        fi
    else
        status=$?
        print_message " Убедитесь, что написанные вами тесты скопированы в указанные в ТЗ директории " "=" 1
        echo \`\`\` 1>&2
        exit $status
    fi
else
    status=$?
    print_message " flake8 обнаружил отклонения от стандартов, приведите код в соответствие с PEP8 " "=" 1
    echo \`\`\` 1>&2
    exit $status
fi
