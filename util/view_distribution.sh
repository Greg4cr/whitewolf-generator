for((try=1;try<=100;try++)); do
    python ../src/Generator.py -c ../demo/sabbat.csv >> temp
    cat temp | grep "Clan" >>  clans.txt
    cat temp | grep "Generation" >>  gens.txt
    rm temp
done

cat clans.txt | sort -n | uniq -c | sort -n
cat gens.txt | sort -n | uniq -c | sort -n
rm clans.txt
rm gens.txt
