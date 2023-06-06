ctime=$(date "+date: %d/%m/%Y; time: %H:%M:%S")
git add .
git commit -m "$ctime"
git push origin main