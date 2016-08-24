#!/usr/bin/env bash

bindings='late_uniform'
bags='16 32 64 128 256 512 1024'
pilots='4'

echo "Bak up current data files..."
find . -type f -name '*.data' -exec bash -c 'mv -v $0 ${0/.data/.bak}' {} \;
find . -type f -name '*.data'
echo "Done."

echo "Compute new data files..."
for bind in $bindings; do

    for bag in $bags; do

        cd "../${bind}/${bag}"

        while IFS= read -r -d '' file; do

            bindarr=(${bind//_/ })
            export BINDING=${bindarr[0]}
            export TIME_DISTR=${bindarr[1]}

            #export PLOT_DIR='../../plots'
            #if [ ! -d "$PLOT_DIR/$bind" ]; then
            #    mkdir -p $PLOT_DIR/$bind
            #fi

            session=`basename ${file%.*}`
            rtimings=$(python ../../bin/get_timing.py "${session}")

            atimings=${rtimings%;*}

            npilots=${rtimings#*;}

            IFS=',' read -ra timings <<< "$atimings"

            for atiming in "${timings[@]}"; do
                
                echo "${atiming#*:}" >> ${atiming%:*}.data

                # Late binding has a variable number of pilots, depending on
                # their queuing time.
                if [[ "late_uniform late_gauss" =~ ${bind} ]]; then

                    # Empty files are needed to create empty cells in the
                    # aggregated csv files.
                    for pilot in $pilots; do
                        if [[ ! -f ${atiming%:*}_p${pilot}.data  ]]; then
                            touch ${atiming%:*}_p${pilot}.data
                        fi
                    done
                    
                    echo "${atiming#*:}" >> ${atiming%:*}_${npilots}.data
                fi
            done

        done < <(find . -type f -name '*.json' -print0)

        cd ../../bin

    done
done
echo "Done."
