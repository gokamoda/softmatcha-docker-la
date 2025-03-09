
source .venv/bin/activate

# Japanese Wikipedia, 0.05B, fasttext-ja-vectors
# python src/download_corpora.py --dataset-name wikipedia-ja-20230720-100k
# python src/indexing.py \
#     --backend fasttext \
#     --model fasttext-ja-vectors \
#     --index src/fasttext-ja-vectors_wikipedia-ja-20230720-100k.h5 \
#     --num_workers 16 \
#     --buffer_size 10000 \
#     --chunk_size 1024 \
#     corpora/wikipedia-ja-20230720-100k.txt


# English Wikitext, 0.1B, glove-wiki-gigaword-300
# python src/download_corpora.py --dataset-name wikitext-103-raw-v1-train
# python src/indexing.py \
#     --backend gensim \
#     --model glove-wiki-gigaword-300 \
#     --index corpora/glove-wiki-gigaword-300_wikitext-103-raw-v1-train.h5 \
#     --num_workers 2 \
#     --buffer_size 10000 \
#     --chunk_size 1024 \
#     corpora/wikitext-103-raw-v1-train.txt


# python src/download_corpora.py --dataset-name latin-10m
# python src/indexing.py \
#     --backend gensim \
#     --model glove-wiki-gigaword-300 \
#     --index corpora/glove-wiki-gigaword-300_wikitext-103-raw-v1-train.h5 \
#     corpora/latin-10m.txt


# Latin augstinian_sermon_parallelisms, , fasttext-la-vectors
git clone https://github.com/Mythologos/Augustinian-Sermon-Parallelisms.git
python src/preprocess/augstinian_sermon_parallelisms.py
python src/indexing.py \
    --backend fasttext \
    --model fasttext-la-vectors\
    --index corpora/fasttext-la-vectors_augustinian-sermon-parallelisms.h5 \
    corpora/augustinian-sermon-parallelisms.txt

# Latin perseus, , fasttext-la-vectors
git clone https://github.com/cltk/lat_text_perseus.git
python src/preprocess/perseus_preprocess.py
python src/indexing.py \
    --backend fasttext \
    --model fasttext-la-vectors\
    --index corpora/fasttext-la-vectors_perseus.h5 \
    --num_workers 2 \
    corpora/lat_text_perseus_preprocessed.txt