#!/bin/bash

# compile nunjucks templates

cmd=`npm bin`/nunjucks-precompile
echo $cmd

destination_file=`pwd`/../core/static/core/js/templates.js
# avoiding 2-d arrays
template_apps=(core interactive_visualization single_quiz manual_news_article_curation)
template_names=(feed_item.html feed_item.html feed_item.html feed_item.html)

rm -rf $destination_file

for (( i=0; i<${#template_apps[@]}; i++ )) do
    echo $i ${template_apps[$i]}/${template_names[$i]}
    cd ../${template_apps[$i]}/templates
    $cmd ${template_apps[$i]}/${template_names[$i]} >> $destination_file
    cd -
done

echo DONE
