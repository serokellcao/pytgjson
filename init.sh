mkdir result

mkdir priv
cd priv
wget https://www.mtgjson.com/files/AllCards.json.zip
unzip *zip
rm *zip
cat AllCards.json | python -m json.tool | tee AllCards.pretty.json

mkdir sets
cd sets
wget https://www.mtgjson.com/files/AllSetFiles.zip
unzip *zip
rm *zip
