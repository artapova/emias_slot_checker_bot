while true; do
	python3 main_emias_checker.py >> log
	killall firefox geckodriver
	sleep 10
done