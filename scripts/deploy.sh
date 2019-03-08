#!/bin/bash
# deploy web page
echo "Deploying to web"
echo "Cleaning deploy directory"
rm -rf deploy/public/*
rm -rf deploy/figure/*
echo  "Copying files to deploy"
cp -Rf htmlbase/* deploy/
cp -Rf html/* deploy/public
cp -Rf figure deploy/
echo "Compressing images.."
pngquant/pngquant.exe 256 --verbose --skip-if-larger --force --ext .png deploy/figure/*.png
echo "Removing powerpoint"
rm -f deploy/figure/*.pptx
echo "Pushing to repository" # assuming deploy is connected to netlify or similar service
cd "deploy" 
git add -A
git commit -m "deploy page"
git pull --rebase
git push
cd ..
echo "Deploying binaries to s3"
cp -Rf latex-book/lnotes_book.pdf binaries/
cp -Rf binaries/* C:/BINARYDIR # change to right dir
cd "C:/BINARYDIR"
read -p "Run acrobat? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    "C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe" # Acrobat executable
fi
read -p "Sync with s3? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    cd ..
    aws s3 sync . s3://AMAZONBUCKET # chenge to right dir
fi
