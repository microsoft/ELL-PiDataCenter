# disable existing trigger for PWR led
echo none | sudo tee /sys/class/leds/led1/trigger
max=$1
if [ -z "$1" ]
then
    max=10
fi

# start blinking it in 1 second loop
for ((i=0; i < $max; i++))
do
    echo $i
    echo 1 | sudo tee /sys/class/leds/led1/brightness > nul
    sleep 0.5
    echo 0 | sudo tee /sys/class/leds/led1/brightness > nul
    sleep 0.5
done

#re-enable PWR trigger
echo input | sudo tee /sys/class/leds/led1/trigger > nul

