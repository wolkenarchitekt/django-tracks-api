#!/bin/bash
# Install autoflake, black and isort and prettier before usage!
autoformat_file() {
    file="${1}"
    if [[ "${file}" != *.py ]] \
    && [[ "${file}" != *.js ]] \
    && [[ "${file}" != *.sql ]]; then
      continue
    fi

    file="${file}"
    tmpfile="$(mktemp /tmp/XXXXXXXXXXX)"
    cp "${file}" "${tmpfile}"
    echo "${file}"

    if [[ "${file}" == *.py ]]; then
      autoflake --in-place --remove-all-unused-imports "${file}"
      isort "${file}"
      black "${file}"
    elif [[ "${file}" == *.js ]]; then
      prettier --write "${file}"
    elif [[ "${file}" == *.sql ]]; then
      sqlformat \
        --reindent \
        --keywords upper \
        --identifiers lower \
        -o "${file}" \
        "${file}"
    fi
    git diff "${tmpfile}" "${file}"
}

for file in "${@}"; do
  autoformat_file "${file}"
done