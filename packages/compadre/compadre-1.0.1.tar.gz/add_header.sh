for name in `find . -name \*.*pp`; do
    echo $name
    cat header.txt $name > file.txt; mv file.txt $name
done
