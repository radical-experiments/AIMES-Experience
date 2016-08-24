#!/usr/bin/env bash

bindings='late_uniform'
BAGS='16 32 64 128 256 512 1024'
timings='Tx Tq TTC Ti To Ts'
pilots='1 2 3 4'

echo "Bak up current aggregated csv files..."
find . -type f -name '*.csv' -exec bash -c 'mv -v $0 ${0/.csv/.bak}' {} \;
find . -type f -name '*.csv'
echo "Done."

echo "Aggregate new csv files..."
get_fdata()
{

    fdata=""

    for bag in $BAGS; do
        fdata+="../${1}/${bag}/${2} "
    done

    echo "$fdata"
}

for binding in $bindings; do

    echo -e "\n$binding";

    for timing in $timings; do

        T=$timing.data;
        echo "$T";

        fdata=$(get_fdata "$binding" "$T")
        fout=../${binding}/${binding}_${timing}_excel.csv
        echo $fdata
        echo $fout
        pr -m -t -s, $fdata > $fout;

        if [[ 'late_uniform late_gauss' =~ ${binding} ]]; then

            for pilot in $pilots; do

                T="${timing}_p${pilot}.data";
                echo "$T";

                fdata=$(get_fdata "$binding" "$T")
                fout=../${binding}/${binding}_${T%.data}_excel.csv

                pr -m -t -s, $fdata > $fout;

            done;
        fi;
    done;
done
echo "Done."
