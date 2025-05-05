echo "Ma'lumotlar bazasiga ulanish tekshirilmoqda..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 0.1
done

echo "PostgreSQL ishga tushdi. Migrate bajarilmoqda..."
python manage.py migrate

echo "Statik fayllar to‘planmoqda..."
python manage.py collectstatic --noinput

exec "$@"
