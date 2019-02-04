@echo off

python -m pip install --upgrade pip

mkdir .tmp
cd .tmp
git clone https://github.com/facebookresearch/fastText
cd fastText
pip install .
cd ..
cd ..
::cleanup
rm fastText -rf

conda install faiss-cpu -c pytorch
conda install --file dev-requirements.txt

