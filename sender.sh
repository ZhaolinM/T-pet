echo "Check database for booking at 9:00AM"
python email_sender.py S0
sleep 90m
echo "Check database for booking at 10:30AM"
python email_sender.py S1
sleep 150m
echo "Check database for booking at 1:00PM"
python email_sender.py S2
sleep 90m
echo "Check database for booking at 2:30PM"
python email_sender.py S3
sleep 90m
echo "Check database for booking at 4:00PM"
python email_sender.py S4

